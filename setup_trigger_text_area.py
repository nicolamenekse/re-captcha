"""
Tetık Yazı Alanı Kurulumu
-------------------------
Bu araç, ekranda BELİRLİ BİR YAZIYI kontrol edeceğimiz alanı config.json'a ekler.

Örnek senaryo:
- Oyunda belli bir uyarı / yazı çıktığında (ör: 'Captcha gerekli'),
- Bu yazı belirlediğiniz bölgede görünüyorsa,
- Script sohbet kutusuna 'captcha' yazıp ENTER basacak,
- Gelen captchayı okuyup numarayı girip confirm'e basacak.

Bu script sadece:
  - coordinates.trigger_text_area
 alanını ayarlar. Diğer koordinatlara dokunmaz.
"""

import json
import os
import time

import pyautogui


def main():
    print("=" * 60)
    print("TETİK YAZI ALANI KURULUMU (trigger_text_area)")
    print("=" * 60)
    print("\nTalimatlar:")
    print("1. 5 saniye içinde OYUN penceresine geç.")
    print("2. Tetik yazının çıkacağı YAZI ekranda görünsün (veya çıkacağı yer boş olsun).")
    print("3. Aşağıdaki adımlarda istenen noktalara mouse'u getirip ENTER'a bas.")
    print("=" * 60)

    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # 1) Sol üst köşe
    print("\n[1] Tetik yazının çıkacağı alanın SOL ÜST köşesi")
    print("Mouse'u bu alanın SOL ÜST köşesine getir.")
    input("Hazırsan ENTER'a bas...")
    top_left = pyautogui.position()
    print(f"Sol üst: ({top_left.x}, {top_left.y})")

    # 2) Sağ alt köşe
    print("\n[2] Tetik yazının çıkacağı alanın SAĞ ALT köşesi")
    print("Mouse'u bu alanın SAĞ ALT köşesine getir.")
    input("Hazırsan ENTER'a bas...")
    bottom_right = pyautogui.position()
    print(f"Sağ alt: ({bottom_right.x}, {bottom_right.y})")

    x = min(top_left.x, bottom_right.x)
    y = min(top_left.y, bottom_right.y)
    w = abs(bottom_right.x - top_left.x)
    h = abs(bottom_right.y - top_left.y)

    print("\nÖZET:")
    print(f"Tetik yazı alanı: ({x}, {y}, {w}x{h})")

    # Config'e yaz
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        if "coordinates" not in config:
            config["coordinates"] = {}

        config["coordinates"]["trigger_text_area"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "description": "Tetik yazının izlendiği alan (trigger_text_area)",
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        print(f"\n✓ Tetik yazı alanı koordinatları kaydedildi: {config_path}")
    except Exception as e:
        print(f"Hata: Koordinatlar kaydedilemedi: {e}")


if __name__ == "__main__":
    main()


