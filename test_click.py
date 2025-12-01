"""
Tıklama Testi
Koordinatların doğru çalışıp çalışmadığını test eder
"""
import json
import time
import pyautogui
from input_simulator import InputSimulator


def test_clicks():
    """Tıklama koordinatlarını test eder"""
    print("=" * 60)
    print("TIKLAMA TESTİ")
    print("=" * 60)
    
    # Config yükle
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Hata: config.json bulunamadı!")
        return
    
    coordinates = config.get("coordinates", {})
    input_field = coordinates.get("input_field", {})
    confirm_button = coordinates.get("confirm_button", {})
    
    simulator = InputSimulator()
    
    print("\n⚠ DİKKAT: Bu test gerçek tıklamalar yapacak!")
    print("Oyun penceresine odaklanın ve hazır olun.")
    
    confirm = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
    if confirm != 'e':
        print("Test iptal edildi.")
        return
    
    print("\n5 saniye içinde oyun penceresine geçin...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 1. Input field testi
    if input_field and input_field.get("x") != 0:
        print("\n" + "=" * 60)
        print("1. INPUT FIELD TESTİ")
        print("=" * 60)
        input_x = input_field.get("x", 0)
        input_y = input_field.get("y", 0)
        input_w = input_field.get("width", 200)
        input_h = input_field.get("height", 30)
        
        print(f"Koordinatlar: ({input_x}, {input_y}, {input_w}x{input_h})")
        print("Merkez:", input_x + input_w // 2, input_y + input_h // 2)
        print("\n3 saniye sonra input field'e tıklanacak...")
        time.sleep(3)
        
        simulator.click_center(input_x, input_y, input_w, input_h, 0.5)
        print("✓ Input field'e tıklandı")
        
        # OCR ile numara oku
        print("\nOCR ile numara okunuyor...")
        from ocr_reader import OCRReader
        from screenshot import ScreenshotCapture
        
        ocr = OCRReader()
        screenshot = ScreenshotCapture()
        
        ocr_area = coordinates.get("ocr_area", {})
        if ocr_area and ocr_area.get("x") != 0:
            ocr_x = ocr_area.get("x", 0)
            ocr_y = ocr_area.get("y", 0)
            ocr_w = ocr_area.get("width", 200)
            ocr_h = ocr_area.get("height", 100)
            
            ocr_settings = config.get("ocr_settings", {})
            preprocess = ocr_settings.get("preprocess", True)
            threshold = ocr_settings.get("threshold", 127)
            invert = ocr_settings.get("invert", False)
            
            number = ocr.read_number_from_region(
                ocr_x, ocr_y, ocr_w, ocr_h,
                preprocess=preprocess,
                threshold=threshold,
                invert=invert
            )
            
            if number:
                print(f"Okunan numara: '{number}'")
                print(f"\n'{number}' yazılacak...")
                time.sleep(1)
                
                # Mevcut içeriği temizle
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
                pyautogui.press('delete')
                time.sleep(0.1)
                
                # Sadece numara yaz
                simulator.type_numbers(number, 0.1)
                time.sleep(1)
                print("✓ Numara yazıldı")
            else:
                print("⚠ Numara okunamadı!")
        else:
            print("OCR alanı koordinatları tanımlı değil!")
    else:
        print("Input field koordinatları tanımlı değil!")
    
    # 2. Confirm button testi
    if confirm_button and confirm_button.get("x") != 0:
        print("\n" + "=" * 60)
        print("2. CONFIRM BUTTON TESTİ")
        print("=" * 60)
        confirm_x = confirm_button.get("x", 0)
        confirm_y = confirm_button.get("y", 0)
        confirm_w = confirm_button.get("width", 100)
        confirm_h = confirm_button.get("height", 30)
        
        print(f"Koordinatlar: ({confirm_x}, {confirm_y}, {confirm_w}x{confirm_h})")
        print("Merkez:", confirm_x + confirm_w // 2, confirm_y + confirm_h // 2)
        print("\n3 saniye sonra confirm butonuna tıklanacak...")
        time.sleep(3)
        
        simulator.click_center(confirm_x, confirm_y, confirm_w, confirm_h, 0.5)
        print("✓ Confirm butonuna tıklandı")
    else:
        print("Confirm button koordinatları tanımlı değil!")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nKontrol edin:")
    print("1. Input field'e tıklandı mı? (cursor görünmeli)")
    print("2. Yazı yazıldı mı?")
    print("3. Confirm butonuna tıklandı mı?")


if __name__ == "__main__":
    test_clicks()

