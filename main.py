"""
ReCAPTCHA Çözücü - Ana Program
"""
import json
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader


def load_config():
    """Konfigürasyon dosyasını yükler"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json bulunamadı! Varsayılan ayarlar kullanılıyor.")
        return {}


def main():
    """Ana program"""
    print("=" * 50)
    print("ReCAPTCHA Çözücü - Başlatılıyor...")
    print("=" * 50)
    
    # Konfigürasyonu yükle
    config = load_config()
    
    # Screenshot modülünü başlat
    screenshot_capture = ScreenshotCapture()
    
    # Ekran bilgilerini göster
    screen_size = screenshot_capture.get_screen_size()
    print(f"\nEkran boyutu: {screen_size['width']}x{screen_size['height']}")
    
    print("\nModüller hazır!")
    print("\nKullanım:")
    print("  python coordinate_selector.py  # Koordinat seçme aracı")
    print("  python screenshot.py           # Screenshot testi")
    print("  python ocr_reader.py            # OCR testi")
    print("\nNot: OCR modülü ilk kullanımda modelleri indirecektir.")


if __name__ == "__main__":
    main()

