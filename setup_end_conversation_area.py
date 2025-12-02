"""
End Conversation Alanı Kurulumu
-------------------------------
Bu araç, oyunda "End conversation" yazan buton/seçeneğin olduğu alanı config.json'a ekler.

Bu alan, captcha başarıyla çözüldükten sonra 5 dakikalık bekleme süresi içinde
belirli aralıklarla kontrol edilip, gerekiyorsa tıklanacaktır.

Bu script sadece:
  - coordinates.end_conversation_area
alanını ayarlar. Diğer koordinatlara dokunmaz.
"""

import json
import os
import time

import pyautogui


def main():
    print("=" * 60)
    print("END CONVERSATION ALANI KURULUMU (end_conversation_area)")
    print("=" * 60)
    print("\nTalimatlar:")
    print("1. 5 saniye içinde OYUN penceresine geç.")
    print("2. NPC ile konuşma penceresinde 'End conversation' seçeneği GÖRÜNSÜN.")
    print("3. Aşağıdaki adımlarda istenen noktalara mouse'u getirip ENTER'a bas.")
    print("=" * 60)

    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # 1) Sol üst köşe
    print("\n[1] 'End conversation' alanının SOL ÜST köşesi")
    print("Mouse'u bu seçeneğin SOL ÜST köşesine getir.")
    input("Hazırsan ENTER'a bas...")
    top_left = pyautogui.position()
    print(f"Sol üst: ({top_left.x}, {top_left.y})")

    # 2) Sağ alt köşe
    print("\n[2] 'End conversation' alanının SAĞ ALT köşesi")
    print("Mouse'u bu seçeneğin SAĞ ALT köşesine getir.")
    input("Hazırsan ENTER'a bas...")
    bottom_right = pyautogui.position()
    print(f"Sağ alt: ({bottom_right.x}, {bottom_right.y})")

    x = min(top_left.x, bottom_right.x)
    y = min(top_left.y, bottom_right.y)
    w = abs(bottom_right.x - top_left.x)
    h = abs(bottom_right.y - top_left.y)

    print("\nÖZET:")
    print(f"End conversation alanı: ({x}, {y}, {w}x{h})")

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

        config["coordinates"]["end_conversation_area"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "description": "NPC penceresindeki 'End conversation' seçeneği alanı",
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        print(f"\n✓ End conversation alanı koordinatları kaydedildi: {config_path}")
    except Exception as e:
        print(f"Hata: Koordinatlar kaydedilemedi: {e}")


if __name__ == "__main__":
    main()


