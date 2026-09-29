"""Duygu etiketli Türkçe metni VoxCPM2 ile seslendirir.

Metin örneği:
    [nötr] Bugün sana bir şey anlatmam lazım.
    [kızgın] Sen zaten hep böyle yapıyorsun!
    [stil: nervous, hesitant, slightly faster] Ben... emin değilim.

Etiket, bir sonraki etikete kadar olan metne uygulanır. Etiketsiz başlangıç nötr sayılır.
Duygu, modelin kendi stil kontrolüyle üretilir: metnin başına "(talimat)" eklenir (VoxCPM2
"Controllable Cloning"). Talimatlar İngilizce, çünkü model talimatları EN/ZH ile eğitilmiş.
referanslar/<duygu>.wav varsa o duygu için referans ses olarak kullanılır.
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

from tr_normalize import turkce_normalize

KOK = Path(__file__).resolve().parent
VARSAYILAN_MODEL = KOK / "models" / "VoxCPM2"
VARSAYILAN_REFERANS = KOK / "reference_female.wav"  # kur.sh / kur.ps1 üretir
REFERANS_KLASORU = KOK / "referanslar"

# duraklama: bu parçadan sonraki sessizlik (sn)
DUYGULAR = {
    "nötr":      dict(talimat=None, duraklama=0.30),
    "mutlu":     dict(talimat="cheerful and happy tone, smiling while speaking", duraklama=0.25),
    "heyecanlı": dict(talimat="excited and energetic, slightly faster", duraklama=0.15),
    "kızgın":    dict(talimat="angry and frustrated, sharp emphasis on words", duraklama=0.20),
    "bağırarak": dict(talimat="shouting angrily, very loud, raised voice", duraklama=0.20),
    "üzgün":     dict(talimat="sad and disappointed, low soft voice, slower pace", duraklama=0.60),
    "sakin":     dict(talimat="calm, soft and gentle, slow pace", duraklama=0.50),
    # model referansla fısıldayamıyor ama bu talimatla fısıltı ritmi/vurgusu veriyor (dokümandaki örnek);
    # sesi sonradan LPC ile fısıltıya çeviriyoruz (fisilti.py). Eren'in seçimi: fisilti_birlesik_dokuman
    "fısıltı":   dict(talimat="Speaking slowly with a whispering, mysterious tone", duraklama=0.40, fisilti=True),
}

ESANLAMLILAR = {
    "notr": "nötr", "normal": "nötr",
    "neşeli": "mutlu", "neseli": "mutlu",
    "heyecanli": "heyecanlı",
    "kizgin": "kızgın", "sinirli": "kızgın", "öfkeli": "kızgın", "ofkeli": "kızgın",
    "bağır": "bağırarak", "bagir": "bağırarak", "bagirarak": "bağırarak", "bağıran": "bağırarak",
    "uzgun": "üzgün", "hüzünlü": "üzgün", "huzunlu": "üzgün",
    "fisilti": "fısıltı", "fısıldayarak": "fısıltı", "fisildayarak": "fısıltı",
}
FISILTI_TEPE = 0.25  # fısıltı normal konuşmadan belirgin kısık olmalı (~ -12 dBFS)

# Modelin metin içi sözsüz ses etiketleri (voxcpm.readthedocs.io, cookbook: Non-verbal Tags).
# Bunlar duygu değiştirmez; olduğu yere gülme/iç çekme vb. koyar ve modele aynen gider.
SOZSUZ_SESLER = {
    "laughing": "laughing", "gülme": "laughing", "gülerek": "laughing", "kahkaha": "laughing",
    "sigh": "sigh", "iç çekme": "sigh", "iç çek": "sigh", "of": "sigh",
    "uhm": "Uhm", "hmm": "Uhm", "ııı": "Uhm", "eee": "Uhm",
    "shh": "Shh", "şşş": "Shh", "sus": "Shh",
    "question-ah": "Question-ah", "question-ei": "Question-ei",
    "question-en": "Question-en", "question-oh": "Question-oh",
    "surprise-wa": "Surprise-wa", "surprise-yo": "Surprise-yo", "şaşırma": "Surprise-wa", "vay": "Surprise-wa",
    "dissatisfaction-hnn": "Dissatisfaction-hnn", "hoşnutsuzluk": "Dissatisfaction-hnn",
}

ETIKET = re.compile(r"\[([^\]]+)\]")
# sözsüz ses etiketleri ayrıştırma sırasında duygu etiketi sanılmasın diye geçici olarak bu işaretlere alınır
SOZSUZ_AC, SOZSUZ_KAPA = "⟦", "⟧"
CFG = 2.0


def _turkce_kucuk(metin: str) -> str:
    # Python'un lower()'ı Türkçe I/İ'yi bilmez
    return metin.strip().replace("I", "ı").replace("İ", "i").lower()


def sozsuzleri_koru(metin: str) -> str:
    def degistir(m):
        model_etiketi = SOZSUZ_SESLER.get(_turkce_kucuk(m.group(1)))
        return f"{SOZSUZ_AC}{model_etiketi}{SOZSUZ_KAPA}" if model_etiketi else m.group()
    return ETIKET.sub(degistir, metin)


def ayar_bul(etiket: str) -> tuple[str, dict]:
    """Etiketi (ad, ayar) çiftine çevirir. [stil: ...] serbest talimattır."""
    ham = etiket.strip()
    if ham.lower().startswith("stil:"):
        talimat = ham[5:].strip()
        return f"stil: {talimat}", dict(talimat=talimat, duraklama=0.30)
    ad = _turkce_kucuk(ham)
    ad = ESANLAMLILAR.get(ad, ad)
    if ad not in DUYGULAR:
        print(f"Uyarı: bilinmeyen etiket [{etiket}], nötr kullanılıyor", file=sys.stderr)
        ad = "nötr"
    return ad, DUYGULAR[ad]


def parcala(metin: str) -> list[tuple[str, dict, str]]:
    metin = sozsuzleri_koru(metin)
    parcalar = []
    ad, ayar = "nötr", DUYGULAR["nötr"]
    konum = 0
    for m in ETIKET.finditer(metin):
        onceki = metin[konum:m.start()].strip()
        if onceki:
            parcalar.append((ad, ayar, onceki))
        ad, ayar = ayar_bul(m.group(1))
        konum = m.end()
    kalan = metin[konum:].strip()
    if kalan:
        parcalar.append((ad, ayar, kalan))
    return parcalar


def model_metni(ayar: dict, parca: str) -> str:
    metin = turkce_normalize(parca).replace(SOZSUZ_AC, "[").replace(SOZSUZ_KAPA, "]")
    return f"({ayar['talimat']}){metin}" if ayar["talimat"] else metin


def referans_sec(ad: str) -> str:
    ozel = REFERANS_KLASORU / f"{ad}.wav"
    return str(ozel if ozel.exists() else VARSAYILAN_REFERANS)


def kirpma_koruma(y: np.ndarray) -> np.ndarray:
    tepe = np.max(np.abs(y))
    return y / tepe * 0.89 if tepe > 0.89 else y  # en fazla -1 dBFS


def seslendir(parcalar, cikti: str, model_yolu: str):
    from voxcpm.core import VoxCPM  # --kuru modelsiz çalışsın diye burada

    model = VoxCPM.from_pretrained(hf_model_id=model_yolu, load_denoiser=False, optimize=False)
    sr = model.tts_model.sample_rate
    sesler = []
    for i, (ad, ayar, parca) in enumerate(parcalar, 1):
        metin = model_metni(ayar, parca)
        print(f"({i}/{len(parcalar)}) {metin}", file=sys.stderr)
        y = model.generate(
            text=metin,
            reference_wav_path=referans_sec(ad),
            cfg_value=CFG,
            inference_timesteps=10,  # dokümandaki değer; beğenilen fısıltı da bununla üretildi
            max_len=4096,
            normalize=False,  # modelin normalizer'ı sayıları İngilizce okuyor
            denoise=False,
        )
        if ayar.get("fisilti"):
            from fisilti import fisiltiya_cevir_lpc

            y = fisiltiya_cevir_lpc(y, sr, derece=36, ic_sr=32000)
            y = y / (np.max(np.abs(y)) or 1.0) * FISILTI_TEPE
        sesler.append(y)
        sesler.append(np.zeros(int(sr * ayar["duraklama"]), dtype=np.float32))
    ses = kirpma_koruma(np.concatenate(sesler[:-1]))
    sf.write(cikti, ses.astype(np.float32), sr)
    print(f"OK: {cikti}")


def main():
    p = argparse.ArgumentParser(description="Duygu etiketli Türkçe metni VoxCPM2 ile seslendirir.")
    p.add_argument("girdi", help="Etiketli metin dosyası (.txt)")
    p.add_argument("-o", "--cikti", default="duygulu_cikti.wav")
    p.add_argument("--model", default=str(VARSAYILAN_MODEL))
    p.add_argument("--kuru", action="store_true", help="Modele gidecek metni göster, modeli yükleme")
    args = p.parse_args()

    parcalar = parcala(Path(args.girdi).read_text(encoding="utf-8"))
    if args.kuru:
        for ad, ayar, parca in parcalar:
            print(f"[{ad}] {model_metni(ayar, parca)}")
        return
    seslendir(parcalar, args.cikti, args.model)


if __name__ == "__main__":
    main()
