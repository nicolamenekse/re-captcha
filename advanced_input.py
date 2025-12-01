"""
Gelişmiş Input Yöntemleri
Arduino gelene kadar denenebilecek alternatif yöntemler
"""
import time
import ctypes
from ctypes import wintypes
import pyautogui

try:
    import win32gui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class AdvancedInput:
    """Gelişmiş input yöntemleri - KGuard bypass denemeleri"""
    
    def __init__(self, hwnd=None):
        self.hwnd = hwnd
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
    def method_1_raw_input(self, text):
        """
        Yöntem 1: Raw Input API
        En düşük seviye Windows input API'si
        KGuard'ı atlatabilir
        """
        if not WIN32_AVAILABLE:
            return False
        
        try:
            print("🔹 Yöntem 1: Raw Input API deneniyor...")
            
            # Raw Input için gerekli yapılar
            RIDEV_INPUTSINK = 0x00000100
            RID_INPUT = 0x10000003
            
            class RAWINPUTHEADER(ctypes.Structure):
                _fields_ = [
                    ("dwType", wintypes.DWORD),
                    ("dwSize", wintypes.DWORD),
                    ("hDevice", wintypes.HANDLE),
                    ("wParam", wintypes.WPARAM)
                ]
            
            class RAWKEYBOARD(ctypes.Structure):
                _fields_ = [
                    ("MakeCode", wintypes.USHORT),
                    ("Flags", wintypes.USHORT),
                    ("Reserved", wintypes.USHORT),
                    ("VKey", wintypes.USHORT),
                    ("Message", wintypes.UINT),
                    ("ExtraInformation", wintypes.ULONG)
                ]
            
            class RAWINPUT(ctypes.Structure):
                _fields_ = [
                    ("header", RAWINPUTHEADER),
                    ("keyboard", RAWKEYBOARD)
                ]
            
            # Her karakter için raw input gönder
            for char in text:
                if char.isdigit():
                    vk_code = ord(char)
                    make_code = self.user32.MapVirtualKeyW(vk_code, 0)
                    
                    # Raw input gönder
                    raw_input = RAWINPUT()
                    raw_input.header.dwType = RID_INPUT
                    raw_input.header.dwSize = ctypes.sizeof(RAWINPUT)
                    raw_input.keyboard.MakeCode = make_code
                    raw_input.keyboard.VKey = vk_code
                    raw_input.keyboard.Message = win32con.WM_KEYDOWN
                    
                    # SendInput ile raw input gönder
                    result = self.user32.SendInput(
                        1,
                        ctypes.byref(raw_input),
                        ctypes.sizeof(RAWINPUT)
                    )
                    
                    time.sleep(0.05)
            
            print("✓ Raw Input API tamamlandı")
            return True
        except Exception as e:
            print(f"✗ Raw Input hatası: {e}")
            return False
    
    def method_2_directinput(self, text):
        """
        Yöntem 2: DirectInput Simulation
        Oyunlar DirectInput kullanır, bu yöntem daha etkili olabilir
        """
        if not WIN32_AVAILABLE:
            return False
        
        try:
            print("🔹 Yöntem 2: DirectInput Simulation deneniyor...")
            
            # DirectInput benzeri input gönderme
            # DirectInput genellikle SendInput'u kullanır ama farklı parametrelerle
            
            PUL = ctypes.POINTER(ctypes.c_ulong)
            
            class KeyBdInput(ctypes.Structure):
                _fields_ = [
                    ("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)
                ]
            
            class Input_I(ctypes.Union):
                _fields_ = [("ki", KeyBdInput)]
            
            class Input(ctypes.Structure):
                _fields_ = [
                    ("type", ctypes.c_ulong),
                    ("ii", Input_I)
                ]
            
            # KEYEVENTF_SCANCODE flag'i ile (DirectInput benzeri)
            KEYEVENTF_SCANCODE = 0x0008
            
            for char in text:
                if char.isdigit():
                    vk_code = ord(char)
                    scan_code = self.user32.MapVirtualKeyW(vk_code, 0)
                    
                    extra = ctypes.c_ulong(0)
                    ii_ = Input_I()
                    
                    # KEYDOWN (scan code ile)
                    ii_.ki = KeyBdInput(
                        0,  # wVk = 0 (scan code kullanıyoruz)
                        scan_code,
                        KEYEVENTF_SCANCODE,  # Scan code flag
                        0,
                        ctypes.pointer(extra)
                    )
                    x = Input(ctypes.c_ulong(1), ii_)
                    self.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                    time.sleep(0.02)
                    
                    # KEYUP
                    ii_.ki = KeyBdInput(
                        0,
                        scan_code,
                        KEYEVENTF_SCANCODE | 0x0002,  # KEYUP flag
                        0,
                        ctypes.pointer(extra)
                    )
                    x = Input(ctypes.c_ulong(1), ii_)
                    self.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                    time.sleep(0.05)
            
            print("✓ DirectInput Simulation tamamlandı")
            return True
        except Exception as e:
            print(f"✗ DirectInput hatası: {e}")
            return False
    
    def method_3_window_message_advanced(self, text):
        """
        Yöntem 3: Gelişmiş Window Message Yöntemleri
        Farklı mesaj türleri ve parametreler
        """
        if not WIN32_AVAILABLE or not self.hwnd:
            return False
        
        try:
            print("🔹 Yöntem 3: Gelişmiş Window Message deneniyor...")
            
            # Child window'ları bul
            child_windows = []
            def enum_child_proc(child_hwnd, lParam):
                if win32gui.IsWindowVisible(child_hwnd):
                    class_name = win32gui.GetClassName(child_hwnd)
                    window_text = win32gui.GetWindowText(child_hwnd)
                    # Edit, Static, vb. kontrol sınıfları
                    if any(x in class_name.lower() for x in ['edit', 'static', 'button']):
                        child_windows.append((child_hwnd, class_name, window_text))
                return True
            
            win32gui.EnumChildWindows(self.hwnd, enum_child_proc, None)
            print(f"  {len(child_windows)} child window bulundu")
            
            for char in text:
                if char.isdigit():
                    char_code = ord(char)
                    vk_code = ord(char.upper())
                    
                    # Her child window'a farklı mesajlar gönder
                    for child_hwnd, class_name, window_text in child_windows:
                        try:
                            # 1. WM_CHAR (standart)
                            win32gui.SendMessage(child_hwnd, win32con.WM_CHAR, char_code, 0)
                            time.sleep(0.01)
                            
                            # 2. WM_KEYDOWN + WM_KEYUP (ayrı ayrı)
                            win32gui.SendMessage(child_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                            time.sleep(0.01)
                            win32gui.SendMessage(child_hwnd, win32con.WM_KEYUP, vk_code, 0)
                            time.sleep(0.01)
                            
                            # 3. WM_IME_CHAR (IME karakter mesajı)
                            try:
                                win32gui.SendMessage(child_hwnd, 0x0286, char_code, 0)  # WM_IME_CHAR
                            except:
                                pass
                            
                            # 4. WM_PASTE (paste benzeri - bazı oyunlar bunu kabul eder)
                            try:
                                # Önce clipboard'a kopyala
                                win32api.OpenClipboard(None)
                                win32api.EmptyClipboard()
                                win32api.SetClipboardText(char)
                                win32api.CloseClipboard()
                                
                                # Paste mesajı gönder
                                win32gui.SendMessage(child_hwnd, win32con.WM_PASTE, 0, 0)
                                time.sleep(0.01)
                            except:
                                pass
                            
                        except Exception as e:
                            pass
                    
                    # Ana pencereye de gönder
                    try:
                        win32gui.SendMessage(self.hwnd, win32con.WM_CHAR, char_code, 0)
                    except:
                        pass
                    
                    time.sleep(0.1)
            
            print("✓ Gelişmiş Window Message tamamlandı")
            return True
        except Exception as e:
            print(f"✗ Gelişmiş Window Message hatası: {e}")
            return False
    
    def method_4_timing_optimized(self, text):
        """
        Yöntem 4: Timing Optimizasyonu
        Farklı timing stratejileri ile input gönderme
        """
        try:
            print("🔹 Yöntem 4: Timing Optimizasyonu deneniyor...")
            
            # Pencereye odaklan
            if self.hwnd:
                win32gui.SetForegroundWindow(self.hwnd)
                time.sleep(0.3)  # Daha uzun bekleme
            
            # Input field'e tıkla (eğer koordinatlar varsa)
            # Bu kısım config'den alınabilir
            
            # Farklı hızlarda yazma dene
            speeds = [0.05, 0.1, 0.15, 0.2]
            
            for speed in speeds:
                try:
                    pyautogui.FAILSAFE = False
                    pyautogui.write(text, interval=speed)
                    time.sleep(0.5)
                    
                    # Kontrol et (eğer mümkünse)
                    # Şimdilik sadece gönder
                    
                    print(f"✓ Timing {speed}s ile yazıldı")
                    return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"✗ Timing Optimizasyonu hatası: {e}")
            return False
    
    def method_5_interception_driver(self, text):
        """
        Yöntem 5: Interception Driver (Kurulum Gerekir)
        Kernel seviyesi input interception
        EN ETKİLİ ama kurulumu zor
        """
        try:
            print("🔹 Yöntem 5: Interception Driver deneniyor...")
            print("⚠ Bu yöntem için interception driver kurulumu gerekir")
            print("   https://github.com/oblitum/Interception")
            
            # Interception driver Python wrapper'ı gerekir
            # pip install interception
            try:
                import interception
                
                # Interception context oluştur
                context = interception.interception()
                interception.set_filter(context, interception.is_keyboard, interception.FILTER_KEY_ALL)
                
                # Her karakter için interception ile gönder
                for char in text:
                    if char.isdigit():
                        scan_code = ord(char) - ord('0') + 2  # 0-9 için scan code
                        
                        # Key down
                        stroke = interception.KeyStroke(scan_code, 0, 0)
                        interception.send(context, interception.keyboard(0), stroke, 1)
                        time.sleep(0.01)
                        
                        # Key up
                        stroke = interception.KeyStroke(scan_code, 0, 2)  # 2 = key up
                        interception.send(context, interception.keyboard(0), stroke, 1)
                        time.sleep(0.05)
                
                print("✓ Interception Driver tamamlandı")
                return True
            except ImportError:
                print("⚠ Interception driver kurulu değil")
                print("   Kurulum: pip install interception")
                print("   Driver: https://github.com/oblitum/Interception/releases")
                return False
        except Exception as e:
            print(f"✗ Interception Driver hatası: {e}")
            return False
    
    def try_all_advanced_methods(self, text, hwnd=None):
        """
        Tüm gelişmiş yöntemleri dener
        
        Args:
            text: Yazılacak metin
            hwnd: Pencere handle'ı
        
        Returns:
            Başarılı olan yöntem veya None
        """
        if hwnd:
            self.hwnd = hwnd
        
        methods = [
            ("DirectInput Simulation", self.method_2_directinput),
            ("Gelişmiş Window Message", self.method_3_window_message_advanced),
            ("Timing Optimizasyonu", self.method_4_timing_optimized),
            ("Raw Input API", self.method_1_raw_input),
            # Interception driver en son (kurulum gerekir)
            # ("Interception Driver", self.method_5_interception_driver),
        ]
        
        for method_name, method_func in methods:
            try:
                if method_func(text):
                    return method_name
            except Exception as e:
                print(f"✗ {method_name} hatası: {e}")
                continue
        
        return None


if __name__ == "__main__":
    # Test
    print("=" * 60)
    print("GELİŞMİŞ INPUT YÖNTEMLERİ TEST")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!")
    print("5 saniye içinde oyun penceresine geçin...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Pencere bul
    if WIN32_AVAILABLE:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        print(f"\nAktif pencere: {window_title}")
    else:
        hwnd = None
    
    # Test
    advanced = AdvancedInput(hwnd)
    result = advanced.try_all_advanced_methods("1234", hwnd)
    
    if result:
        print(f"\n✓ Başarılı yöntem: {result}")
    else:
        print("\n✗ Hiçbir yöntem çalışmadı")

