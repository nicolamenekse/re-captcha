"""
Belirli OSK tuşlarını (harf/rakam) kalibre etme aracı.

Önceden:
  - 'calibrate_osk.py' ile 0–9 rakamlarını kaydetmiştik.

Şimdi:
  - Özellikle 'captcha' kelimesi için gerekli harfleri (c, a, p, t, h)
    kalibre edeceğiz ve mevcut 'osk_calibration.json' içine ekleyeceğiz.

Kullanım:
  1. Windows Ekran Klavyesi'ni (osk.exe) AÇ ve ekranda görünür bırak.
  2. Bu scripti çalıştır:
       python calibrate_osk_keys.py
  3. İstenen her tuş için mouse'u OSK üzerindeki o tuşun ÜZERİNE getir,
     sayım bitince pozisyon otomatik kaydedilecek.
"""

import time
import pyautogui
from onscreen_keyboard import OnScreenKeyboard


def main():
    print("=" * 60)
    print("OSK TUŞ KALİBRASYONU (HARF/Rakam)")
    print("=" * 60)
    print("\nBu araç özellikle 'captcha' kelimesi için gerekli harfleri kalibre eder.")
    print("Lütfen:")
    print("  1) Windows Ekran Klavyesi'ni (osk.exe) aç ve görünür bırak.")
    print("  2) OSK penceresini hareket ettirme (sabit kalsın).")
    print("  3) Aşağıdaki yönergelerde istenen tuşların ÜZERİNE mouse'u getir.")
    print("")

    osk = OnScreenKeyboard()

    if not osk.start_osk():
        print("\n✗ OSK bulunamadı. Lütfen ekran klavyesini açıp tekrar dene.")
        return

    # 'captcha' kelimesi için gereken benzersiz karakterler + ENTER tuşu
    keys_to_calibrate = ['c', 'a', 'p', 't', 'h', 'enter']

    print("\nAşağıdaki tuşlar için sırayla pozisyon kaydedeceğiz:")
    print("  " + ", ".join(keys_to_calibrate))
    time.sleep(1)

    for key in keys_to_calibrate:
        label = "ENTER" if key == "enter" else key.upper()
        print(f"\n[{key}] tuşu için:")
        print(f"  1. Mouse'u OSK üzerindeki '{label}' tuşunun ÜZERİNE getir")
        print(f"  2. Terminal'e dön ve ENTER'a bas")
        input("  Hazır olduğunuzda ENTER'a basın...")
        x, y = pyautogui.position()
        osk.key_positions[key] = (x, y)
        print(f"  ✓ '{key}' tuşu kaydedildi: ({x}, {y})")

    # Mevcut kalibrasyonu kaydet
    # (OnScreenKeyboard içindeki private metoda erişiyoruz; Python için sorun değil)
    try:
        osk._save_calibration()
    except Exception as e:
        print(f"Kalibrasyon kaydetme hatası: {e}")
        return

    print("\n✓ Tüm gerekli tuşlar kalibre edildi ve kaydedildi.")
    print("Artık 'OnScreenKeyboardAuto' ile 'captcha' kelimesini OSK üzerinden yazabiliriz.")


if __name__ == "__main__":
    main()


