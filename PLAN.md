# ReCAPTCHA Çözücü Proje Planı

## Proje Özeti
Oyun ekranından screenshot alarak, belirli koordinatlardaki numaraları okuyup, oyuna yazıp ENTER ile gönderen bir sistem.

## İlerleme Adımları

### 1. Temel Altyapı Kurulumu
- [ ] Gerekli kütüphaneleri belirleme ve kurulum
  - `Pillow` veya `mss` - Ekran görüntüsü alma
  - `pytesseract` veya `easyocr` - OCR (Optik Karakter Tanıma)
  - `opencv-python` - Görüntü işleme
  - `pyautogui` veya `pynput` - Klavye/mouse kontrolü
  - `numpy` - Görüntü işleme için

### 2. Ekran Görüntüsü Alma Modülü
- [ ] Belirli bir pencere/oyun alanından screenshot alma
- [ ] Görüntüyü kaydetme ve işleme hazır hale getirme
- [ ] Performans optimizasyonu (hızlı screenshot alma)

### 3. Koordinat Belirleme Sistemi
- [ ] Kullanıcının manuel olarak koordinat seçebilmesi
- [ ] Koordinatları kaydetme (config dosyası)
- [ ] Birden fazla koordinat desteği (farklı numara alanları)

### 4. OCR (Optik Karakter Tanıma) Modülü
- [ ] Görüntüden belirli koordinatlardaki alanları kırpma
- [ ] OCR ile numara okuma
- [ ] Okuma doğruluğunu artırma (görüntü ön işleme: threshold, noise reduction)
- [ ] Hata yönetimi (okunamayan durumlar)

### 5. Klavye Simülasyonu
- [ ] Belirli pencereye odaklanma
- [ ] Numaraları yazma
- [ ] ENTER tuşuna basma
- [ ] Timing kontrolü (oyunun hazır olmasını bekleme)

### 6. Ana Akış Kontrolü
- [ ] Screenshot → OCR → Yazma → Enter döngüsü
- [ ] Hata yakalama ve retry mekanizması
- [ ] Loglama sistemi
- [ ] Kullanıcı arayüzü (opsiyonel: GUI veya CLI)

### 7. Optimizasyon ve İyileştirmeler
- [ ] Performans optimizasyonu
- [ ] Doğruluk artırma (OCR preprocessing)
- [ ] Konfigürasyon dosyası sistemi
- [ ] Test ve debug araçları

## Teknik Detaylar

### Önerilen Kütüphaneler:
```python
# Ekran görüntüsü
mss  # Hızlı screenshot için
Pillow  # Görüntü işleme

# OCR
easyocr  # Modern ve kolay kullanım
# veya
pytesseract  # Tesseract wrapper

# Görüntü işleme
opencv-python  # cv2
numpy

# Klavye kontrolü
pyautogui  # Basit ve kullanışlı
# veya
pynput  # Daha fazla kontrol

# Yardımcı
keyboard  # Global hotkey desteği için
```

### Proje Yapısı Önerisi:
```
re-captcha/
├── main.py              # Ana program
├── screenshot.py        # Screenshot modülü
├── ocr_reader.py        # OCR modülü
├── coordinate_manager.py # Koordinat yönetimi
├── input_simulator.py   # Klavye simülasyonu
├── config.json          # Konfigürasyon
├── requirements.txt     # Bağımlılıklar
└── README.md           # Dokümantasyon
```

## Başlangıç Adımları

1. **İlk olarak**: Temel screenshot alma ve görüntüleme
2. **İkinci**: Koordinat seçme aracı (mouse ile tıklayarak koordinat alma)
3. **Üçüncü**: OCR entegrasyonu ve test
4. **Dördüncü**: Klavye simülasyonu
5. **Beşinci**: Tüm parçaları birleştirme

## Notlar
- OCR doğruluğu için görüntü ön işleme kritik
- Oyun penceresine odaklanma önemli
- Timing kontrolü (oyunun hazır olmasını bekleme) gerekebilir
- Farklı ekran çözünürlükleri için koordinat scaling gerekebilir

