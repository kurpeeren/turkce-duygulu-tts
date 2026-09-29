# Ses modeli eğitimi (LoRA) için kayıt metni

~100 cümle, okuma süresi ~7-8 dakika. Her cümlenin duygusu bilindiği için eğitimde metnin başına
programın kullandığı talimat eklenir (ör. `(sad and disappointed, low soft voice, slower pace)`). Model böylece
"bu talimat gelince bu kişi böyle konuşur" diye öğrenir; fısıltı, gülme gibi modelin kendi başına iyi
yapamadığı şeyleri de senin kayıtlarından öğrenir.

Aynı kayıtlar eğitimden önce de işe yarar: her bölümden en iyi cümle `referanslar/<duygu>.wav` olarak kullanılabilir.

## Kayıt kuralları

- **Her bölüm ayrı dosya:** `01_notr`, `02_mutlu` ... (m4a, mp3, wav fark etmez).
- **Kodları okuma** (N01, M02...). Sadece cümleyi oku.
- **Cümleler arasında 2 saniye sus.** Program kaydı bu boşluklardan bölüp cümlelerle eşleştirecek.
- **Hata yaparsan:** 3 saniye sus, **aynı cümleyi baştan** oku. Tekrarları program ayıklar.
- **Bütün bölümler aynı koşullarda:** aynı oda, aynı telefon, ağızdan aynı uzaklık (20-30 cm). Farklı günlerde
  kaydedersen de aynı yeri kullan; oda sesi değişirse model onu da ses sanır.
- **Duyguyu gerçekten yaşa.** Abartılı tiyatro değil; o duyguda gerçekten nasıl konuşuyorsan öyle.
- Sayılar ve kısaltmalar zaten yazıyla; okuduğun ile yazılan birebir aynı olmalı.

---

## 01 · Nötr (~2 dk) → `01_notr`

Doğal, günlük konuşma. Bir kısmı müşteri hizmetleri tarzında.

- N01. Merhaba, Siyah Labs'e hoş geldiniz. Size nasıl yardımcı olabilirim?
- N02. Siparişinizin durumunu hemen kontrol ediyorum, bir dakika lütfen.
- N03. Kargonuz yarın öğleden sonra adresinize teslim edilecek.
- N04. Elektronik kart üretiminde ortalama teslim süremiz üç haftadır.
- N05. Bu konuda size e-posta ile ayrıntılı bilgi göndereceğim.
- N06. Toplantıyı perşembe saat on dörde aldık, uygun musunuz?
- N07. Hesabınızda görünen tutar ile faturadaki tutar birbirini tutmuyor.
- N08. Yeni sürümde birkaç hata düzeltildi ve uygulama biraz hızlandı.
- N09. Güneş batarken sahil boyunca yavaşça yürüdük.
- N10. Çocuklar bahçede top oynarken anneleri pencereden onları izliyordu.
- N11. Buzdolabında yoğurt, peynir ve birkaç domates kalmış.
- N12. Kışın dağ köylerine giden yollar bazen günlerce kapalı kalıyor.
- N13. Öğretmen, öğrencilerden ödevlerini cuma gününe kadar teslim etmelerini istedi.
- N14. Şehir merkezindeki müzede eski çağlara ait ilginç eserler var.
- N15. Jandarma, fırtına nedeniyle köprünün geçici olarak kapatıldığını duyurdu.
- N16. Bu akşam yemekte mercimek çorbası ve zeytinyağlı fasulye var.
- N17. Telefonunuzu şarj etmeyi unutmayın, yolculuk uzun sürecek.
- N18. Kitabın son bölümünü okuyunca her şey daha anlamlı geldi.
- N19. Görüşmemizi burada tamamlıyoruz, başka bir sorunuz var mı?
- N20. Bizi tercih ettiğiniz için teşekkür ederiz, iyi günler dilerim.

## 02 · Mutlu → `02_mutlu`

- M01. Ne güzel bir sürpriz bu, gerçekten çok sevindim!
- M02. Sonunda tatile çıkıyoruz, günlerdir bu anı bekliyordum.
- M03. Annem aradı, doğum günümü hiç unutmamış.
- M04. Proje çok beğenildi, müşteri bizimle çalışmaya devam etmek istiyor.
- M05. Bugün her şey yolunda gitti, içim içime sığmıyor.
- M06. Seni görmek ne kadar iyi geldi, anlatamam.
- M07. Kahvemi aldım, güneş de açtı, daha ne isteyeyim?
- M08. Harika bir iş çıkardın, seninle gurur duyuyorum.

## 03 · Heyecanlı → `03_heyecanli`

- H01. Haberi duydun mu? Başvurumuz kabul edildi!
- H02. Hemen gel, sana göstermem gereken bir şey var!
- H03. Maç son dakikada dönmüş, inanılmaz bir gol atmışlar!
- H04. Yarın ilk kez sahneye çıkıyorum, heyecandan uyuyamayacağım!
- H05. Yeni cihaz geldi, kutusunu açmak için sabırsızlanıyorum!
- H06. Bak, bak, ekranda sonuçlar çıkıyor!
- H07. Biletleri aldım, konsere gidiyoruz!
- H08. Bu fikir her şeyi değiştirebilir, hemen başlayalım!

## 04 · Üzgün → `04_uzgun`

- U01. Keşke o gün yanında olabilseydim.
- U02. Köpeğimiz dün gece öldü, evin içi çok sessiz.
- U03. Bütün emeklerimiz bir anda boşa gitti.
- U04. Onu bir daha göremeyeceğimi bilmek çok zor.
- U05. Bugün kimseyle konuşmak istemiyorum.
- U06. Eski fotoğraflara bakınca gözlerim doldu.
- U07. Elimden geleni yaptım ama yetmedi.
- U08. Bazen her şey üst üste geliyor, insan yoruluyor.

## 05 · Kızgın → `05_kizgin`

- K01. Bunu sana kaç kere söyledim, neden dinlemiyorsun?
- K02. Randevuya yine geç kaldın ve bir özür bile dilemedin!
- K03. Bu kabul edilemez, hemen bir yetkiliyle görüşmek istiyorum!
- K04. Sözünü tutmadın, bir daha sana nasıl güveneyim?
- K05. Üç haftadır aynı sorunu yaşıyorum ve kimse ilgilenmiyor!
- K06. Benim eşyalarımı izinsiz karıştırma!
- K07. Her seferinde bahane uyduruyorsun, artık bıktım!
- K08. Kapıyı çarpıp çıkması hiç hoş değildi.

## 06 · Bağırarak → `06_bagirarak`

Kısa tut, sesini zorlama. Telefonu biraz uzaklaştır, kayıt cızırdamasın.

- B01. Dur! Oraya gitme!
- B02. Buraya gel, hemen şimdi!
- B03. Duyuyor musun beni? Sesini kes!
- B04. Yangın var, herkes dışarı!
- B05. Yeter artık, sus!

## 07 · Sakin → `07_sakin`

- S01. Derin bir nefes al, her şey yoluna girecek.
- S02. Acele etmene gerek yok, zamanımız var.
- S03. Sorunu birlikte, adım adım çözeceğiz.
- S04. Önce oturalım, sonra her şeyi konuşuruz.
- S05. Endişelenme, ben buradayım.
- S06. Işıkları kısıp biraz dinlenelim.
- S07. Hata yapmak normal, önemli olan ondan ders almak.
- S08. Yağmurun sesi insanı ne kadar rahatlatıyor.

## 08 · Fısıltı → `08_fisilti`

**Gerçek fısıltı:** ses tellerin hiç titremesin, sadece hava. Telefonu biraz yaklaştır (15 cm).

- F01. Aramızda kalsın ama ben de biraz korkuyorum.
- F02. Sessiz ol, bebek yeni uyudu.
- F03. Arkana bakma, bizi izliyorlar.
- F04. Sana bir sır vereceğim, kimseye söyleme.
- F05. Film başladı, konuşmayalım.
- F06. Kapının arkasında biri var galiba.
- F07. Sürprizi bozma, o daha bir şey bilmiyor.
- F08. Şşş, dinle, bir ses geliyor.

## 09 · Gülme → `09_gulme`

G01-G04 sadece gülme. G05-G09'da **[gülme]** yazan yerde gerçekten gül, sonra konuşmaya devam et.
Zorla gülme doğal durmaz; aklına komik bir şey getir.

- G01. (kısa bir kıkırdama)
- G02. (içten bir kahkaha)
- G03. (tutamadığın, uzun bir gülme)
- G04. (hafif, gülümser gibi bir "hı hı")
- G05. Gerçekten mi? [gülme] Çok komiksin!
- G06. [gülme] Olamaz, yine mi aynı şakayı yaptın?
- G07. Kendimi tutamadım, [gülme] herkes bize bakıyordu.
- G08. Bunu hatırladıkça [gülme] hâlâ gülüyorum.
- G09. [gülme] Tamam, tamam, kabul ediyorum, haklısın.

## 10 · İç çekme → `10_ic_cekme`

- I01. [iç çekme] Neyse, yapacak bir şey yok.
- I02. [iç çekme] Yine mi toplantı?
- I03. Uzun bir gündü. [iç çekme] Artık eve gitmek istiyorum.
- I04. [iç çekme] Keşke her şey bu kadar zor olmasaydı.

## 11 · Tereddüt → `11_tereddut`

- T01. Eee... nereden başlasam bilmiyorum.
- T02. Hmm, bir düşüneyim, sanırım salı günü olabilir.
- T03. Şey... aslında bunu söylemek biraz zor.
- T04. Iıı, bir saniye, dosyayı arıyorum.
- T05. Eee, yani, tam emin değilim ama olabilir.

## 12 · Şaşırma → `12_sasirma`

- SA01. Vaaay! Bunu sen mi yaptın?
- SA02. Vay canına, hiç beklemiyordum!
- SA03. Aaa! Sen burada ne arıyorsun?
- SA04. Olamaz! Gerçekten kazandık mı?
- SA05. Hayret bir şey, bu kadar çabuk mu bitti?

## 13 · Nefes → `13_nefes`

- NF01. (derin bir nefes al, yavaşça ver)
- NF02. (kısa bir nefes al) Tamam, başlıyorum.
- NF03. (yorgun, uzun bir nefes ver)

---

## Kayıtlar gelince yapılacaklar

1. Her dosya 2 saniyelik boşluklardan cümlelere bölünür; Whisper ile yazıya çevrilip bu listedeki cümleyle
   eşleştirilir. Hatalı ve tekrar edilmiş okumalar ayıklanır.
2. Her cümle için eğitim satırı: `(bölümün talimatı)cümle` — `[gülme]` gibi yerler modelin etiketine çevrilir
   (`[laughing]`, `[sigh]`, `[Uhm]`).
3. Kiralık bir NVIDIA GPU'da (~20 GB bellek) LoRA eğitimi, 1-3 tur. Ara kayıtlar dinlenip en iyisi seçilir.
4. LoRA ayrı bir dosya olarak saklanır, temel modele gömülmez; diğer sesler de çalışmaya devam eder.
   Senin sesinden eğitilen dosya **açık repoya konmaz**.
