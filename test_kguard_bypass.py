"""
KGuard Bypass Test
Farklı input yöntemlerini test eder
"""
import time
import pyautogui
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

try:
    import win32gui
    import win32con
    import ctypes
    from ctypes import wintypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def test_input_methods():
    """Farklı input yöntemlerini test eder"""
    print("=" * 60)
    print("KGUARD BYPASS TEST")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!")
    print("5 saniye içinde oyun penceresine geçin ve input field'e tıklayın...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    test_text = "1234"
    
    print(f"\nTest edilecek metin: '{test_text}'")
    print("\n" + "=" * 60)
    
    # Yöntem 1: keyboard kütüphanesi (en düşük seviye)
    if KEYBOARD_AVAILABLE:
        print("\n1️⃣ Yöntem 1: keyboard kütüphanesi (en düşük seviye)")
        print("   Bu yöntem gerçek klavye input'larını simüle eder")
        print("   3 saniye içinde input field'e tıklayın...")
        time.sleep(3)
        try:
            keyboard.write(test_text, delay=0.1)
            print("   ✓ keyboard.write() çalıştırıldı")
        except Exception as e:
            print(f"   ✗ Hata: {e}")
        time.sleep(2)
    
    # Yöntem 2: SendInput API (hardware level)
    if WIN32_AVAILABLE:
        print("\n2️⃣ Yöntem 2: SendInput API (hardware level)")
        print("   Bu yöntem Windows API ile hardware input simüle eder")
        print("   3 saniye içinde input field'e tıklayın...")
        time.sleep(3)
        try:
            user32 = ctypes.windll.user32
            PUL = ctypes.POINTER(ctypes.c_ulong)
            
            class KeyBdInput(ctypes.Structure):
                _fields_ = [("wVk", ctypes.c_ushort),
                           ("wScan", ctypes.c_ushort),
                           ("dwFlags", ctypes.c_ulong),
                           ("time", ctypes.c_ulong),
                           ("dwExtraInfo", PUL)]
            
            class Input_I(ctypes.Union):
                _fields_ = [("ki", KeyBdInput)]
            
            class Input(ctypes.Structure):
                _fields_ = [("type", ctypes.c_ulong),
                           ("ii", Input_I)]
            
            for char in test_text:
                if char.isdigit():
                    vk_code = ord(char)
                    extra = ctypes.c_ulong(0)
                    ii_ = Input_I()
                    
                    # KEYDOWN
                    ii_.ki = KeyBdInput(vk_code, 0, 0, 0, ctypes.pointer(extra))
                    x = Input(ctypes.c_ulong(1), ii_)
                    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                    time.sleep(0.05)
                    
                    # KEYUP
                    ii_.ki = KeyBdInput(vk_code, 0, 2, 0, ctypes.pointer(extra))
                    x = Input(ctypes.c_ulong(1), ii_)
                    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                    time.sleep(0.1)
            
            print("   ✓ SendInput API çalıştırıldı")
        except Exception as e:
            print(f"   ✗ Hata: {e}")
        time.sleep(2)
    
    # Yöntem 3: PyAutoGUI (fallback)
    print("\n3️⃣ Yöntem 3: PyAutoGUI")
    print("   Bu yöntem standart input simülasyonu yapar")
    print("   3 saniye içinde input field'e tıklayın...")
    time.sleep(3)
    try:
        original_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        pyautogui.write(test_text, interval=0.1)
        pyautogui.FAILSAFE = original_failsafe
        print("   ✓ PyAutoGUI çalıştırıldı")
    except Exception as e:
        print(f"   ✗ Hata: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nOyun penceresinde kontrol edin:")
    print("1. Hangi yöntem çalıştı? (input field'de '1234' yazıldı mı?)")
    print("2. Hiçbiri çalışmadıysa, KGuard input'ları engelliyor olabilir")
    print("\nÇözüm önerileri:")
    print("- Oyunu yönetici olarak çalıştırmayı deneyin")
    print("- KGuard ayarlarını kontrol edin")
    print("- Oyun ayarlarında 'Raw Input' seçeneğini kapatın/açın")


if __name__ == "__main__":
    test_input_methods()

