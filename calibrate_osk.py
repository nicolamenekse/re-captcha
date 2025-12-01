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

    # OSK'yi bulur; kalibrasyon eksikse seni zaten sorularla yönlendirecek ve kaydedecek
    if not osk.start_osk():
        print("\n✗ OSK bulunamadı. Lütfen 'Ekran Klavyesi'ni açıp tekrar dene.")
        return

    # Eğer kalibrasyon zaten varsa, kullanıcıya bilgi ver
    if osk.key_positions:
        print(f"\n✓ Mevcut kalibrasyon bulundu ({len(osk.key_positions)} tuş).")
        print("Yeniden kalibre etmek istiyorsanız, 'osk_calibration.json' dosyasını silip tekrar çalıştırın.")
    else:
        print("\n✓ Kalibrasyon tamamlandı (ve kaydedildi).")
    
    print("\nArtık oyun içi otomatik çözüm için doğrudan 'python auto_solution.py' çalıştırabilirsin.")


if __name__ == "__main__":
    main()


