# 📖 Detaylı Kurulum Rehberi - Yeni Bilgisayar

Bu rehber, projeyi sıfırdan yeni bir bilgisayara kurmak için adım adım talimatlar içerir.

## 🎯 Ön Gereksinimler

- **Windows 10 veya 11** işletim sistemi
- **Python 3.8 veya üzeri** (Python 3.9+ önerilir)
- **İnternet bağlantısı** (ilk kurulum için)
- **SeaSRO2025** oyunu kurulu ve çalışır durumda
- **Yönetici yetkileri** (OSK ile çalışmak için gerekli olabilir)

---

## 📥 ADIM 1: Python Kurulumu

### Python'un Kurulu Olup Olmadığını Kontrol Et

1. **PowerShell** veya **CMD** açın
2. Şu komutu çalıştırın:
   ```bash
   python --version
   ```
3. Eğer Python kuruluysa, versiyon numarası görünecek (örn: `Python 3.11.5`)
4. Eğer "Python tanınmıyor" hatası alırsanız, Python'u kurmanız gerekir

### Python Kurulumu (Eğer Kurulu Değilse)

1. [Python.org](https://www.python.org/downloads/) adresine gidin
2. **"Download Python"** butonuna tıklayın (en son sürüm)
3. İndirilen `.exe` dosyasını çalıştırın
4. **ÖNEMLİ:** Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin! ✅
5. **"Install Now"** butonuna tıklayın
6. Kurulum tamamlandıktan sonra PowerShell'i kapatıp yeniden açın
7. Tekrar `python --version` komutu ile kontrol edin

---

## 📦 ADIM 2: Projeyi İndirme (Git Clone)

### Git Kurulu mu Kontrol Et

1. PowerShell'de şu komutu çalıştırın:
   ```bash
   git --version
   ```
2. Eğer Git kurulu değilse, [Git for Windows](https://git-scm.com/download/win) indirin ve kurun

### Projeyi Klonla

1. İstediğiniz bir klasöre gidin (örneğin Masaüstü):
   ```bash
   cd Desktop
   ```
2. Projeyi klonlayın:
   ```bash
   git clone https://github.com/nicolamenekse/re-captcha.git
   ```
3. Proje klasörüne girin:
   ```bash
   cd re-captcha
   ```
4. Dosyaların geldiğini kontrol edin:
   ```bash
   dir
   ```
   (veya `ls` - PowerShell'de her ikisi de çalışır)

---

## 🔧 ADIM 3: Python Kütüphanelerini Kurma

1. Proje klasöründe olduğunuzdan emin olun:
   ```bash
   cd re-captcha
   ```
2. Pip'in güncel olduğundan emin olun:
   ```bash
   python -m pip install --upgrade pip
   ```
3. Tüm bağımlılıkları kurun:
   ```bash
   pip install -r requirements.txt
   ```
4. Bu işlem **5-10 dakika** sürebilir (özellikle EasyOCR modelleri indirilecek)
5. Kurulum sırasında hata alırsanız, şu komutu deneyin:
   ```bash
   pip install -r requirements.txt --user
   ```

### ⚠️ İlk EasyOCR Kullanımı

İlk kez `auto_solution.py` çalıştırıldığında EasyOCR modelleri otomatik indirilecek (yaklaşık 200-300 MB). Bu normaldir ve sadece bir kez olur.

---

## 📝 ADIM 4: Konfigürasyon Dosyalarını Oluşturma

1. Örnek config dosyalarını kopyalayın:
   ```bash
   copy config.json.example config.json
   copy osk_calibration.json.example osk_calibration.json
   ```
   (PowerShell'de `copy` yerine `Copy-Item` da kullanabilirsiniz)

2. Dosyaların oluşturulduğunu kontrol edin:
   ```bash
   dir *.json
   ```
   Şunları görmelisiniz:
   - `config.json`
   - `osk_calibration.json`
   - `config.json.example`
   - `osk_calibration.json.example`

---

## 🎮 ADIM 5: Oyun Koordinatlarını Ayarlama

Bu adımda, oyun ekranındaki önemli alanların koordinatlarını belirleyeceksiniz.

### Ön Hazırlık

1. **SeaSRO2025** oyununu açın
2. Oyunu **tam ekran** veya **pencere modu**nda çalıştırın (tercih ettiğiniz mod)
3. Oyun penceresinin görünür olduğundan emin olun
4. Captcha ekranına geçin (oyunda "captcha" yazarak tetikleyebilirsiniz)

### Koordinat Kalibrasyonu

1. **ÖNEMLİ:** Oyun penceresini açın ve **captcha ekranına** geçin (oyunda "captcha" yazarak tetikleyebilirsiniz)

2. PowerShell'de (yönetici olarak çalıştırmanız önerilir):
   ```bash
   python setup_window.py
   ```
3. Script önce oyun penceresini bulacak, sonra size **4 alan** için koordinat belirlemenizi isteyecek:

   **a) OCR Alanı (Büyük Numara Okuma Alanı):**
   - Captcha ekranındaki **büyük numaranın** göründüğü çerçeve
   - Mouse'u bu alanın **sol üst köşesine** getirin
   - Terminal'e dönüp **ENTER** tuşuna basın
   - Sonra **sağ alt köşesine** getirin ve tekrar **ENTER** tuşuna basın

   **b) Input Field (Yazılacak Alan):**
   - Captcha numarasının **yazılacağı** metin kutusu
   - Mouse'u bu alanın **sol üst köşesine** getirin
   - Terminal'e dönüp **ENTER** tuşuna basın
   - Sonra **sağ alt köşesine** getirin ve tekrar **ENTER** tuşuna basın

   **c) Confirm Button (Onay Butonu):**
   - Captcha'yı **onaylamak için tıklanacak** buton
   - Mouse'u bu butonun **sol üst köşesine** getirin
   - Terminal'e dönüp **ENTER** tuşuna basın
   - Sonra **sağ alt köşesine** getirin ve tekrar **ENTER** tuşuna basın

   **d) Captcha Trigger Input (Chat Metin Kutusu - Opsiyonel):**
   - Oyun içinde **"captcha" yazılacak** chat metin kutusu
   - Bu adımı atlamak için direkt ENTER'a basabilirsiniz
   - Devam etmek için 'e' yazıp ENTER'a basın
   - Mouse'u bu alanın **sol üst köşesine** getirin ve **ENTER** tuşuna basın
   - Sonra **sağ alt köşesine** getirin ve tekrar **ENTER** tuşuna basın

4. Tüm koordinatlar kaydedildikten sonra `config.json` dosyası otomatik güncellenecek

### ✅ Kontrol

Koordinatların doğru kaydedildiğini kontrol edin:
```bash
type config.json
```
Koordinatların 0'dan büyük değerler olduğundan emin olun.

---

## ⌨️ ADIM 6: OSK (On-Screen Keyboard) Tuş Kalibrasyonu

OSK, anti-cheat sistemini bypass etmek için kullanılan sanal klavyedir. Her tuşun ekrandaki konumunu belirlemeniz gerekir.

### 6.1: OSK'yi Açma

1. Windows arama çubuğuna **"On-Screen Keyboard"** yazın
2. **"On-Screen Keyboard"** uygulamasını açın
3. OSK'yi ekranın **alt kısmına** yerleştirin (oyun penceresini kapatmayacak şekilde)
4. **OSK'yi açık bırakın** - script çalışırken her zaman açık olmalı

### 6.2: Sayı Tuşları Kalibrasyonu (0-9)

1. OSK açıkken, PowerShell'de (yönetici olarak):
   ```bash
   python calibrate_osk.py
   ```
2. Script size **0'dan 9'a kadar** her sayı için koordinat belirlemenizi isteyecek
3. Her sayı için:
   - Mouse'u OSK'deki **ilgili sayı tuşunun üzerine** getirin
   - **Terminal'e dönüp ENTER tuşuna basın**
   - Koordinat kaydedilecek
4. Tüm sayılar tamamlandığında `osk_calibration.json` dosyası otomatik güncellenecek

### 6.3: Harf Tuşları ve Enter Kalibrasyonu

1. OSK açıkken, PowerShell'de (yönetici olarak):
   ```bash
   python calibrate_osk_keys.py
   ```
2. Script size şu tuşlar için koordinat belirlemenizi isteyecek:
   - **c** (captcha kelimesi için)
   - **a** (captcha kelimesi için)
   - **p** (captcha kelimesi için)
   - **t** (captcha kelimesi için)
   - **h** (captcha kelimesi için)
   - **Enter** (göndermek için)
3. Her tuş için:
   - Mouse'u OSK'deki **ilgili tuşun üzerine** getirin
   - **Terminal'e dönüp ENTER tuşuna basın**
   - Koordinat kaydedilecek

### ✅ Kontrol

OSK kalibrasyonunun doğru kaydedildiğini kontrol edin:
```bash
type osk_calibration.json
```
Tüm tuşların koordinatlarının kaydedildiğinden emin olun.

---

## 🧪 ADIM 7: Test ve İlk Kullanım

### 7.1: OSK Testi

1. OSK'yi açık tutun
2. Herhangi bir metin editörü açın (Notepad, Cursor, VS Code)
3. PowerShell'de:
   ```bash
   python -c "from onscreen_keyboard import OnScreenKeyboardAuto; osk = OnScreenKeyboardAuto(); osk.type_with_osk('1234')"
   ```
4. Editörde "1234" yazılıp yazılmadığını kontrol edin

### 7.2: Tek Seferlik Captcha Çözümü Testi

1. **SeaSRO2025** oyununu açın
2. Oyun içinde **captcha ekranına** geçin (oyunda "captcha" yazarak)
3. OSK'yi açık tutun
4. PowerShell'de (yönetici olarak):
   ```bash
   python auto_solution.py
   ```
5. Script şunları yapmalı:
   - OCR ile numarayı okumalı
   - Input field'e tıklamalı
   - OSK ile numarayı yazmalı
   - Confirm butonuna tıklamalı

### 7.3: Tam Akış Testi (Trigger + OCR + Yaz + Confirm)

1. **SeaSRO2025** oyununu açın
2. Oyun penceresini **aktif** tutun
3. OSK'yi açık tutun
4. PowerShell'de (yönetici olarak):
   ```bash
   python auto_solution.py full
   ```
5. Script şunları yapmalı:
   - Chat'e "captcha" yazmalı ve Enter'a basmalı
   - Captcha ekranı çıktığında OCR ile numarayı okumalı
   - Input field'e tıklamalı
   - OSK ile numarayı yazmalı
   - Confirm butonuna tıklamalı

---

## 🚀 ADIM 8: Sürekli Döngü Modunu Başlatma

Artık her şey hazır! Sürekli çalışan otomatik sistem:

1. **SeaSRO2025** oyununu açın
2. Oyun penceresini **aktif** tutun
3. OSK'yi açık tutun
4. PowerShell'de (yönetici olarak):
   ```bash
   python auto_solution.py full_loop 330
   ```
   (330 saniye = 5.5 dakika aralıkla çalışır)

5. Script sürekli döngüde çalışacak:
   - Her 330 saniyede bir
   - Chat'e "captcha" yazacak
   - Captcha'yı okuyup çözecek
   - Bekleyip tekrar edecek

6. Durdurmak için: **Ctrl + C**

---

## ⚠️ Önemli Notlar

### Koordinatlar Her Bilgisayarda Farklıdır!

- **Farklı ekran çözünürlüğü** → Farklı koordinatlar
- **Farklı pencere modu** (tam ekran/pencere) → Farklı koordinatlar
- **Farklı monitör** → Farklı koordinatlar

**Çözüm:** Her yeni bilgisayarda **ADIM 5** ve **ADIM 6**'yı tekrar yapın!

### OSK Her Zaman Açık Olmalı

- Script çalışırken OSK **mutlaka açık** olmalı
- OSK kapanırsa script çalışmaz

### Yönetici Yetkileri

- Bazı durumlarda PowerShell'i **"Yönetici olarak çalıştır"** ile açmanız gerekebilir
- Özellikle OSK ile etkileşim için

### Oyun Penceresi Aktif Olmalı

- Script çalışırken oyun penceresi **aktif ve görünür** olmalı
- Oyun minimize edilirse script çalışmayabilir

---

## 🔧 Sorun Giderme

### "Oyun penceresi bulunamadı" Hatası

**Çözüm:**
1. Oyun penceresinin başlığının **"SeaSRO2025"** olduğundan emin olun
2. `config.json` dosyasında `window_name` değerini kontrol edin
3. Oyun penceresinin **aktif** olduğundan emin olun

### "Koordinatlar yanlış" / "Tıklama çalışmıyor"

**Çözüm:**
1. `setup_window.py` scriptini tekrar çalıştırın
2. Koordinatları yeniden belirleyin
3. Oyun penceresinin **aynı modda** (tam ekran/pencere) olduğundan emin olun

### "OCR numara okuyamıyor"

**Çözüm:**
1. `config.json` içindeki `ocr_area` koordinatlarını kontrol edin
2. Captcha ekranının **görünür** olduğundan emin olun
3. `debug_ocr_failed.png` dosyasını kontrol edin (varsa)

### "OSK tuşları çalışmıyor"

**Çözüm:**
1. OSK'nin **açık** olduğundan emin olun
2. `calibrate_osk.py` ve `calibrate_osk_keys.py` scriptlerini tekrar çalıştırın
3. OSK'nin **ekranda görünür** olduğundan emin olun

### "WinError 740" / "Erişim engellendi"

**Çözüm:**
1. PowerShell'i **"Yönetici olarak çalıştır"** ile açın
2. Script'i tekrar çalıştırın

---

## 📞 Yardım

Sorun yaşıyorsanız:
1. Terminal çıktısını kontrol edin
2. `config.json` ve `osk_calibration.json` dosyalarını kontrol edin
3. GitHub'da [Issue](https://github.com/nicolamenekse/re-captcha/issues) açın

---

## ✅ Kurulum Tamamlandı!

Artık sisteminiz hazır! İyi kullanımlar! 🎮✨

