import re

BIRLER = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
BASAMAKLAR = [(10**12, "trilyon"), (10**9, "milyar"), (10**6, "milyon"), (1000, "bin")]


def _yuzluk(n: int) -> str:
    yuz, kalan = divmod(n, 100)
    on, bir = divmod(kalan, 10)
    parcalar = []
    if yuz:
        parcalar.append("yüz" if yuz == 1 else f"{BIRLER[yuz]} yüz")
    if on:
        parcalar.append(ONLAR[on])
    if bir:
        parcalar.append(BIRLER[bir])
    return " ".join(parcalar)


def sayi_oku(n: int) -> str:
    if n == 0:
        return "sıfır"
    parcalar = []
    for deger, ad in BASAMAKLAR:
        adet, n = divmod(n, deger)
        if adet:
            # Türkçede "bir bin" denmez, sadece "bin"
            parcalar.append(ad if (deger == 1000 and adet == 1) else f"{_yuzluk(adet)} {ad}")
    if n:
        parcalar.append(_yuzluk(n))
    return " ".join(parcalar)


def _ondalik_oku(tam: str, ondalik: str) -> str:
    if ondalik == "5":
        # konuşma dilinde: 3,5 -> üç buçuk, 0,5 -> yarım
        return "yarım" if tam == "0" else f"{sayi_oku(int(tam))} buçuk"
    sifirlar = len(ondalik) - len(ondalik.lstrip("0"))
    kalan = ondalik.lstrip("0")
    okunus = " ".join(["sıfır"] * sifirlar + ([sayi_oku(int(kalan))] if kalan else []))
    return f"{sayi_oku(int(tam))} virgül {okunus}"


def _sayi_ifadesi(m: re.Match) -> str:
    tam, ondalik, ek = m.group(1), m.group(2), m.group(3) or ""
    okunus = sayi_oku(int(tam)) if ondalik is None else _ondalik_oku(tam, ondalik)
    # 7'de -> yedide, 11'e -> on bire (ek, rakamın okunuşuna göre zaten doğru yazılmış olur)
    return okunus + ek


KISALTMALAR = {"TL": "lira", "kg": "kilo", "km": "kilometre", "cm": "santim", "dk": "dakika", "sn": "saniye"}


def turkce_normalize(metin: str) -> str:
    # 5 kg -> 5 kilo (sadece sayıdan sonra gelen kısaltmalar, yanlış eşleşme olmasın diye)
    metin = re.sub(
        r"(\d)\s?(" + "|".join(KISALTMALAR) + r")\b",
        lambda m: f"{m.group(1)} {KISALTMALAR[m.group(2)]}",
        metin,
    )
    # 1.250.000 -> 1250000 (binlik ayırıcı nokta)
    metin = re.sub(r"\d{1,3}(?:\.\d{3})+(?!\d)", lambda m: m.group().replace(".", ""), metin)
    # 14:30 -> on dört otuz
    metin = re.sub(r"\b(\d{1,2}):(\d{2})\b", lambda m: f"{m.group(1)} {int(m.group(2))}" if m.group(2) != "00" else m.group(1), metin)
    # %20 -> yüzde 20
    metin = re.sub(r"%\s?(?=\d)", "yüzde ", metin)
    return re.sub(r"(\d+)(?:,(\d+))?(?:['’](\w+))?", _sayi_ifadesi, metin)


if __name__ == "__main__":
    for ornek in ["352 lira", "1.250.000 TL", "%20 indirim", "3,5 derece", "1000 kişi", "2026 yılı", "0",
                  "saat 7'de", "11'e kadar", "2026’da", "3,5 günde", "1,5 saat", "0,5 litre", "%2,5 faiz",
                  "3,75 metre", "2,05 kg", "saat 14:30'da", "09:00"]:
        print(f"{ornek!r:>18} -> {turkce_normalize(ornek)}")
