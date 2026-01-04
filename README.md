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
