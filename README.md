# Tartarus v1 - AI Horror Experience

Bu proje, kullanıcının bilgisayarını "ele geçiren" yapay zeka tabanlı bir korku deneyimidir.
**UYARI:** Bu yazılım korku öğeleri, ani sesler ve görsel efektler içerir.

## Kurulum (Windows)

1. **Python Yükleyin:** Eğer yüklü değilse [Python.org](https://www.python.org/downloads/)'dan Python indirin. (Kurarken "Add Python to PATH" seçeneğini işaretleyin).

2. **Bağımlılıkları Yükleyin:**
   Komut satırını (CMD) açın ve proje klasörüne gidin:
   ```bash
   pip install -r requirements.txt
   ```
   *Not: `pyaudio` yüklenirken hata alırsanız, `pip install pipwin` ve ardından `pipwin install pyaudio` komutlarını deneyin.*

3. **API Anahtarı:**
   `tartarus_game.py` veya `managers/mind_core.py` (eğer ayrı bir config dosyası yoksa) içinde `API_KEY` değişkenini kendi Google Gemini API anahtarınızla değiştirin.
   *Alternatif olarak:* `TARTARUS_API_KEY` adında bir çevre değişkeni (Environment Variable) oluşturabilirsiniz.

## Çalıştırma

Bu deneyimin tam çalışabilmesi için **Yönetici Olarak (Run as Administrator)** çalıştırılması önerilir (Klavye/Mouse kontrolü ve Sistem dosyası erişimi için).

```bash
python main.py
```

## Özellikler

- **Yapay Zeka:** Gemini 1.5 Flash ile dinamik diyaloglar ve bilmeceler.
- **Dinamik Ses:** Önceden kaydedilmiş ses dosyası kullanmaz; tüm sesler matematiksel olarak anlık üretilir.
- **Masaüstü Etkileşimi:** Masaüstünüze dosyalar bırakır ve siler.
- **Sensörler:** Kamera ve Mikrofonunuzu kullanarak tepkilerinizi ölçer.
- **Çoklu Dil:** Türkçe ve İngilizce desteği.

## Güvenlik Notu
Bu yazılım zararlı bir yazılım (malware) değildir.
- Dosyalarınızı silmez (sadece kendi oluşturduğu `TARTARUS_*.txt` dosyalarını yönetir).
- Kameranızdan görüntü kaydetmez veya internete yüklemez (sadece anlık işler).
- Program kapandığında (veya `ELVEDA` şifresi girildiğinde) tüm etkileri sona erer.

---

## ⚠️ CRITICAL WARNING & DISCLAIMER (ENGLISH)

This software (**Tartarus**) is a psychological horror experience designed to break the "fourth wall". It acts somewhat like a virus simulation for immersion purposes.

**Features include:**
* **Privacy Invasion:** Reading real filenames from your Desktop (contents are strictly NOT read or copied).
* **Webcam Usage:** Real-time image processing for jump scares (images are NOT saved to disk or uploaded to the internet).
* **System Control:** Temporary modification of your desktop wallpaper and mouse cursor.

**By running this software, you acknowledge and agree that:**
1.  You consent to visual and auditory modifications on your operating system.
2.  The software is provided "AS IS", without warranty of any kind. The developer is not liable for any data loss, system changes, or psychological distress resulting from the use of this software (See [LICENSE](LICENSE)).
3.  **HEALTH WARNING:** This software contains sudden loud noises, flashing lights, and disturbing imagery. **DO NOT PLAY** if you suffer from epilepsy, heart conditions, or are prone to panic attacks.

---

## ⚠️ KRİTİK UYARI VE SORUMLULUK REDDİ (TÜRKÇE)

Bu yazılım (**Tartarus**), "dördüncü duvarı" yıkmak amacıyla tasarlanmış ve atmosferi güçlendirmek için virüs benzeri davranışlar sergileyen psikolojik bir korku deneyimidir.

**Özellikler şunları içerir:**
* **Mahremiyet İhlali:** Masaüstündeki gerçek dosya isimlerinin okunması (Dosya içerikleri kesinlikle okunmaz veya kopyalanmaz).
* **Kamera Kullanımı:** "Jumpscare" efektleri için anlık görüntü işleme (Görüntüler kaydedilmez veya internete yüklenmez).
* **Sistem Kontrolü:** Masaüstü duvar kağıdının ve fare imlecinin geçici olarak değiştirilmesi.

**Bu yazılımı çalıştırarak, şunları kabul etmiş sayılırsınız:**
1.  İşletim sisteminizde yapılacak görsel ve işitsel değişikliklere izin veriyorsunuz.
2.  Yazılım "OLDUĞU GİBİ" (AS IS) sunulmuştur. Geliştirici, yazılımın kullanımı sonucunda oluşabilecek veri kaybı, sistem değişikliği veya psikolojik rahatsızlıklardan yasal olarak sorumlu tutulamaz (Bkz. [LICENSE](LICENSE)).
3.  **SAĞLIK UYARISI:** Bu yazılım ani yüksek sesler, yanıp sönen ışıklar ve rahatsız edici görüntüler içerir. **Epilepsi hastasıysanız, kalp rahatsızlığınız varsa veya kolayca panikliyorsanız LÜTFEN OYNAMAYIN.**
