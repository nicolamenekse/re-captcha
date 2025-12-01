"""
Oyun Penceresi Durumu Testi
Pencere durumunu ve input kabul edip etmediğini test eder
"""
import time
import pyautogui
import json
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def test_window_state():
    """Oyun penceresi durumunu test eder"""
    print("=" * 60)
    print("OYUN PENCERESİ DURUMU TESTİ")
    print("=" * 60)
    
    # Config yükle
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Hata: config.json bulunamadı!")
        return
    
    game_settings = config.get("game_settings", {})
    window_name = game_settings.get("window_name", "")
    
    if not WIN32_AVAILABLE:
        print("Win32 modülleri bulunamadı!")
        return
    
    # Pencereyi bul
    def find_window_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_name.lower() in window_text.lower():
                windows.append((hwnd, window_text))
    
    windows = []
    win32gui.EnumWindows(find_window_callback, windows)
    
    if not windows:
        print(f"Pencere bulunamadı: {window_name}")
        return
    
    hwnd, title = windows[0]
    print(f"✓ Pencere bulundu: {title}")
    
    # Pencere durumunu kontrol et
    print("\nPencere durumu kontrol ediliyor...")
    
    # Pencere boyutları
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    
    print(f"Window rect: {window_rect}")
    print(f"Client rect: {client_rect}")
    
    # Pencere durumu
    is_minimized = win32gui.IsIconic(hwnd)
    # IsZoomed yerine GetWindowPlacement kullan
    try:
        placement = win32gui.GetWindowPlacement(hwnd)
        is_maximized = (placement[1] == win32con.SW_SHOWMAXIMIZED)
    except:
        is_maximized = False
    
    print(f"Minimized: {is_minimized}")
    print(f"Maximized: {is_maximized}")
    
    # Aktif pencere mi?
    active_hwnd = win32gui.GetForegroundWindow()
    is_active = (active_hwnd == hwnd)
    print(f"Aktif pencere: {is_active}")
    
    # Pencereye odaklan
    print("\nPencereye odaklanılıyor...")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.2)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.3)
        
        # Tekrar kontrol et
        active_hwnd = win32gui.GetForegroundWindow()
        is_active = (active_hwnd == hwnd)
        print(f"Odaklanma sonrası aktif: {is_active}")
    except Exception as e:
        print(f"Odaklanma hatası: {e}")
    
    # Test: Basit bir tuş gönder
    print("\n" + "=" * 60)
    print("BASIT TUŞ TESTİ")
    print("=" * 60)
    print("Oyun penceresine '1' tuşu gönderilecek...")
    print("5 saniye içinde oyun penceresine geçin...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Pencereye odaklan
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    # Test 1: Pyautogui
    print("\nTest 1: Pyautogui ile '1' yazılıyor...")
    original_failsafe = pyautogui.FAILSAFE
    pyautogui.FAILSAFE = False
    try:
        pyautogui.write('1', interval=0.1)
        print("✓ Pyautogui ile yazıldı")
    except Exception as e:
        print(f"✗ Pyautogui hatası: {e}")
    finally:
        pyautogui.FAILSAFE = original_failsafe
    
    time.sleep(1)
    
    # Test 2: SendInput
    print("\nTest 2: SendInput API ile '2' yazılıyor...")
    try:
        import ctypes
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
        
        vk_code = ord('2')
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(vk_code, 0, 0, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(0.05)
        ii_.ki = KeyBdInput(vk_code, 0, 2, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        print("✓ SendInput ile yazıldı")
    except Exception as e:
        print(f"✗ SendInput hatası: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nOyun penceresinde kontrol edin:")
    print("1. '1' veya '2' yazıldı mı?")
    print("2. Hangi yöntem çalıştı?")
    print("3. Pencere aktif mi?")


if __name__ == "__main__":
    test_window_state()

