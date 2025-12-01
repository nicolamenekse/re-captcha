"""
Mouse Testi - Mouse hareketinin çalışıp çalışmadığını test eder
"""
import pyautogui
import time


def test_mouse():
    """Mouse hareketini test eder"""
    print("=" * 60)
    print("MOUSE HAREKET TESTİ")
    print("=" * 60)
    
    print("\nBu test mouse'un hareket edip etmediğini kontrol edecek.")
    print("Mouse ekranın köşelerine hareket edecek.")
    print("\n⚠ DİKKAT: FAILSAFE kapalı olacak!")
    print("Mouse köşeye götürünce durmaz!")
    
    confirm = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
    if confirm != 'e':
        print("Test iptal edildi.")
        return
    
    print("\n5 saniye içinde hazır olun...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # FAILSAFE'i kapat
    original_failsafe = pyautogui.FAILSAFE
    pyautogui.FAILSAFE = False
    
    try:
        # Mevcut pozisyon
        start_pos = pyautogui.position()
        print(f"\nBaşlangıç pozisyonu: {start_pos}")
        
        # Ekran boyutu
        screen_width, screen_height = pyautogui.size()
        print(f"Ekran boyutu: {screen_width}x{screen_height}")
        
        # Test noktaları
        test_points = [
            (100, 100, "Sol üst"),
            (screen_width - 100, 100, "Sağ üst"),
            (screen_width - 100, screen_height - 100, "Sağ alt"),
            (100, screen_height - 100, "Sol alt"),
            (screen_width // 2, screen_height // 2, "Merkez")
        ]
        
        for x, y, name in test_points:
            print(f"\n{name} noktasına hareket ediliyor: ({x}, {y})")
            pyautogui.moveTo(x, y, duration=1.0)
            time.sleep(0.5)
            
            current_pos = pyautogui.position()
            print(f"Mevcut pozisyon: {current_pos}")
            
            if abs(current_pos.x - x) < 5 and abs(current_pos.y - y) < 5:
                print(f"✓ {name} noktasına ulaşıldı!")
            else:
                print(f"⚠ {name} noktasına ulaşılamadı!")
                print(f"  Hedef: ({x}, {y})")
                print(f"  Gerçek: ({current_pos.x}, {current_pos.y})")
        
        # Başlangıç pozisyonuna dön
        print(f"\nBaşlangıç pozisyonuna dönülüyor: {start_pos}")
        pyautogui.moveTo(start_pos.x, start_pos.y, duration=1.0)
        time.sleep(0.5)
        
        final_pos = pyautogui.position()
        print(f"Son pozisyon: {final_pos}")
        
        print("\n" + "=" * 60)
        print("TEST TAMAMLANDI")
        print("=" * 60)
        
        if abs(final_pos.x - start_pos.x) < 5 and abs(final_pos.y - start_pos.y) < 5:
            print("✓ Mouse hareketi çalışıyor!")
        else:
            print("⚠ Mouse hareketi sorunlu olabilir!")
    
    finally:
        # FAILSAFE'i geri aç
        pyautogui.FAILSAFE = original_failsafe
        print(f"\nFAILSAFE geri açıldı: {pyautogui.FAILSAFE}")


if __name__ == "__main__":
    test_mouse()

