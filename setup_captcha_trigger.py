"""
Captcha Tetikleme Metin Kutusu Kurulumu
---------------------------------------
Bu araç, oyunda "captcha" yazacağın metin kutusunun koordinatlarını config.json'a ekler.

Mevcut:
  - coordinates.ocr_area
  - coordinates.input_field
  - coordinates.confirm_button

Yeni eklenecek:
  - coordinates.captcha_trigger_input
"""

import json
import time
import pyautogui
import os


def main():
    print("=" * 60)
    print("CAPTCHA TETİKLEME METİN KUTUSU KURULUMU")
    print("=" * 60)
    print("\nTalimatlar:")
    print("1. 5 saniye içinde OYUN penceresine geç.")
    print("2. 'captcha' yazdığın METİN KUTUSU ekranda görünsün.")
    print("3. Aşağıdaki adımlarda istenen noktalara mouse'u getirip ENTER'a bas.")
    print("=" * 60)

    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # Sol üst köşe
    print("\n[1] CHAT METİN KUTUSU (Captcha tetikleme alanı)")
    print("Mouse'u chat metin kutusunun SOL ÜST köşesine getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    top_left = pyautogui.position()
    print(f"Sol üst: ({top_left.x}, {top_left.y})")

    # Sağ alt köşe
    print("Şimdi chat metin kutusunun SAĞ ALT köşesine mouse'u getirin...")
    input("Hazır olduğunuzda ENTER'a basın...")
    bottom_right = pyautogui.position()
    print(f"Sağ alt: ({bottom_right.x}, {bottom_right.y})")

    x = min(top_left.x, bottom_right.x)
    y = min(top_left.y, bottom_right.y)
    w = abs(bottom_right.x - top_left.x)
    h = abs(bottom_right.y - top_left.y)

    print("\nÖZET:")
    print(f"Metin kutusu alanı: ({x}, {y}, {w}x{h})")

    # Config'e yaz
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        coords = config.get("coordinates", {})
        coords["captcha_trigger_input"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "description": "Captcha tetikleme metin kutusu (oyunda 'captcha' yazılan alan)"
        }

        config["coordinates"] = coords

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        print(f"\n✓ Koordinatlar kaydedildi: {config_path}")
    except Exception as e:
        print(f"\n✗ Config yazma hatası: {e}")


if __name__ == "__main__":
    main()


