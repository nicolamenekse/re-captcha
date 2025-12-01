"""
Sadece Input Field (Captcha Yazılacak Alan) Kalibrasyonu
--------------------------------------------------------
Bu script sadece captcha numarasının yazılacağı input field'in koordinatlarını ayarlar.
"""

import json
import pyautogui
import os


def setup_input_field():
    """Input field koordinatlarını ayarlar"""
    print("=" * 60)
    print("INPUT FIELD KALİBRASYONU")
    print("=" * 60)
    print("\nBu script, captcha numarasının YAZILACAĞI alanın koordinatlarını ayarlar.")
    print("\n⚠ ÖNEMLİ:")
    print("1. Oyun penceresini açın")
    print("2. Captcha ekranına geçin (oyunda 'captcha' yazarak)")
    print("3. Captcha numarasının yazılacağı metin kutusu görünür olmalı")
    print("\n5 saniye içinde hazır olun...\n")
    
    import time
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Config dosyasını yükle
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("⚠ config.json bulunamadı! Önce 'python setup_window.py' çalıştırın.")
        return
    
    if "coordinates" not in config:
        config["coordinates"] = {}
    
    # Input Field Kalibrasyonu
    print("\n[INPUT FIELD] Captcha numarasının yazılacağı alan")
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
    
    # Config'i kaydet
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print(f"\n✓ Input field kaydedildi: ({input_x}, {input_y}, {input_w}x{input_h})")
    print(f"✓ Config dosyası güncellendi: {config_path}")


if __name__ == "__main__":
    setup_input_field()

