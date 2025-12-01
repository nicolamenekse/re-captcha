"""
Input Yöntemleri Test Aracı
Farklı input yöntemlerini test eder ve hangisinin çalıştığını bulur
"""
import time
import pyautogui
import json
try:
    import win32gui
    import win32con
    import ctypes
    from ctypes import wintypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def find_child_windows(parent_hwnd):
    """Pencere içindeki child window'ları bulur"""
    if not WIN32_AVAILABLE:
        return []
    
    child_windows = []
    
    def enum_child_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            window_text = win32gui.GetWindowText(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            child_windows.append({
                'hwnd': hwnd,
                'class': class_name,
                'text': window_text,
                'rect': rect
            })
        return True
    
    try:
        win32gui.EnumChildWindows(parent_hwnd, enum_child_proc, None)
    except:
        pass
    
    return child_windows


def test_input_methods():
    """Farklı input yöntemlerini test eder"""
    print("=" * 60)
    print("INPUT YÖNTEMLERİ TEST ARACI")
    print("=" * 60)
    
    # Config yükle
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Hata: config.json bulunamadı!")
        return
    
    coordinates = config.get("coordinates", {})
    input_field = coordinates.get("input_field", {})
    confirm_button = coordinates.get("confirm_button", {})
    game_settings = config.get("game_settings", {})
    window_name = game_settings.get("window_name", "")
    
    if not window_name:
        print("Hata: Oyun penceresi adı config'de yok!")
        return
    
    # Pencereyi bul
    if not WIN32_AVAILABLE:
        print("Win32 modülleri bulunamadı!")
        return
    
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
    
    # Child window'ları bul
    print("\nChild window'lar aranıyor...")
    child_windows = find_child_windows(hwnd)
    print(f"Bulunan child window sayısı: {len(child_windows)}")
    
    for i, child in enumerate(child_windows[:10], 1):  # İlk 10'u göster
        print(f"  {i}. Class: {child['class']}, Text: {child['text']}, Rect: {child['rect']}")
    
    # Pencereye odaklan
    print("\nPencereye odaklanılıyor...")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # Test 1: Input field koordinatları
    if input_field and input_field.get("x") != 0:
        input_x = input_field.get("x", 0)
        input_y = input_field.get("y", 0)
        input_w = input_field.get("width", 200)
        input_h = input_field.get("height", 30)
        input_center_x = input_x + input_w // 2
        input_center_y = input_y + input_h // 2
        
        print("\n" + "=" * 60)
        print("TEST 1: INPUT FIELD TIKLAMA")
        print("=" * 60)
        print(f"Koordinatlar: ({input_center_x}, {input_center_y})")
        
        # Client rect al
        try:
            client_rect = win32gui.GetClientRect(hwnd)
            client_point = win32gui.ClientToScreen(hwnd, (0, 0))
            screen_x = client_point[0] + input_center_x
            screen_y = client_point[1] + input_center_y
            print(f"Ekran koordinatları: ({screen_x}, {screen_y})")
        except:
            screen_x, screen_y = input_center_x, input_center_y
        
        print("\n5 saniye içinde hazır olun...")
        time.sleep(5)
        
        # Yöntem 1: Pyautogui
        print("\nYöntem 1: Pyautogui ile tıklama...")
        original_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(screen_x, screen_y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click(screen_x, screen_y)
            print("✓ Pyautogui tıklama yapıldı")
        except Exception as e:
            print(f"✗ Pyautogui hatası: {e}")
        finally:
            pyautogui.FAILSAFE = original_failsafe
        
        time.sleep(1)
        
        # Yöntem 2: SendInput
        print("\nYöntem 2: SendInput API ile tıklama...")
        try:
            user32 = ctypes.windll.user32
            user32.SetCursorPos(int(screen_x), int(screen_y))
            time.sleep(0.1)
            
            # SendInput structure
            PUL = ctypes.POINTER(ctypes.c_ulong)
            
            class MouseInput(ctypes.Structure):
                _fields_ = [("dx", ctypes.c_long),
                           ("dy", ctypes.c_long),
                           ("mouseData", ctypes.c_ulong),
                           ("dwFlags", ctypes.c_ulong),
                           ("time", ctypes.c_ulong),
                           ("dwExtraInfo", PUL)]
            
            class Input_I(ctypes.Union):
                _fields_ = [("mi", MouseInput)]
            
            class Input(ctypes.Structure):
                _fields_ = [("type", ctypes.c_ulong),
                           ("ii", Input_I)]
            
            # MOUSEDOWN
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            time.sleep(0.05)
            
            # MOUSEUP
            ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            print("✓ SendInput tıklama yapıldı")
        except Exception as e:
            print(f"✗ SendInput hatası: {e}")
        
        time.sleep(2)
        
        # Test 2: Yazma
        print("\n" + "=" * 60)
        print("TEST 2: YAZMA")
        print("=" * 60)
        test_number = "1234"
        print(f"Test numarası: '{test_number}'")
        
        print("\n5 saniye içinde hazır olun...")
        time.sleep(5)
        
        # Yöntem 1: Pyautogui
        print("\nYöntem 1: Pyautogui ile yazma...")
        original_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        try:
            pyautogui.write(test_number, interval=0.1)
            print("✓ Pyautogui yazma yapıldı")
        except Exception as e:
            print(f"✗ Pyautogui hatası: {e}")
        finally:
            pyautogui.FAILSAFE = original_failsafe
        
        time.sleep(2)
        
        # Yöntem 2: SendInput
        print("\nYöntem 2: SendInput API ile yazma...")
        try:
            user32 = ctypes.windll.user32
            
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
            
            for char in test_number:
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
            
            print("✓ SendInput yazma yapıldı")
        except Exception as e:
            print(f"✗ SendInput hatası: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nLütfen oyun penceresinde kontrol edin:")
    print("1. Input field'e tıklama çalıştı mı?")
    print("2. Yazma çalıştı mı?")
    print("3. Hangi yöntem çalıştı?")


if __name__ == "__main__":
    test_input_methods()

