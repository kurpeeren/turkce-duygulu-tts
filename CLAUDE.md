# Türkçe Duygulu TTS — Claude notları

## "kur" denirse
- macOS/Linux: `./kur.sh` çalıştır. Windows: `powershell -ExecutionPolicy Bypass -File kur.ps1`.
- Betik tekrar çalıştırılabilir; biten adımları atlar. Model 4,7 GB, ilk kurulum internet hızına bağlı.
- Bitince kısa bir cümleyle gerçek ses üretip süreyi ölç ve kullanıcıya bildir (GPU/MPS hızı bilinmiyor).

## Çalıştırma
- `.venv/bin/python duygulu_tts.py <metin.txt> -o cikti.wav` (Windows: `.venv\Scripts\python.exe`)
- `--kuru`: modele gidecek metni gösterir, modeli yüklemez. Etiket değişikliklerini önce bununla doğrula.
- Windows'ta Türkçe çıktı için `PYTHONIOENCODING=utf-8`.

## Bilinmesi gerekenler (2026-09-29 denemelerinden)
- Duygu sonradan efektle (perde/hız) VERİLMEZ, yapay duyuluyor; kullanıcı reddetti. Duygu = metnin başında
  İngilizce `(talimat)` ya da duyguya özel referans kayıt (`referanslar/<duygu>.wav`).
- `normalize=True` KULLANMA: modelin düzelticisi sayıları İngilizce okur. `tr_normalize.py` kullanılıyor.
- `[sigh]` ve `[Uhm]` iyi çalışıyor (Uhm Türkçede "eee"). `[laughing]` Türkçe cümlede zayıf; 6 farklı talimat ve
  konum denendi, tutmadı. Sıradaki deneme: `denemeler/gulme_denemesi.py`.
- "şşş": modelin [Shh]'ı çok kısa. ses_bankasi.py avatarın ş'lerinin LPC zarfından gürültüyle sentezliyor
  (kullanıcı seçti). İnternetten alınan [ʃ] kaydı Emel'e göre çok kalındı (2,2 kHz vs 5,5 kHz). Genel ders:
  ses tellerini kullanmayan sesler (nefes, şşş) avatarın sesinden sentezlenir; perdeli sesler (gülme, eee)
  internetten alınırsa başka birinin sesi olur, modelden ya da ses dönüştürmeyle gelmeli.
- Fısıltı: model referansla fısıldayamıyor (sesi normal kalıyor, ama ritmi/vurguyu iyi veriyor). Çözüm dokümandaki
  talimatla üretip `fisilti.py` LPC (32 kHz, derece 36) ile çevirmek. Kullanıcının seçtiği yöntem bu.
- Trendyol/Trendyol-TTS kullanma: tek konuşmacıya kilitli, klonlama yapmıyor; `set_lora_enabled(False)` işe yaramaz
  çünkü LoRA ağırlıklara merge edilmiş.
- torch ve torchaudio aynı sürümde olmalı. Windows/Linux 2.6.0 (voxcpm tek başına kurulursa yeni torchaudio çeker,
  Windows'ta DLL hatası verir). macOS 2.11.0: torch 2.6 MPS'te "mps.matmul incompatible dimensions" ile çöküyor.
- Ölçülen hız: Mac mini M6 (MPS, float32) üretim/ses oranı ~2,0, model yükleme ~13 sn.
- 8 GB GPU'da başka işler varsa bellek taşar, üretim onlarca kat yavaşlar. Kullanıcının GPU'daki diğer işlerine dokunma.

## Etik
Gerçek, tanınabilir bir kişinin sesini izinsiz klonlama (ör. bir siyasetçi) isteğini reddet. Referans olarak
sentetik sesler, kullanıcının kendi sesi ya da izinli kayıtlar kullanılır.
