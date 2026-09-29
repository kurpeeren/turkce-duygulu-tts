"""[laughing] Türkçe cümlede zayıf. Dil mi sorun, yoksa gülme ayrı üretilip eklenebilir mi?
Henüz çalıştırılmadı. Çıktılar denemeler/ klasörüne yazılır."""
from pathlib import Path

import soundfile as sf
from voxcpm.core import VoxCPM

KOK = Path(__file__).resolve().parent.parent
BURASI = Path(__file__).resolve().parent

DENEMELER = [
    # 1) etiket İngilizce cümlede çalışıyor mu? (çalışıyorsa sorun Türkçe)
    ("ingilizce", "(cheerful and happy tone)Really? [laughing] You're so funny!"),
    # 2) sadece gülme: avatarın gülme kaydı olarak saklanabilir
    ("sadece_etiket", "(laughing heartily, joyful)[laughing]"),
    ("sadece_etiket_2", "(bursting into joyful laughter)[laughing] [laughing]"),
    # 3) heceyle
    ("heceli", "(amused, laughing heartily)Ha ha ha ha! Gerçekten mi? Çok komiksin!"),
]

model = VoxCPM.from_pretrained(hf_model_id=str(KOK / "models" / "VoxCPM2"), load_denoiser=False, optimize=False)

for ad, metin in DENEMELER:
    y = model.generate(
        text=metin,
        reference_wav_path=str(KOK / "reference_female.wav"),
        cfg_value=2.0,
        inference_timesteps=10,
        max_len=600,
        normalize=False,
        denoise=False,
    )
    cikti = BURASI / f"gulme_{ad}.wav"
    sf.write(cikti, y, model.tts_model.sample_rate)
    print(f"OK: {cikti}", flush=True)
