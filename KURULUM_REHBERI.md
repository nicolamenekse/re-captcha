# Arduino USB HID Klavye - Kurulum Rehberi

## 📋 Adım Adım Kurulum

### 1️⃣ Arduino Satın Alma

**Gerekli Arduino Modelleri:**
- ✅ **Arduino Leonardo** (Önerilen - en yaygın)
- ✅ **Arduino Pro Micro** (Küçük ve ucuz)
- ❌ Arduino Uno (ÇALIŞMAZ - USB HID desteklemiyor)
- ❌ Arduino Nano (ÇALIŞMAZ - USB HID desteklemiyor)

**Nereden Alınır:**
- Türkiye: GittiGidiyor, Hepsiburada, N11 (yaklaşık 50-100 TL)
- Yurtdışı: Amazon, AliExpress (daha ucuz ama kargo süresi uzun)
- Yerel: Elektronik malzeme satan dükkanlar

**Önerilen:**
- Arduino Leonardo (orijinal veya klon - ikisi de çalışır)
- USB kablosu (genellikle Arduino ile birlikte gelir)

### 2️⃣ Arduino IDE Kurulumu

1. **Arduino IDE İndir:**
   - https://www.arduino.cc/en/software
   - "Windows Installer" seçin
   - İndirip kurun

2. **Arduino'yu Bağla:**
   - Arduino'yu USB kablosu ile bilgisayara bağlayın
   - Windows otomatik olarak driver yükleyecek

3. **Port Kontrolü:**
   - Arduino IDE'yi açın
   - **Tools > Port** menüsünden Arduino portunu seçin
   - Genellikle "COM3", "COM4" gibi görünür

### 3️⃣ Arduino Kodunu Yükleme

1. **Kodu Aç:**
   - `arduino_keyboard/arduino_keyboard.ino` dosyasını Arduino IDE'de açın

2. **Board Seç:**
   - **Tools > Board > Arduino Leonardo** (veya Pro Micro)

3. **Port Seç:**
   - **Tools > Port** menüsünden Arduino portunu seçin

4. **Yükle:**
   - **Sketch > Upload** (veya Ctrl+U)
   - "Done uploading" mesajını bekleyin

5. **Test:**
   - Arduino IDE'de **Tools > Serial Monitor** açın
   - "READY" mesajını görmelisiniz

### 4️⃣ Python Kütüphanesi Kurulumu

```bash
pip install pyserial
```

### 5️⃣ Test Etme

```bash
python arduino_keyboard/arduino_controller.py
```

**Beklenen Çıktı:**
```
✓ Arduino bağlandı: COM3
⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!
...
✓ Metin yazıldı
```

### 6️⃣ Ana Programda Kullanım

Arduino bağlıyken:

```bash
python auto_solution.py
```

Arduino otomatik olarak kullanılacak ve KGuard'ı atlatacak!

## 🔧 Sorun Giderme

### Arduino bulunamıyor:
- ✅ USB kablosunun veri aktarımı yapabildiğinden emin olun (sadece şarj kablosu çalışmaz)
- ✅ Farklı USB portunu deneyin
- ✅ Arduino IDE'de port seçimini kontrol edin
- ✅ Arduino'yu çıkarıp tekrar takın

### Komutlar çalışmıyor:
- ✅ Arduino IDE Serial Monitor'ü kapatın (Python ile çakışır)
- ✅ Arduino'yu yeniden başlatın (USB'den çıkarıp takın)
- ✅ Kodu tekrar yükleyin

### Input gönderilmiyor:
- ✅ Arduino Leonardo/Pro Micro kullandığınızdan emin olun
- ✅ Oyun penceresine odaklanın
- ✅ Input field'e tıklayın
- ✅ Arduino'nun "READY" mesajı gönderdiğinden emin olun

## 💡 Alternatif Çözümler

### Arduino yerine:
1. **Raspberry Pi Zero** (USB Gadget modu) - Daha gelişmiş ama daha pahalı
2. **Teensy** - Arduino benzeri ama daha güçlü
3. **Digispark** - Çok küçük ve ucuz ama kurulumu zor

### Arduino bulamazsanız:
- AliExpress'ten sipariş verin (2-3 hafta sürebilir)
- Yerel elektronik malzeme satan dükkanlara sorun
- İkinci el Arduino Leonardo arayın

## 📝 Özet

1. ✅ Arduino Leonardo/Pro Micro satın al
2. ✅ Arduino IDE kur
3. ✅ Kodu Arduino'ya yükle
4. ✅ `pip install pyserial`
5. ✅ Test et: `python arduino_keyboard/arduino_controller.py`
6. ✅ Kullan: `python auto_solution.py`

## 🎯 Sonuç

Arduino bağlıyken `auto_solution.py` otomatik olarak Arduino'yu kullanacak ve KGuard'ı atlatacak. Bu, yazılımsal yöntemlerin çalışmadığı durumlarda en etkili çözümdür!

