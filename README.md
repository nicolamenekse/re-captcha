# ReCAPTCHA Otomatik Çözücü - SRO Client

Oyun ekranından screenshot alarak, belirli koordinatlardaki numaraları OCR ile okuyup, On-Screen Keyboard (OSK) kullanarak oyuna yazıp otomatik olarak çözen bir sistem.

## 🎯 Özellikler

- ✅ **Tam Otomatik**: Captcha tetikleme, OCR okuma, yazma ve onaylama tek komutla
- ✅ **On-Screen Keyboard (OSK) Desteği**: KGuard gibi anti-cheat sistemlerini bypass eder
- ✅ **Güçlü OCR**: EasyOCR ile yüksek doğrulukta numara okuma
- ✅ **Sürekli Döngü**: Belirli aralıklarla otomatik kontrol ve çözüm
- ✅ **Kolay Kalibrasyon**: İnteraktif koordinat ve OSK tuş kalibrasyonu

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- Windows 10/11
- SeaSRO2025 oyunu
- On-Screen Keyboard (OSK) - Windows ile birlikte gelir

## 🚀 Kurulum

> 📖 **Yeni bilgisayarda sıfırdan kurulum için:** [Detaylı Kurulum Rehberi](KURULUM_REHBERI_DETAYLI.md) dosyasına bakın!

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/nicolamenekse/re-captcha.git
cd re-captcha
```

### 2. Python Bağımlılıklarını Kurun

```bash
pip install -r requirements.txt
```

### 3. Konfigürasyon Dosyalarını Hazırlayın

```bash
# Örnek config dosyasını kopyalayın
copy config.json.example config.json
copy osk_calibration.json.example osk_calibration.json
```

### 4. Koordinatları Ayarlayın

**Oyun koordinatlarını ayarlama:**
```bash
python setup_window.py
```

**ÖNEMLİ:** Oyun penceresini açın ve captcha ekranına geçin (oyunda "captcha" yazarak tetikleyebilirsiniz)

Bu script ile şu alanların koordinatlarını belirleyeceksiniz:
1. OCR alanı (büyük numara okuma alanı) - Sol üst ve sağ alt köşeleri
2. Input field (yazılacak alan) - Sol üst ve sağ alt köşeleri
3. Confirm button (onay butonu) - Sol üst ve sağ alt köşeleri
4. Captcha trigger input (chat metin kutusu - opsiyonel) - Sol üst ve sağ alt köşeleri

**Her alan için:** Mouse'u köşeye getirin, terminal'e dönüp ENTER'a basın.

### 5. OSK Tuş Kalibrasyonu

**Sayı tuşları (0-9) için:**
```bash
python calibrate_osk.py
```

**Harf tuşları (c, a, p, t, h) ve Enter için:**
```bash
python calibrate_osk_keys.py
```

**Önemli:** 
- OSK'yi manuel olarak açık tutun. Script çalışırken OSK açık olmalı.
- Her tuş için: Mouse'u OSK'deki tuşun üzerine getirin, terminal'e dönüp ENTER'a basın.

## 💻 Kullanım

### Temel Komutlar

**Tek seferlik çözüm (sadece OCR + yazma + onay):**
```bash
python auto_solution.py
```

**Sadece captcha tetikleme (chat'e 'captcha' yazma):**
```bash
python auto_solution.py trigger
```

**Tam akış (tetikleme + OCR + yazma + onay):**
```bash
python auto_solution.py full
```

**Sürekli döngü (varsayılan 3 saniye aralık):**
```bash
python auto_solution.py loop
```

**Özel aralıklı döngü (örnek: 5 saniye):**
```bash
python auto_solution.py loop 5
```

**Tam akış sürekli döngü (varsayılan 330 saniye = 5.5 dakika):**
```bash
python auto_solution.py full_loop
```

**Özel aralıklı tam akış döngüsü:**
```bash
python auto_solution.py full_loop 600  # 10 dakika
```

## 📁 Proje Yapısı

```
re-captcha/
├── auto_solution.py          # Ana otomatik çözücü (KULLANILAN)
├── recaptcha_solver.py       # Eski çözücü (referans)
├── window_manager.py         # Pencere yönetimi
├── ocr_reader.py             # OCR okuma modülü
├── screenshot.py             # Ekran görüntüsü modülü
├── onscreen_keyboard.py      # OSK entegrasyonu
├── advanced_input.py         # Gelişmiş input yöntemleri
├── setup_window.py           # Koordinat ayarlama aracı
├── setup_captcha_trigger.py  # Captcha trigger koordinat ayarlama
├── calibrate_osk.py          # OSK sayı tuşları kalibrasyonu
├── calibrate_osk_keys.py     # OSK harf tuşları kalibrasyonu
├── config.json               # Oyun koordinatları (kullanıcıya özel)
├── osk_calibration.json      # OSK tuş koordinatları (kullanıcıya özel)
├── config.json.example       # Örnek config dosyası
├── osk_calibration.json.example  # Örnek OSK kalibrasyon dosyası
├── requirements.txt          # Python bağımlılıkları
└── README.md                 # Bu dosya
```

## ⚙️ Çalışma Mantığı

1. **Captcha Tetikleme** (opsiyonel): Chat metin kutusuna "captcha" yazar ve Enter'a basar
2. **OCR Okuma**: Belirlenen alandan büyük numarayı OCR ile okur
3. **Input Field'e Tıklama**: Yazılacak alana tıklar
4. **Yazma**: OSK kullanarak okunan numarayı yazar
5. **Onaylama**: Confirm butonuna tıklar

## 🔧 Sorun Giderme

### OSK Açılmıyor / "WinError 740" Hatası

**Çözüm:** OSK'yi manuel olarak açın:
1. Windows arama çubuğuna "On-Screen Keyboard" yazın
2. OSK'yi açın ve açık bırakın
3. Script'i çalıştırın

### Koordinatlar Yanlış

**Çözüm:** `setup_window.py` ve `calibrate_osk.py` scriptlerini tekrar çalıştırın.

### OCR Numarayı Okuyamıyor

**Çözüm:** 
- Oyun penceresinin tam ekran veya doğru çözünürlükte olduğundan emin olun
- `config.json` içindeki `ocr_area` koordinatlarını kontrol edin
- Debug görüntüleri (`debug_ocr_failed.png`) kontrol edin

### Script Terminalden Çalışmıyor

**Çözüm:** 
- Python'u ve script'i "Yönetici olarak çalıştır" ile başlatın
- Veya VSCode/Cursor içinden çalıştırın

## 📝 Notlar

- İlk kullanımda EasyOCR modelleri indirilecektir (birkaç yüz MB)
- OSK her zaman açık olmalıdır
- Oyun penceresi aktif ve görünür olmalıdır
- Koordinatlar ekran çözünürlüğüne ve pencere moduna bağlıdır
- Tam ekran ve pencere modu arasında geçiş yaparsanız koordinatları yeniden ayarlamanız gerekebilir

## 🛠️ Geliştirme

Bu proje, KGuard gibi anti-cheat sistemlerini bypass etmek için çeşitli input yöntemleri denemiştir:
- Win32 API (SendMessage, PostMessage)
- SendInput API
- PyAutoGUI
- Keyboard library
- On-Screen Keyboard (OSK) - **ÇALIŞAN YÖNTEM**
- Arduino USB HID (hardware-level) - alternatif çözüm

## 📄 Lisans

Bu proje eğitim amaçlıdır. Kendi sorumluluğunuzda kullanın.

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce bir issue açarak neyi değiştirmek istediğinizi tartışın.
