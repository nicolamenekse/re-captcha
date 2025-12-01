"""
Debug Test - Tüm adımları detaylı test eder
"""
import json
import time
import pyautogui
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader
from input_simulator import InputSimulator


def debug_test():
    """Tüm adımları detaylı test eder"""
    print("=" * 60)
    print("DEBUG TEST - DETAYLI ADIM ADIM TEST")
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
    input_field = coordinates.get("input_field", {})
    confirm_button = coordinates.get("confirm_button", {})
    
    simulator = InputSimulator()
    
    print("\n⚠ DİKKAT: Bu test gerçek işlemler yapacak!")
    print("Oyun penceresine odaklanın ve captcha görünsün.")
    
    confirm = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
    if confirm != 'e':
        print("Test iptal edildi.")
        return
    
    print("\n5 saniye içinde oyun penceresine geçin...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # ADIM 1: OCR
    print("\n" + "=" * 60)
    print("ADIM 1: OCR İLE NUMARA OKUMA")
    print("=" * 60)
    
    if not ocr_area or ocr_area.get("x") == 0:
        print("Hata: OCR alanı koordinatları tanımlı değil!")
        return
    
    ocr = OCRReader()
    ocr_x = ocr_area.get("x", 0)
    ocr_y = ocr_area.get("y", 0)
    ocr_w = ocr_area.get("width", 200)
    ocr_h = ocr_area.get("height", 100)
    
    ocr_settings = config.get("ocr_settings", {})
    preprocess = ocr_settings.get("preprocess", True)
    threshold = ocr_settings.get("threshold", 127)
    invert = ocr_settings.get("invert", False)
    
    print(f"OCR alanı: ({ocr_x}, {ocr_y}, {ocr_w}x{ocr_h})")
    number = ocr.read_number_from_region(
        ocr_x, ocr_y, ocr_w, ocr_h,
        preprocess=preprocess,
        threshold=threshold,
        invert=invert
    )
    
    if not number:
        print("Hata: Numara okunamadı!")
        return
    
    print(f"✓ Okunan numara: '{number}'")
    
    # ADIM 2: Input field'e tıkla
    print("\n" + "=" * 60)
    print("ADIM 2: INPUT FIELD'E TIKLAMA")
    print("=" * 60)
    
    if not input_field or input_field.get("x") == 0:
        print("Hata: Input field koordinatları tanımlı değil!")
        return
    
    input_x = input_field.get("x", 0)
    input_y = input_field.get("y", 0)
    input_w = input_field.get("width", 200)
    input_h = input_field.get("height", 30)
    input_center_x = input_x + input_w // 2
    input_center_y = input_y + input_h // 2
    
    print(f"Input field: ({input_x}, {input_y}, {input_w}x{input_h})")
    print(f"Merkez: ({input_center_x}, {input_center_y})")
    current_pos = pyautogui.position()
    print(f"Mevcut mouse pozisyonu: {current_pos}")
    
    print("\n3 saniye sonra input field'e tıklanacak...")
    print("⚠ LÜTFEN OYUN PENCERESİNE MANUEL OLARAK TIKLAYIN VE AKTİF EDİN!")
    time.sleep(3)
    
    print("Mouse hareket ettiriliyor...")
    # Önce FAILSAFE'i kontrol et
    pyautogui.FAILSAFE = False  # Geçici olarak kapat (dikkatli kullanın!)
    
    try:
        # Mouse'u hareket ettir
        pyautogui.moveTo(input_center_x, input_center_y, duration=0.5)
        time.sleep(0.3)
        new_pos = pyautogui.position()
        print(f"Mouse pozisyonu (hareket sonrası): {new_pos}")
        
        if abs(new_pos.x - input_center_x) > 10 or abs(new_pos.y - input_center_y) > 10:
            print("⚠ UYARI: Mouse hedefe ulaşamadı!")
            print("Manuel olarak mouse'u input field'e getirin ve ENTER'a basın...")
            input("Mouse'u input field'e getirip ENTER'a basın...")
        else:
            print("✓ Mouse hedefe ulaştı")
    except Exception as e:
        print(f"Hata: Mouse hareket ettirilemedi: {e}")
        print("Manuel olarak mouse'u input field'e getirin ve ENTER'a basın...")
        input("Mouse'u input field'e getirip ENTER'a basın...")
    
    print("Tıklama yapılıyor...")
    try:
        pyautogui.click(input_center_x, input_center_y, clicks=2, interval=0.1)
        time.sleep(0.5)
        print("✓ Input field'e tıklandı")
    except Exception as e:
        print(f"Tıklama hatası: {e}")
        print("Manuel tıklama deneniyor...")
        pyautogui.click()
        time.sleep(0.5)
    
    # ADIM 3: Yazma
    print("\n" + "=" * 60)
    print("ADIM 3: NUMARA YAZMA")
    print("=" * 60)
    
    print("Mevcut içerik temizleniyor...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.2)
    
    print(f"Numara yazılıyor: '{number}'")
    simulator.type_numbers(number, 0.1)
    time.sleep(0.5)
    print("✓ Yazma tamamlandı")
    
    # ADIM 4: Confirm
    print("\n" + "=" * 60)
    print("ADIM 4: CONFIRM BUTONUNA TIKLAMA")
    print("=" * 60)
    
    if not confirm_button or confirm_button.get("x") == 0:
        print("Hata: Confirm button koordinatları tanımlı değil!")
        return
    
    confirm_x = confirm_button.get("x", 0)
    confirm_y = confirm_button.get("y", 0)
    confirm_w = confirm_button.get("width", 100)
    confirm_h = confirm_button.get("height", 30)
    confirm_center_x = confirm_x + confirm_w // 2
    confirm_center_y = confirm_y + confirm_h // 2
    
    print(f"Confirm button: ({confirm_x}, {confirm_y}, {confirm_w}x{confirm_h})")
    print(f"Merkez: ({confirm_center_x}, {confirm_center_y})")
    
    print("\n3 saniye sonra confirm butonuna tıklanacak...")
    print("⚠ LÜTFEN OYUN PENCERESİNİN AKTİF OLDUĞUNDAN EMİN OLUN!")
    time.sleep(3)
    
    print("Mouse hareket ettiriliyor...")
    try:
        pyautogui.moveTo(confirm_center_x, confirm_center_y, duration=0.5)
        time.sleep(0.3)
        new_pos = pyautogui.position()
        print(f"Mouse pozisyonu (hareket sonrası): {new_pos}")
        
        if abs(new_pos.x - confirm_center_x) > 10 or abs(new_pos.y - confirm_center_y) > 10:
            print("⚠ UYARI: Mouse hedefe ulaşamadı!")
            print("Manuel olarak mouse'u confirm butonuna getirin ve ENTER'a basın...")
            input("Mouse'u confirm butonuna getirip ENTER'a basın...")
        else:
            print("✓ Mouse hedefe ulaştı")
    except Exception as e:
        print(f"Hata: Mouse hareket ettirilemedi: {e}")
        print("Manuel olarak mouse'u confirm butonuna getirin ve ENTER'a basın...")
        input("Mouse'u confirm butonuna getirip ENTER'a basın...")
    
    print("Tıklama yapılıyor...")
    try:
        pyautogui.click(confirm_center_x, confirm_center_y)
        time.sleep(0.5)
        print("✓ Confirm butonuna tıklandı")
    except Exception as e:
        print(f"Tıklama hatası: {e}")
        print("Manuel tıklama deneniyor...")
        pyautogui.click()
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)


if __name__ == "__main__":
    debug_test()

