"""
Tam Akış Testi
OCR -> Input tıkla -> Yaz -> Confirm tıkla
"""
import time
from recaptcha_solver import ReCaptchaSolver


def test_full_flow():
    """Tam akışı test eder"""
    print("=" * 60)
    print("TAM AKIŞ TESTİ")
    print("=" * 60)
    print("\nBu test şunları yapacak:")
    print("1. OCR ile numara okuyacak")
    print("2. Input field'e tıklayacak")
    print("3. Numarayı yazacak")
    print("4. Confirm butonuna tıklayacak")
    print("\n" + "=" * 60)
    
    print("\n⚠ DİKKAT: Bu test gerçek işlem yapacak!")
    print("Oyun penceresinde captcha görünür olmalı.")
    
    confirm = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
    if confirm != 'e':
        print("Test iptal edildi.")
        return
    
    print("\n5 saniye içinde oyun penceresine geçin...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Çözücüyü başlat
    solver = ReCaptchaSolver()
    
    # Tek seferlik çözüm
    print("\nTest başlıyor...\n")
    result = solver.solve_once(wait_before=0.5)
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    
    if result:
        print(f"✓ İşlem başarılı! Okunan numara: '{result}'")
    else:
        print("⚠ İşlem başarısız veya numara okunamadı.")
        print("\nKontrol edin:")
        print("1. OCR testini çalıştırın: python test_ocr.py")
        print("2. Koordinatların doğru olduğundan emin olun")
        print("3. Oyun penceresinin görünür olduğundan emin olun")


if __name__ == "__main__":
    test_full_flow()

