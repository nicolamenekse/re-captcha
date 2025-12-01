"""
Oyun Penceresi ve Koordinat Kurulum Aracı
Oyun penceresini bulur, koordinatları kalibre eder ve config'e kaydeder
"""
import json
import pyautogui
import time
from window_manager import find_game_window, WindowManager


def setup_window():
    """Oyun penceresini bulur, koordinatları kalibre eder ve config'e kaydeder"""
    print("=" * 60)
    print("OYUN PENCERESİ VE KOORDİNAT KURULUMU")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve aktif edin!")
    print("Oyun penceresine geçmeniz için 10 saniye bekleniyor...")
    
    for i in range(10, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nOyun penceresi aranıyor...")
    result = find_game_window()
    
    window_name = None
    if result:
        hwnd, title = result
        window_name = title
        print(f"\n✓ Pencere bulundu: {title}")
    else:
        print("\n⚠ Oyun penceresi otomatik bulunamadı!")
        print("\nManuel olarak pencere adını girebilirsiniz:")
        window_name = input("Pencere adı (boş bırakırsanız 'SeaSRO2025' kullanılacak): ").strip()
        if not window_name:
            window_name = "SeaSRO2025"
    
    # Config'i yükle veya oluştur
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}
    
    if "game_settings" not in config:
        config["game_settings"] = {}
    
    config["game_settings"]["window_name"] = window_name
    
    if "coordinates" not in config:
        config["coordinates"] = {}
    
    print(f"\n✓ Pencere adı kaydedildi: {window_name}")
    
    # Şimdi koordinat kalibrasyonu
    print("\n" + "=" * 60)
    print("KOORDİNAT KALİBRASYONU")
    print("=" * 60)
    print("\nTalimatlar:")
    print("1. Her alan için mouse'u alanın SOL ÜST köşesine getirin")
    print("2. Terminal'e dönüp ENTER'a basın")
    print("3. Sonra SAĞ ALT köşesine getirin ve ENTER'a basın")
    print("\n⚠ ÖNEMLİ: Oyun penceresinde captcha ekranı açık olmalı!")
    print("5 saniye içinde hazır olun...\n")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 1. OCR Alanı
    print("\n[1] OCR ALANI (Büyük numara okuma alanı)")
    print("Mouse'u numara alanının SOL ÜST köşesine getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    ocr_top_left = pyautogui.position()
    print(f"Sol üst: ({ocr_top_left.x}, {ocr_top_left.y})")
    
    print("Şimdi numara alanının SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    ocr_bottom_right = pyautogui.position()
    print(f"Sağ alt: ({ocr_bottom_right.x}, {ocr_bottom_right.y})")
    
    ocr_x = min(ocr_top_left.x, ocr_bottom_right.x)
    ocr_y = min(ocr_top_left.y, ocr_bottom_right.y)
    ocr_w = abs(ocr_bottom_right.x - ocr_top_left.x)
    ocr_h = abs(ocr_bottom_right.y - ocr_top_left.y)
    
    config["coordinates"]["ocr_area"] = {
        "x": ocr_x,
        "y": ocr_y,
        "width": ocr_w,
        "height": ocr_h,
        "description": "1 - Büyük numara okuma alanı (OCR)"
    }
    print(f"✓ OCR alanı kaydedildi: ({ocr_x}, {ocr_y}, {ocr_w}x{ocr_h})")
    
    # 2. Input Field
    print("\n[2] INPUT FIELD (Yazılacak alan)")
    print("Mouse'u input field'in SOL ÜST köşesine getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    input_top_left = pyautogui.position()
    print(f"Sol üst: ({input_top_left.x}, {input_top_left.y})")
    
    print("Şimdi input field'in SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    input_bottom_right = pyautogui.position()
    print(f"Sağ alt: ({input_bottom_right.x}, {input_bottom_right.y})")
    
    input_x = min(input_top_left.x, input_bottom_right.x)
    input_y = min(input_top_left.y, input_bottom_right.y)
    input_w = abs(input_bottom_right.x - input_top_left.x)
    input_h = abs(input_bottom_right.y - input_top_left.y)
    
    config["coordinates"]["input_field"] = {
        "x": input_x,
        "y": input_y,
        "width": input_w,
        "height": input_h,
        "description": "2 - Input field (yazılacak alan)"
    }
    print(f"✓ Input field kaydedildi: ({input_x}, {input_y}, {input_w}x{input_h})")
    
    # 3. Confirm Button
    print("\n[3] CONFIRM BUTONU (Tıklanacak buton)")
    print("Mouse'u confirm butonunun SOL ÜST köşesine getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    confirm_top_left = pyautogui.position()
    print(f"Sol üst: ({confirm_top_left.x}, {confirm_top_left.y})")
    
    print("Şimdi confirm butonunun SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    confirm_bottom_right = pyautogui.position()
    print(f"Sağ alt: ({confirm_bottom_right.x}, {confirm_bottom_right.y})")
    
    confirm_x = min(confirm_top_left.x, confirm_bottom_right.x)
    confirm_y = min(confirm_top_left.y, confirm_bottom_right.y)
    confirm_w = abs(confirm_bottom_right.x - confirm_top_left.x)
    confirm_h = abs(confirm_bottom_right.y - confirm_top_left.y)
    
    config["coordinates"]["confirm_button"] = {
        "x": confirm_x,
        "y": confirm_y,
        "width": confirm_w,
        "height": confirm_h,
        "description": "3 - Confirm butonu (tıklanacak)"
    }
    print(f"✓ Confirm button kaydedildi: ({confirm_x}, {confirm_y}, {confirm_w}x{confirm_h})")
    
    # 4. Captcha Trigger Input (opsiyonel)
    print("\n[4] CAPTCHA TRIGGER INPUT (Chat metin kutusu - Opsiyonel)")
    print("Bu adımı atlamak için ENTER'a basın, devam etmek için 'e' yazıp ENTER'a basın...")
    choice = input("Devam edilsin mi? (e/h): ").strip().lower()
    
    if choice == 'e':
        print("Mouse'u chat metin kutusunun SOL ÜST köşesine getirin...")
        input("Hazır olduğunuzda ENTER'a basın...")
        trigger_top_left = pyautogui.position()
        print(f"Sol üst: ({trigger_top_left.x}, {trigger_top_left.y})")
        
        print("Şimdi chat metin kutusunun SAĞ ALT köşesine mouse'u getirin...")
        input("Hazır olduğunuzda ENTER'a basın...")
        trigger_bottom_right = pyautogui.position()
        print(f"Sağ alt: ({trigger_bottom_right.x}, {trigger_bottom_right.y})")
        
        trigger_x = min(trigger_top_left.x, trigger_bottom_right.x)
        trigger_y = min(trigger_top_left.y, trigger_bottom_right.y)
        trigger_w = abs(trigger_bottom_right.x - trigger_top_left.x)
        trigger_h = abs(trigger_bottom_right.y - trigger_top_left.y)
        
        config["coordinates"]["captcha_trigger_input"] = {
            "x": trigger_x,
            "y": trigger_y,
            "width": trigger_w,
            "height": trigger_h,
            "description": "Captcha tetikleme metin kutusu (oyunda 'captcha' yazılan alan)"
        }
        print(f"✓ Captcha trigger input kaydedildi: ({trigger_x}, {trigger_y}, {trigger_w}x{trigger_h})")
    else:
        print("Captcha trigger input atlandı. Daha sonra 'python setup_captcha_trigger.py' ile ayarlayabilirsiniz.")
    
    # Config'i kaydet
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("✓ TÜM KOORDİNATLAR KAYDEDİLDİ!")
    print("=" * 60)
    print(f"\nConfig dosyası: config.json")
    print("\nÖzet:")
    for key, coord in config["coordinates"].items():
        print(f"  - {coord.get('description', key)}: ({coord['x']}, {coord['y']}, {coord['width']}x{coord['height']})")


if __name__ == "__main__":
    setup_window()

