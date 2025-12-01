"""
OCR Test Aracı
Koordinatların doğru çalışıp çalışmadığını test eder
"""
import json
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader


def test_ocr_coordinates():
    """OCR koordinatlarını test eder"""
    print("=" * 60)
    print("OCR KOORDİNAT TESTİ")
    print("=" * 60)
    
    # Config yükle
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Hata: config.json bulunamadı!")
        return
    
    coordinates = config.get("coordinates", {})
    ocr_area = coordinates.get("ocr_area", {})
    
    if not ocr_area or ocr_area.get("x") == 0:
        print("Uyarı: OCR alanı koordinatları tanımlı değil!")
        return
    
    print(f"\nOCR Alanı Koordinatları:")
    print(f"  X: {ocr_area['x']}, Y: {ocr_area['y']}")
    print(f"  Genişlik: {ocr_area['width']}, Yükseklik: {ocr_area['height']}")
    
    # Screenshot al
    print("\nEkran görüntüsü alınıyor...")
    screenshot = ScreenshotCapture()
    
    # OCR alanını yakala
    x = ocr_area['x']
    y = ocr_area['y']
    width = ocr_area['width']
    height = ocr_area['height']
    
    print(f"\nBölge yakalanıyor: ({x}, {y}, {width}x{height})")
    region = screenshot.capture_region(x, y, width, height)
    screenshot.save_screenshot(region, "test_ocr_region.png")
    print("✓ Bölge kaydedildi: test_ocr_region.png")
    
    # OCR ile oku
    print("\nOCR ile okunuyor...")
    ocr = OCRReader()
    
    ocr_settings = config.get("ocr_settings", {})
    preprocess = ocr_settings.get("preprocess", True)
    threshold = ocr_settings.get("threshold", 127)
    invert = ocr_settings.get("invert", False)
    
    number = ocr.read_number_from_region(
        x, y, width, height,
        preprocess=preprocess,
        threshold=threshold,
        invert=invert
    )
    
    print("\n" + "=" * 60)
    print("SONUÇ")
    print("=" * 60)
    print(f"Okunan Numara: '{number}'")
    
    if number:
        print("✓ Numara başarıyla okundu!")
        print("\nÖnizleme görüntüsünü kontrol edin: test_ocr_region.png")
    else:
        print("⚠ Numara okunamadı!")
        print("\nKontrol edin:")
        print("1. Oyun penceresi açık ve görünür mü?")
        print("2. Koordinatlar doğru mu?")
        print("3. OCR ayarlarını (threshold, invert) değiştirmeyi deneyin")
    
    return number


if __name__ == "__main__":
    print("\n5 saniye içinde oyun penceresine geçin ve captcha görünsün!")
    import time
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    test_ocr_coordinates()

