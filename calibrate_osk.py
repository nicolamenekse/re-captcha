"""
Ekran Klavyesi (OSK) Kalibrasyon Aracı
--------------------------------------
Bu script SADECE bir kere çalıştırılacak:
- OSK tuşlarının (0–9) ekran koordinatlarını kaydeder
- Sonra bu koordinatları 'osk_calibration.json' içine yazar

Sonrasında:
- Oyun içi otomatik çözücü (auto_solution.py) bu kalibrasyonu kullanır
- Yeniden kalibrasyon gerekmeyene kadar bu scripti tekrar çalıştırmana gerek yok
"""

import time
import pyautogui
from onscreen_keyboard import OnScreenKeyboard


def main():
    print("=" * 60)
    print("OSK KALİBRASYON ARACI (0-9 Sayı Tuşları)")
    print("=" * 60)
    print("\n⚠ ÖNEMLİ ADIMLAR:")
    print("1. Windows Ekran Klavyesi'ni (osk.exe) AÇ ve ekranda görünür bırak.")
    print("2. OSK penceresini hareket ettirme (sabit kalsın).")
    print("3. Bu terminaldeki yönergeleri takip ederek 0–9 tuşlarının ÜZERİNE mouse'u getir.")
    print("4. Her tuş için mouse'u tuşun üstüne getirip terminal'e dön ve ENTER'a bas.")
    print("\nKalibrasyon bittikten sonra bu ayar kaydedilecek ve auto_solution.py bunu kullanacak.")
    print("\nHazırsan 3 saniye içinde başlıyoruz...")

    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    osk = OnScreenKeyboard()

    # OSK'yi bul
    if not osk.find_osk_window():
        print("\n✗ OSK bulunamadı. Lütfen 'Ekran Klavyesi'ni açıp tekrar dene.")
        return

    print("✓ Ekran klavyesi bulundu (manuel açık)")
    
    # Mevcut kalibrasyonu kontrol et
    existing_keys = len(osk.key_positions) if osk.key_positions else 0
    
    if existing_keys > 0:
        print(f"\n⚠ Mevcut kalibrasyon bulundu ({existing_keys} tuş).")
        choice = input("Yeniden kalibre etmek istiyor musunuz? (e/h): ").strip().lower()
        if choice != 'e':
            print("Kalibrasyon atlandı.")
            return
        # Kalibrasyonu sıfırla
        osk.key_positions = {}
        print("Kalibrasyon sıfırlandı, yeni kalibrasyon başlıyor...\n")
    
    # Şimdi kalibrasyonu yap
    print("=== EKRAN KLAVYESİ TUŞ KALİBRASYONU ===")
    print("Lütfen ekran klavyesini görünür ve sabit bir yerde tut.")
    print("Şimdi sırasıyla tuşların ÜZERİNE mouse'u getir ve ENTER'a bas.\n")
    time.sleep(2)

    try:
        # 0-9 sırasıyla
        for digit in range(10):
            key = str(digit)
            print(f"\n[{key}] tuşu için:")
            print(f"  1. Mouse'u OSK'deki '{key}' tuşunun ÜZERİNE getir")
            print(f"  2. Terminal'e dön ve ENTER'a bas")
            input("  Hazır olduğunuzda ENTER'a basın...")
            x, y = pyautogui.position()
            osk.key_positions[key] = (x, y)
            print(f"  ✓ '{key}' tuşu kaydedildi: ({x}, {y})")

        print("\n✓ Tüm tuş pozisyonları kaydedildi.")
        
        # Kalibrasyonu kaydet
        osk._save_calibration()
        
        print("\n✓ Kalibrasyon tamamlandı ve kaydedildi!")
        print("Artık oyun içi otomatik çözüm için doğrudan 'python auto_solution.py' çalıştırabilirsin.")
        
    except Exception as e:
        print(f"\n✗ Kalibrasyon hatası: {e}")
        print("Lütfen tekrar deneyin.")


if __name__ == "__main__":
    main()


