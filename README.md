# Türkçe Duygulu TTS

Etiketli Türkçe metni duygulu konuşmaya çeviren küçük bir araç. [VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) modelinin
ses klonlama ve stil kontrolü üzerine kurulu; Türkçe sayı okuma ve fısıltı için kendi eklerini içerir.

```
[nötr] Merhaba Deniz, nasılsın? [eee] Nereden başlasam bilmiyorum.
[heyecanlı] Projeyi kazandık! Tam 3,5 milyon liralık bir bütçe!
[üzgün] [iç çekme] Ama kötü bir haber de var.
[fısıltı] [şşş] Aramızda kalsın ama... ben de biraz korkuyorum.
```

## Kurulum

Gerekenler: ~15 GB boş disk, ~8 GB GPU belleği (NVIDIA) ya da Apple Silicon Mac (16 GB+ bellek önerilir).

**macOS / Linux**
```bash
git clone https://github.com/kurpeeren/turkce-duygulu-tts.git
cd turkce-duygulu-tts
./kur.sh
```

**Windows** (NVIDIA GPU, Python 3.12)
```powershell
git clone https://github.com/kurpeeren/turkce-duygulu-tts.git
cd turkce-duygulu-tts
powershell -ExecutionPolicy Bypass -File kur.ps1
```

Kurulum betiği: Python ortamını kurar, modeli Hugging Face'ten test edilen sürüme sabitleyerek indirir (4,7 GB)
ve varsayılan referans sesi üretir. Tekrar çalıştırmak güvenlidir.

## Kullanım

```bash
.venv/bin/python duygulu_tts.py ornekler/tam_ornek.txt -o cikti.wav   # Windows: .venv\Scripts\python.exe
.venv/bin/python duygulu_tts.py ornekler/tam_ornek.txt --kuru         # modele gidecek metni göster, ses üretme
```

### Duygu etiketleri

Etiket, bir sonraki etikete kadar geçerlidir. Etiketsiz başlangıç nötr sayılır.

| Etiket | Eş anlamlılar |
|---|---|
| `[nötr]` | `[normal]` |
| `[mutlu]` | `[neşeli]` |
| `[heyecanlı]` | |
| `[kızgın]` | `[sinirli]`, `[öfkeli]` |
| `[bağırarak]` | `[bağır]`, `[bağıran]` |
| `[üzgün]` | `[hüzünlü]` |
| `[sakin]` | |
| `[fısıltı]` | `[fısıldayarak]` |
| `[stil: ...]` | Serbest İngilizce tarif, ör. `[stil: nervous, hesitant, slightly faster]` |

Büyük harf ve Türkçe karakter olmadan yazım (`[KIZGIN]`, `[uzgun]`) da tanınır.

### Sözsüz sesler

Tek seferliktir; yazıldığı yere eklenir, duyguyu değiştirmez.

| Etiket | Model etiketi | Durum |
|---|---|---|
| `[iç çekme]`, `[of]` | `[sigh]` | iyi çalışıyor |
| `[eee]`, `[hmm]`, `[ııı]` | `[Uhm]` | iyi çalışıyor, Türkçede "eee" olarak çıkıyor |
| `[şşş]`, `[sus]` | `[Shh]` | |
| `[vay]`, `[şaşırma]` | `[Surprise-wa]` | |
| `[hoşnutsuzluk]` | `[Dissatisfaction-hnn]` | |
| `[gülme]`, `[kahkaha]` | `[laughing]` | Türkçe cümlede zayıf, bkz. Bilinen sınırlar |

### Sayılar

Modelin kendi metin düzelticisi sayıları İngilizce okuduğu için kapalıdır; yerine `tr_normalize.py` kullanılır:
`3,5 gün` → üç buçuk gün, `0,5 litre` → yarım litre, `%20` → yüzde yirmi, `saat 14:30'da` → saat on dört otuzda,
`7'de` → yedide, `1.250.000` → bir milyon iki yüz elli bin, `5 kg` → beş kilo, `3 TL` → üç lira.

### Kendi sesin / farklı ses

Ses, modele gömülü değildir; 5-10 saniyelik bir referans kayıttan gelir.

- Varsayılan referans: `reference_female.wav` (kurulumda üretilir).
- Duyguya özel referans: `referanslar/<duygu>.wav` (ör. `referanslar/kızgın.wav`) varsa o duygu için kullanılır.
  Aynı kişinin o duyguyla konuştuğu kayıt, talimattan çok daha güçlü duygu verir.

## Nasıl çalışıyor

1. Metin etiketlere göre parçalanır, sayılar Türkçe okunuşa çevrilir.
2. Her parça için VoxCPM2'ye referans ses + metnin başında İngilizce stil talimatı verilir
   (ör. `(sad and disappointed, low soft voice, slower pace)Ama kötü bir haber de var.`).
3. Fısıltı parçaları ayrıca `fisilti.py` ile gerçek fısıltıya çevrilir: model referansla fısıldayamıyor ama fısıltı
   ritmini veriyor; ses tellerinin titreşimi (perde) kaldırılıp ağız şekli (LPC zarfı) gürültüyle yeniden sentezlenir.
4. Parçalar duyguya göre değişen duraklamalarla birleştirilir.

## Bilinen sınırlar

- **Gülme**: `[laughing]` Türkçe cümlelerde zayıf. `denemeler/gulme_denemesi.py` İngilizce cümle, yalnız gülme ve
  heceli gülme yöntemlerini dener (henüz sonuç yok).
- **Hız** (üretim süresi / ses süresi):

  | Donanım | Oran | 10 sn ses |
  |---|---|---|
  | RTX 4090 (geliştiricinin değeri) | ~0,3 | ~3 sn |
  | Apple M6 Mac mini, 24 GB, MPS (ölçüldü) | ~2,0 | ~20 sn |
  | RTX 4060 Laptop 8 GB, GPU başka işlerle paylaşılırken (ölçüldü) | ~40 | ~7 dk |

  Model ~8 GB bellek ister; 8 GB kartta başka işler varsa bellek taşar ve üretim onlarca kat yavaşlar.
  Model yüklemesi ayrıca ~13 sn sürer (Mac); uzun süre çalışan bir serviste bir kez yüklenir.
- **macOS**: MPS'te bfloat16 desteklenmediği için model float32 çalışır. torch 2.6 MPS'te çöktüğü için macOS'ta 2.11
  kurulur (`requirements.txt`).
- **Sonradan efekt işe yaramaz**: Perde/hız değiştirerek duygu vermeyi denedik; yapay duyuluyor. Duygu modelin
  kendisinden gelmeli (talimat ya da duygulu referans kayıt).
- **Trendyol/Trendyol-TTS**: Türkçe için ince ayarlanmış bir VoxCPM2 sürümü. Tek konuşmacıyla eğitilip ağırlıklara
  gömüldüğü için referans sesle klonlama yapamıyor (her zaman aynı sesi üretiyor); bu yüzden temel VoxCPM2 kullanılıyor.

## Kullanılan modeller ve atıflar

| Bileşen | Kaynak | Lisans / koşullar |
|---|---|---|
| **VoxCPM2** (TTS modeli) | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2), [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) | Apache-2.0. Model kartı taklit, dolandırıcılık ve dezenformasyon amaçlı kullanımı açıkça yasaklar; yapay ses olduğu belirtilmelidir |
| **voxcpm** (Python paketi) | [PyPI](https://pypi.org/project/voxcpm/) | OpenBMB |
| Stil talimatları ve sözsüz ses etiketleri | [VoxCPM belgeleri](https://voxcpm.readthedocs.io/en/latest/cookbook.html) | |
| **Varsayılan referans ses** | Microsoft Edge "tr-TR-EmelNeural", [edge-tts](https://github.com/rany2/edge-tts) ile | Microsoft'un sesidir; bu depoda dağıtılmaz, kurulumda kullanıcının kendi makinesinde üretilir. Ticari kullanımda Microsoft koşullarını kontrol edin ya da kendi/izinli bir referans ses kullanın |
| **WORLD vocoder** (fısıltı analizi) | [pyworld](https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder) | |
| Ses işleme | [librosa](https://librosa.org/), [SciPy](https://scipy.org/), [soundfile](https://github.com/bastibe/python-soundfile) | |
| Test edilip kullanılmayan | [Trendyol/Trendyol-TTS](https://huggingface.co/Trendyol/Trendyol-TTS) | |

## Etik kullanım

Gerçek bir kişinin sesini, o kişinin izni olmadan klonlamak için kullanmayın. Ürettiğiniz sesi paylaşırken yapay
olduğunu belirtin. `referanslar/` klasörü, kişisel ses kayıtları yanlışlıkla yayınlanmasın diye `.gitignore`'dadır.

## Lisans

Bu depodaki kod [MIT](LICENSE). Model ve servisler kendi lisanslarına tabidir (yukarıdaki tablo).
