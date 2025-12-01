"""
Koordinat Kurulum Aracı
Görselden veya manuel olarak koordinatları belirleme
"""
import json
import pyautogui
import time


def get_coordinates_interactive():
    """İnteraktif koordinat belirleme"""
    print("=" * 60)
    print("KOORDİNAT KURULUM ARACI")
    print("=" * 60)
    print("\nTalimatlar:")
    print("1. Oyun penceresine geçin")
    print("2. Her alan için mouse'u alanın merkezine getirin")
    print("3. Buraya dönüp ENTER'a basın")
    print("=" * 60)
    
    coordinates = {}
    
    # 1. OCR Alanı (Büyük numara)
    print("\n[1] OCR ALANI (Büyük numara okuma alanı)")
    print("Mouse'u büyük numaranın merkezine getirin ve ENTER'a basın...")
    input("Hazır olduğunuzda ENTER'a basın...")
    ocr_center = pyautogui.position()
    print(f"Merkez: ({ocr_center.x}, {ocr_center.y})")
    
    print("Şimdi numara alanının SOL ÜST köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    ocr_top_left = pyautogui.position()
    
    print("Şimdi numara alanının SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    ocr_bottom_right = pyautogui.position()
    
    ocr_x = min(ocr_top_left.x, ocr_bottom_right.x)
    ocr_y = min(ocr_top_left.y, ocr_bottom_right.y)
    ocr_w = abs(ocr_bottom_right.x - ocr_top_left.x)
    ocr_h = abs(ocr_bottom_right.y - ocr_top_left.y)
    
    coordinates["ocr_area"] = {
        "x": ocr_x,
        "y": ocr_y,
        "width": ocr_w,
        "height": ocr_h,
        "description": "1 - Büyük numara okuma alanı (OCR)"
    }
    print(f"✓ OCR alanı: ({ocr_x}, {ocr_y}, {ocr_w}x{ocr_h})")
    
    # 2. Input Field
    print("\n[2] INPUT FIELD (Yazılacak alan)")
    print("Mouse'u input field'in merkezine getirin ve ENTER'a basın...")
    input("Hazır olduğunuzda ENTER'a basın...")
    input_center = pyautogui.position()
    
    print("Şimdi input field'in SOL ÜST köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    input_top_left = pyautogui.position()
    
    print("Şimdi input field'in SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    input_bottom_right = pyautogui.position()
    
    input_x = min(input_top_left.x, input_bottom_right.x)
    input_y = min(input_top_left.y, input_bottom_right.y)
    input_w = abs(input_bottom_right.x - input_top_left.x)
    input_h = abs(input_bottom_right.y - input_top_left.y)
    
    coordinates["input_field"] = {
        "x": input_x,
        "y": input_y,
        "width": input_w,
        "height": input_h,
        "description": "2 - Input field (yazılacak alan)"
    }
    print(f"✓ Input field: ({input_x}, {input_y}, {input_w}x{input_h})")
    
    # 3. Confirm Button
    print("\n[3] CONFIRM BUTONU (Tıklanacak buton)")
    print("Mouse'u confirm butonunun merkezine getirin ve ENTER'a basın...")
    input("Hazır olduğunuzda ENTER'a basın...")
    confirm_center = pyautogui.position()
    
    print("Şimdi confirm butonunun SOL ÜST köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    confirm_top_left = pyautogui.position()
    
    print("Şimdi confirm butonunun SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    confirm_bottom_right = pyautogui.position()
    
    confirm_x = min(confirm_top_left.x, confirm_bottom_right.x)
    confirm_y = min(confirm_top_left.y, confirm_bottom_right.y)
    confirm_w = abs(confirm_bottom_right.x - confirm_top_left.x)
    confirm_h = abs(confirm_bottom_right.y - confirm_top_left.y)
    
    coordinates["confirm_button"] = {
        "x": confirm_x,
        "y": confirm_y,
        "width": confirm_w,
        "height": confirm_h,
        "description": "3 - Confirm butonu (tıklanacak)"
    }
    print(f"✓ Confirm button: ({confirm_x}, {confirm_y}, {confirm_w}x{confirm_h})")
    
    return coordinates


def save_coordinates(coordinates, config_path="config.json"):
    """Koordinatları config dosyasına kaydeder"""
    try:
        # Mevcut config'i yükle
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        
        # Koordinatları güncelle
        config["coordinates"] = coordinates
        
        # Kaydet
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"\n✓ Koordinatlar kaydedildi: {config_path}")
        return True
    
    except Exception as e:
        print(f"Hata: Koordinatlar kaydedilemedi: {e}")
        return False


def main():
    """Ana program"""
    print("\nKoordinat kurulum aracı başlatılıyor...")
    print("5 saniye içinde oyun penceresine geçin!\n")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    coordinates = get_coordinates_interactive()
    
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    for key, coord in coordinates.items():
        print(f"{coord['description']}: ({coord['x']}, {coord['y']}, {coord['width']}x{coord['height']})")
    
    save = input("\nKoordinatları kaydetmek ister misiniz? (e/h): ").strip().lower()
    if save == 'e':
        save_coordinates(coordinates)
        print("\n✓ Kurulum tamamlandı!")
    else:
        print("\nKoordinatlar kaydedilmedi.")


if __name__ == "__main__":
    main()

