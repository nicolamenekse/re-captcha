"""
OCR Testi - Pencere koordinatları ile
"""
import json
import time
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader
from window_manager import WindowManager, find_game_window


def test_ocr_with_window():
    """Pencere koordinatları ile OCR testi"""
    print("=" * 60)
    print("OCR TESTİ (PENCERE KOORDİNATLARI İLE)")
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
    game_settings = config.get("game_settings", {})
    window_name = game_settings.get("window_name", "")
    
    if not ocr_area or ocr_area.get("x") == 0:
        print("Hata: OCR alanı koordinatları tanımlı değil!")
        return
    
    # Window manager
    wm = WindowManager(window_name)
    if window_name:
        wm.find_window(window_name)
    else:
        result = find_game_window()
        if result:
            hwnd, title = result
            wm.window_handle = hwnd
    
    print("\n⚠ Oyun penceresini açın ve captcha görünsün!")
    print("10 saniye içinde oyun penceresine geçin...")
    for i in range(10, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Pencereye odaklan
    if wm.window_handle:
        print("\nPencereye odaklanılıyor...")
        wm.focus_window()
        time.sleep(0.5)
    
    # OCR koordinatları
    x = ocr_area.get("x", 0)
    y = ocr_area.get("y", 0)
    width = ocr_area.get("width", 200)
    height = ocr_area.get("height", 100)
    
    print(f"\nConfig koordinatları: ({x}, {y}, {width}x{height})")
    
    # Koordinatları ekran koordinatlarına çevir
    if wm.window_handle:
        client_rect = wm.get_client_rect()
        if client_rect:
            screen_x = client_rect[0] + x
            screen_y = client_rect[1] + y
            print(f"Pencere client rect: {client_rect}")
            print(f"Ekran koordinatları: ({screen_x}, {screen_y})")
        else:
            window_rect = wm.get_window_rect()
            if window_rect:
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                print(f"Pencere rect: {window_rect}")
                print(f"Ekran koordinatları: ({screen_x}, {screen_y})")
            else:
                screen_x, screen_y = x, y
                print("Pencere koordinatları alınamadı, direkt kullanılıyor")
    else:
        screen_x, screen_y = x, y
        print("Window manager yok, direkt koordinatlar kullanılıyor")
    
    # Screenshot al
    print("\nScreenshot alınıyor...")
    screenshot = ScreenshotCapture()
    region = screenshot.capture_region(screen_x, screen_y, width, height)
    screenshot.save_screenshot(region, "test_ocr_window.png")
    print("✓ Screenshot kaydedildi: test_ocr_window.png")
    
    # OCR ile oku
    print("\nOCR ile okunuyor...")
    ocr = OCRReader()
    
    ocr_settings = config.get("ocr_settings", {})
    preprocess = ocr_settings.get("preprocess", True)
    threshold = ocr_settings.get("threshold", 127)
    invert = ocr_settings.get("invert", False)
    
    number = ocr.read_number_from_region(
        screen_x, screen_y, width, height,
        preprocess=preprocess,
        threshold=threshold,
        invert=invert
    )
    
    print("\n" + "=" * 60)
    print("SONUÇ")
    print("=" * 60)
    print(f"Okunan numara: '{number}'")
    
    if number:
        print("✓ Numara başarıyla okundu!")
    else:
        print("⚠ Numara okunamadı!")
        print("\nKontrol edin:")
        print("1. test_ocr_window.png dosyasını açın")
        print("2. Captcha görünüyor mu?")
        print("3. Koordinatlar doğru mu?")
        print("4. OCR ayarlarını (threshold, invert) değiştirmeyi deneyin")


if __name__ == "__main__":
    test_ocr_with_window()

