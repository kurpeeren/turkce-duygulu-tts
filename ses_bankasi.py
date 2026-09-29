"""Avatarın kendi sesinden türetilen sözsüz sesler. Şimdilik: "şşş" (susturma).

Modelin [Shh] etiketi çok kısa bir ses veriyor. "ş" ses tellerini kullanmayan bir sestir; onu kişiye
özgü yapan ağız/dil şeklidir (spektral zarf). Bu yüzden modele ş'li bir cümle söyletip o cümledeki ş'lerin
LPC zarfını çıkarıyor, beyaz gürültüyü bu zarfla renklendirip uzun bir "şşş" sentezliyoruz.
İnternetten indirilen bir [ʃ] kaydı (erkek, ağırlık merkezi ~2,2 kHz) Emel'in ş'sine (~5,5 kHz) göre çok
kalındı; bu yöntem 2026-09-29 dinleme testinde tercih edildi.

Üretilen ses referans başına ses_bankasi/<referans adı>/ altında saklanır; başka bir sese geçilirse
"şşş" de o sesten yeniden türetilir.
"""
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, sosfilt

KOK = Path(__file__).resolve().parent
ONBELLEK = KOK / "ses_bankasi"
S_CUMLESI = "Şişede şeker var, şimdi şuraya koy. Şaşırdım, şahane bir iş!"


def _s_cerceveleri(y: np.ndarray, sr: int) -> tuple[np.ndarray, int]:
    """Enerjisi 2-6 kHz'de yoğunlaşan (ş/s) ve yeterince güçlü 10 ms'lik çerçeveler."""
    hop = int(0.01 * sr)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)) ** 2
    frek = librosa.fft_frequencies(sr=sr, n_fft=2048)
    oran = S[(frek > 2000) & (frek < 6000)].sum(axis=0) / (S.sum(axis=0) + 1e-12)
    enerji = np.sqrt(S.sum(axis=0))
    return (oran > 0.6) & (enerji > 0.1 * enerji.max()), hop


def _zarf(n: int, sr: int, acilis: float = 0.08, kapanis: float = 0.30) -> np.ndarray:
    """Hızlı açılış, hafif şişen orta kısım, yumuşak kapanış."""
    e = np.ones(n)
    a, k = int(acilis * sr), int(kapanis * sr)
    e[:a] = np.linspace(0, 1, a) ** 1.5
    e[-k:] = np.linspace(1, 0, k) ** 2
    return e * (0.85 + 0.15 * np.sin(np.linspace(0, np.pi, n)))


def sss_sentezle(konusma: np.ndarray, sr: int, sure: float = 1.1, seviye: float = 1.6) -> np.ndarray:
    """konusma: aynı sesle söylenmiş, ş'li bir cümle. seviye: konuşmadaki ş'ye göre güç (susturma biraz güçlü)."""
    secili, hop = _s_cerceveleri(konusma, sr)
    cerceve = int(0.025 * sr)
    parcalar = [konusma[i * hop: i * hop + cerceve] * np.hanning(cerceve)
                for i in np.flatnonzero(secili) if i * hop + cerceve <= len(konusma)]
    if len(parcalar) < 10:
        raise RuntimeError(f"cümlede yeterli ş bulunamadı ({len(parcalar)} çerçeve)")
    a = np.mean([librosa.lpc(p.astype(np.float64), order=30) for p in parcalar], axis=0)
    # katsayı ortalaması nadiren kararsız süzgeç verebilir; kutupları birim çemberin içine çek
    if np.max(np.abs(np.roots(a))) >= 1.0:
        a = a * 0.98 ** np.arange(len(a))
    rms = np.mean([np.sqrt(np.mean(p ** 2)) for p in parcalar])

    y = lfilter([1.0], a, np.random.default_rng(1).standard_normal(int(sure * sr))) * _zarf(int(sure * sr), sr)
    y = sosfilt(butter(2, 1000, btype="highpass", fs=sr, output="sos"), y)  # ş'de 1 kHz altı yok
    y = y / (np.sqrt(np.mean(y ** 2)) + 1e-12) * rms * seviye
    return np.clip(y, -0.95, 0.95).astype(np.float32)


def klip(ad: str, model, referans: str) -> np.ndarray:
    yol = ONBELLEK / Path(referans).stem / f"{ad}.wav"
    if yol.exists():
        y, _ = sf.read(yol, dtype="float32")
        return y
    if ad != "sss":
        raise ValueError(f"bilinmeyen ses: {ad}")
    sr = model.tts_model.sample_rate
    konusma = model.generate(text=S_CUMLESI, reference_wav_path=referans, cfg_value=2.0,
                             inference_timesteps=10, max_len=1000, normalize=False, denoise=False)
    y = sss_sentezle(konusma, sr)
    yol.parent.mkdir(parents=True, exist_ok=True)
    sf.write(yol, y, sr)
    return y
