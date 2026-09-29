"""Normal konuşmayı fısıltıya çevirir (WORLD vocoder).

Fısıltıda ses telleri titremez: perde (f0) yoktur, ses sadece havanın ağız boşluğundaki
rezonansıdır. Bu yüzden sesi analiz edip ağız rezonanslarını (spektral zarf) koruyor,
perdeyi sıfırlayıp gürültüyle yeniden sentezliyoruz. Tını (ağız yapısı) aynı kalır.
"""
import argparse

import numpy as np
import pyworld as pw
import soundfile as sf
from scipy.signal import butter, sosfilt


def fisiltiya_cevir(y: np.ndarray, sr: int, oran: float = 1.0) -> np.ndarray:
    """oran=1.0 tam fısıltı; 0 < oran < 1 nefesli / yarı fısıltı."""
    x = np.ascontiguousarray(y, dtype=np.float64)
    f0, t = pw.dio(x, sr, frame_period=5.0)
    f0 = pw.stonemask(x, f0, t, sr)
    sp = pw.cheaptrick(x, f0, t, sr)
    ap = pw.d4c(x, f0, t, sr)
    if oran >= 1.0:
        f0 = np.zeros_like(f0)
    else:
        ap = ap + (1.0 - ap) * oran
    z = pw.synthesize(f0, sp, ap, sr, frame_period=5.0)
    # fısıltıda gırtlaktan gelen kalın tonlar yoktur
    z = sosfilt(butter(2, 250, btype="highpass", fs=sr, output="sos"), z)
    return z.astype(np.float32)


def fisiltiya_cevir_lpc(y: np.ndarray, sr: int, derece: int = 18, ic_sr: int = 16000) -> np.ndarray:
    """Klasik fısıltı sentezi: her 25 ms'de ağız şeklini (LPC zarfı) çıkar, beyaz gürültüyle uyar.
    WORLD'ün ayrıntılı zarfı konuşmanın yapısını fazla taşıyor; LPC'nin kaba zarfı daha "havalı" çıkar."""
    import librosa
    from scipy.signal import lfilter

    x = librosa.resample(np.asarray(y, dtype=np.float32), orig_sr=sr, target_sr=ic_sr).astype(np.float64)
    x = np.append(x[0], x[1:] - 0.97 * x[:-1])  # ön vurgu: tiz rezonanslar da yakalansın
    cerceve, adim = int(0.025 * ic_sr), int(0.005 * ic_sr)
    pencere = np.hanning(cerceve)
    cikti = np.zeros(len(x) + cerceve)
    toplam_pencere = np.zeros_like(cikti)
    rng = np.random.default_rng(0)
    for i in range(0, len(x) - cerceve, adim):
        parca = x[i:i + cerceve] * pencere
        enerji = np.sqrt(np.mean(parca ** 2))
        if enerji < 1e-5:
            continue
        a = librosa.lpc(parca, order=derece)
        uyarim = lfilter([1.0], a, rng.standard_normal(cerceve))
        uyarim *= enerji / (np.sqrt(np.mean(uyarim ** 2)) + 1e-12)
        cikti[i:i + cerceve] += uyarim * pencere
        toplam_pencere[i:i + cerceve] += pencere ** 2
    cikti = cikti[:len(x)] / np.maximum(toplam_pencere[:len(x)], 1e-3)
    cikti = sosfilt(butter(2, 400, btype="highpass", fs=ic_sr, output="sos"), cikti)
    return librosa.resample(cikti.astype(np.float32), orig_sr=ic_sr, target_sr=sr)


def _formant_kaydir(a: np.ndarray, sr: int, oran: float, ust_sinir_hz: float = 1500.0) -> np.ndarray:
    """LPC kutuplarından üst sınırın altındakilerin frekansını oran kadar kaydırır (F1'i yukarı taşır)."""
    kokler = np.roots(a)
    sinir = 2 * np.pi * ust_sinir_hz / sr
    yeni = []
    for k in kokler:
        aci = np.angle(k)
        if 0 < abs(aci) < sinir:
            k = np.abs(k) * np.exp(1j * aci * oran)
        yeni.append(k)
    return np.real(np.poly(yeni))


def fisiltiya_cevir_lpc3(
    y: np.ndarray,
    sr: int,
    derece: int = 36,
    ic_sr: int = 32000,
    bant_genisletme: float = 0.98,
    unlu_kisma_db: float = 5.0,
    dinamik_us: float = 0.7,
    formant_orani: float = 1.0,
) -> np.ndarray:
    """lpc2 + gerçek fısıltının üç özelliği:
    - bant_genisletme: rezonansları yayvanlaştırır (a_k *= g^k), metalik çınlamayı alır
    - unlu_kisma_db / dinamik_us: fısıltıda ünlüler zayıflar, sessizler öne çıkar
    - formant_orani: fısıldarken ağız açılır, F1 yukarı kayar (1.0 = kaydırma yok)
    """
    import librosa
    from scipy.signal import lfilter

    x = librosa.resample(np.asarray(y, dtype=np.float32), orig_sr=sr, target_sr=ic_sr).astype(np.float64)
    # ünlüleri bulmak için: perdeli (ses tellerinin titrediği) anlar ünlü ve ötümlü sessizlerdir
    f0, _ = pw.dio(x, ic_sr, frame_period=5.0)
    x = np.append(x[0], x[1:] - 0.97 * x[:-1])
    cerceve, adim = int(0.025 * ic_sr), int(0.005 * ic_sr)
    pencere = np.hanning(cerceve)
    cikti = np.zeros(len(x) + cerceve)
    toplam_pencere = np.zeros_like(cikti)
    rng = np.random.default_rng(0)
    genisletme = bant_genisletme ** np.arange(derece + 1)
    unlu_kazanci = 10 ** (-unlu_kisma_db / 20)
    for i in range(0, len(x) - cerceve, adim):
        parca = x[i:i + cerceve] * pencere
        enerji = np.sqrt(np.mean(parca ** 2))
        if enerji < 1e-5:
            continue
        a = librosa.lpc(parca, order=derece) * genisletme
        if formant_orani != 1.0:
            a = _formant_kaydir(a, ic_sr, formant_orani)
        uyarim = lfilter([1.0], a, rng.standard_normal(cerceve))
        hedef = enerji ** dinamik_us
        f0_idx = min((i + cerceve // 2) * 1000 // (5 * ic_sr), len(f0) - 1)
        if f0[f0_idx] > 0:
            hedef *= unlu_kazanci
        uyarim *= hedef / (np.sqrt(np.mean(uyarim ** 2)) + 1e-12)
        cikti[i:i + cerceve] += uyarim * pencere
        toplam_pencere[i:i + cerceve] += pencere ** 2
    cikti = cikti[:len(x)] / np.maximum(toplam_pencere[:len(x)], 1e-3)
    cikti = sosfilt(butter(2, 400, btype="highpass", fs=ic_sr, output="sos"), cikti)
    return librosa.resample(cikti.astype(np.float32), orig_sr=ic_sr, target_sr=sr)


def son_parca(y: np.ndarray, sr: int, en_az_sessizlik: float = 0.4) -> np.ndarray:
    """duygulu_tts çıktısında parçalar arası duraklamalar tam sıfırdır; son duraklamadan sonrasını döndürür."""
    sifir = np.concatenate([[False], y == 0, [False]])
    degisim = np.flatnonzero(np.diff(sifir.astype(np.int8)))
    baslar, bitisler = degisim[::2], degisim[1::2]
    uzun = [(b, s) for b, s in zip(baslar, bitisler) if s - b >= en_az_sessizlik * sr]
    return y[uzun[-1][1]:] if uzun else y


def main():
    p = argparse.ArgumentParser(description="Bir kaydı fısıltıya çevirir.")
    p.add_argument("girdi")
    p.add_argument("--son-parca", action="store_true", help="duygulu_tts çıktısının sadece son cümlesini al")
    args = p.parse_args()

    y, sr = sf.read(args.girdi, dtype="float32")
    if args.son_parca:
        y = son_parca(y, sr)
    sf.write("fisilti_orijinal.wav", y, sr)
    # fısıltı gerçekte konuşmadan çok daha kısıktır; tepe 0.25 (~ -12 dBFS)
    denemeler = {
        # karşılaştırma için referans: Eren'in beğendiği sürüm
        "lpc2": fisiltiya_cevir_lpc(y, sr, derece=36, ic_sr=32000),
        # A: sadece rezonans genişletme (metalik iz gider mi?)
        "lpc3_a": fisiltiya_cevir_lpc3(y, sr, unlu_kisma_db=0.0, dinamik_us=1.0),
        # B: A + ünlüler kısık, sessizler öne çıkar
        "lpc3_b": fisiltiya_cevir_lpc3(y, sr),
        # C: B + ağız açılması (F1 %12 yukarı)
        "lpc3_c": fisiltiya_cevir_lpc3(y, sr, formant_orani=1.12),
    }
    for ad, z in denemeler.items():
        z = z / np.max(np.abs(z)) * 0.25
        sf.write(f"fisilti_{ad}.wav", z, sr)
        print(f"OK: fisilti_{ad}.wav ({len(z) / sr:.1f} sn)")


if __name__ == "__main__":
    main()
