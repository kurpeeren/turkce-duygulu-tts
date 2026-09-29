# Kendi sesini klonlamak için okuma metni

Her bölümü **ayrı bir dosya** olarak kaydet. Başlıkları okuma, sadece tırnak içindeki metni oku.

**Kayıt ipuçları**
- Telefonun ses kayıt uygulaması yeterli (m4a, mp3, wav fark etmez).
- Sessiz bir oda; televizyon, müzik, klima sesi olmasın. Telefonu ağzından 20-30 cm uzakta tut.
- Başta ve sonda 1 saniye sus.
- Kendi doğal hızınla, birine anlatır gibi oku. Hata yaparsan o dosyayı baştan kaydet.

---

## 1. Ana kayıt (zorunlu, ~25 sn) → `ana`

Bütün klonlama bu kayda dayanır. Türkçedeki bütün sesleri ve soru/düz cümle tonlamasını içerir.

> "Merhaba, bu kısa kaydı sesimi tanıtmak için yapıyorum. Bugün hava oldukça güzel; sabah erkenden kalkıp kısa bir yürüyüşe çıktım. Şehrin sessiz sokaklarında dolaşırken çiçek açmış ağaçlara ve işe yetişmek için acele eden insanlara baktım. Köşedeki küçük fırından taze bir simit ve bir de poğaça aldım. Sonra eve dönüp çayımı demledim ve yeni projeler üzerinde çalışmaya başladım. Peki, senin günün nasıl geçti?"

## 2. Duygu kayıtları (isteğe bağlı, her biri ~10 sn)

Bu kayıtlar `referanslar/<duygu>.wav` olur; o duygudaki cümleler senin gerçek tonunla üretilir.
Rol yapar gibi değil, gerçekten o duyguyu yaşıyormuş gibi oku.

**Neşeli** → `mutlu`
> "Harika bir haberim var! Başvurduğumuz işi aldık, hem de ilk denemede! İnanabiliyor musun, bu akşam kutlama yapıyoruz!"

**Üzgün** → `üzgün`
> "Bugün pek iyi hissetmiyorum. Uzun zamandır beklediğim haber geldi ama sonuç istediğim gibi olmadı. Neyse... yapacak bir şey yok."

**Kızgın** → `kızgın`
> "Bunu sana kaç kere söyledim! Her seferinde aynı hatayı yapıyorsun, sonra da hiçbir şey olmamış gibi davranıyorsun! Artık yeter!"

**Sakin** → `sakin`
> "Tamam, sakin olalım. Her şeyi adım adım konuşuruz. Acelemiz yok, yarın sabah oturup birlikte bakarız."

## 3. Sözsüz sesler (isteğe bağlı, her biri 3-5 sn)

Modelin iyi üretemediği sesler. Senin sesinden olursa doğrudan ses bankasına girer.

- **Gülme** → `gulme`: Aklına komik bir şey getir ve gerçekten gül. Zorla gülme doğal durmaz; birkaç deneme yapıp en doğalını gönder.
- **Düşünme** → `eee`: "Eee... bilmiyorum. Hmm... bir düşüneyim."
- **Nefes** → `nefes`: Derin bir nefes al, yavaşça ver. İki kez.

---

Dosyaları gönderdiğinde: ana kayıt varsayılan referans olur, duygu kayıtları `referanslar/` klasörüne, sözsüz sesler
`ses_bankasi/` klasörüne girer. Bu klasörler `.gitignore`'da olduğu için kayıtların asla repoya gitmez.
