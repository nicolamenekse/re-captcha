"""
Oyun Penceresi Yönetimi
Oyun penceresinin koordinatlarını bulur ve tıklamaları pencereye göre ayarlar
"""
import pyautogui
import time
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Uyarı: win32gui bulunamadı. Pencere yönetimi için: pip install pywin32")


class WindowManager:
    """Oyun penceresi yönetimi"""
    
    def __init__(self, window_title=None):
        """
        Window manager'ı başlatır
        
        Args:
            window_title: Pencere başlığı (opsiyonel)
        """
        self.window_title = window_title
        self.window_handle = None
        self.window_rect = None
        self.client_rect = None
    
    def find_window(self, window_title=None):
        """
        Pencereyi bulur
        
        Args:
            window_title: Pencere başlığı (None ise self.window_title kullanılır)
        
        Returns:
            Pencere handle'ı veya None
        """
        if not WIN32_AVAILABLE:
            return None
        
        title = window_title or self.window_title
        
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if title and title.lower() in window_text.lower():
                    windows.append((hwnd, window_text))
        
        windows = []
        if title:
            win32gui.EnumWindows(callback, windows)
            if windows:
                self.window_handle = windows[0][0]
                return self.window_handle
        
        return None
    
    def get_window_rect(self):
        """
        Pencere koordinatlarını alır
        
        Returns:
            (left, top, right, bottom) tuple veya None
        """
        if not WIN32_AVAILABLE or not self.window_handle:
            return None
        
        try:
            rect = win32gui.GetWindowRect(self.window_handle)
            self.window_rect = rect
            return rect
        except:
            return None
    
    def get_client_rect(self):
        """
        Client area koordinatlarını alır (pencere içi alan)
        
        Returns:
            (left, top, right, bottom) tuple veya None
        """
        if not WIN32_AVAILABLE or not self.window_handle:
            return None
        
        try:
            # Client area koordinatları (pencere içi)
            client_rect = win32gui.GetClientRect(self.window_handle)
            window_rect = self.get_window_rect()
            
            if window_rect:
                # Client area'yı ekran koordinatlarına çevir
                left, top = win32gui.ClientToScreen(self.window_handle, (0, 0))
                right = left + client_rect[2]
                bottom = top + client_rect[3]
                self.client_rect = (left, top, right, bottom)
                return self.client_rect
        except Exception as e:
            print(f"Client rect hatası: {e}")
        
        return None
    
    def focus_window(self):
        """Pencereye odaklanır"""
        if not WIN32_AVAILABLE or not self.window_handle:
            return False
        
        try:
            # Pencereyi öne getir
            win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.window_handle)
            return True
        except Exception as e:
            print(f"Pencere odaklama hatası: {e}")
            return False
    
    def click_in_window(self, x, y, relative=True):
        """
        Pencere içinde tıklar (Win32 API ile)
        
        Args:
            x, y: Koordinatlar
            relative: True ise pencere içi koordinatlar, False ise ekran koordinatları
        
        Returns:
            Başarılı ise True
        """
        if not WIN32_AVAILABLE or not self.window_handle:
            # Fallback: Normal pyautogui
            print("Win32 yok, normal tıklama deneniyor...")
            pyautogui.click(x, y)
            return True
        
        try:
            # Pencereye odaklan
            self.focus_window()
            time.sleep(0.2)
            
            if relative:
                # Pencere içi koordinatları kullan (direkt)
                click_x, click_y = x, y
            else:
                # Ekran koordinatlarını pencere içi koordinatlara çevir
                client_rect = self.get_client_rect()
                if client_rect:
                    click_x = x - client_rect[0]
                    click_y = y - client_rect[1]
                else:
                    window_rect = self.get_window_rect()
                    if window_rect:
                        click_x = x - window_rect[0]
                        click_y = y - window_rect[1]
                    else:
                        click_x, click_y = x, y
            
            # Koordinatları ekran koordinatlarına çevir
            client_rect = self.get_client_rect()
            if client_rect:
                screen_x = client_rect[0] + click_x
                screen_y = client_rect[1] + click_y
            else:
                window_rect = self.get_window_rect()
                if window_rect:
                    screen_x = window_rect[0] + click_x
                    screen_y = window_rect[1] + click_y
                else:
                    screen_x, screen_y = click_x, click_y
            
            # Önce pyautogui ile dene (daha güvenilir)
            try:
                print(f"Pyautogui ile tıklanıyor: ({screen_x}, {screen_y})")
                original_failsafe = pyautogui.FAILSAFE
                pyautogui.FAILSAFE = False
                
                # Mouse'u hareket ettir
                pyautogui.moveTo(screen_x, screen_y, duration=0.2)
                time.sleep(0.1)
                
                # Tıkla
                pyautogui.click(screen_x, screen_y)
                time.sleep(0.1)
                
                pyautogui.FAILSAFE = original_failsafe
                print(f"✓ Pyautogui ile tıklandı: ({screen_x}, {screen_y})")
                return True
            except Exception as e_py:
                print(f"Pyautogui tıklama hatası: {e_py}, SendInput deneniyor...")
                
                # Fallback: SendInput API
                try:
                    import ctypes
                    user32 = ctypes.windll.user32
                    
                    # Mouse'u hareket ettir
                    user32.SetCursorPos(int(screen_x), int(screen_y))
                    time.sleep(0.1)
                    
                    # Mouse tıklama (SendInput)
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
                    time.sleep(0.05)
                    
                    print(f"✓ SendInput API ile tıklandı: ({click_x}, {click_y})")
                    return True
                except Exception as e2:
                    print(f"SendInput tıklama hatası: {e2}")
                    return False
        except Exception as e:
            print(f"Win32 tıklama hatası: {e}")
            # Fallback: Normal pyautogui
            try:
                if relative:
                    client_rect = self.get_client_rect()
                    if client_rect:
                        screen_x = client_rect[0] + x
                        screen_y = client_rect[1] + y
                    else:
                        screen_x, screen_y = x, y
                else:
                    screen_x, screen_y = x, y
                
                pyautogui.click(screen_x, screen_y)
                return True
            except Exception as e2:
                print(f"Fallback tıklama hatası: {e2}")
                return False
    
    def send_key_to_window(self, key):
        """
        Pencereye tuş gönderir
        
        Args:
            key: Tuş kodu veya string
        """
        if not WIN32_AVAILABLE or not self.window_handle:
            pyautogui.press(key)
            return
        
        try:
            self.focus_window()
            time.sleep(0.1)
            pyautogui.press(key)
        except Exception as e:
            print(f"Tuş gönderme hatası: {e}")
            pyautogui.press(key)
    
    def send_text_to_window(self, text):
        """
        Pencereye metin gönderir (birden fazla yöntem dener - hardware-level öncelikli)
        
        Args:
            text: Gönderilecek metin
        """
        if not self.window_handle:
            # Fallback: pyautogui
            pyautogui.write(text)
            return
        
        try:
            self.focus_window()
            time.sleep(0.1)  # Kısa bekleme
            
            # Yöntem 1: Hardware-level SendInput (scan code ile - en düşük seviye)
            if WIN32_AVAILABLE:
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
                    
                    print(f"Yöntem 1: Hardware-level SendInput (scan code ile)...")
                    # Her karakter için tuş bas (scan code ile)
                    for char in text:
                        if char.isdigit() or char.isalpha():
                            vk_code = ord(char.upper())
                            # Scan code'u al (hardware-level)
                            scan_code = user32.MapVirtualKeyW(vk_code, 0)
                            
                            extra = ctypes.c_ulong(0)
                            ii_ = Input_I()
                            
                            # KEYDOWN
                            ii_.ki = KeyBdInput(vk_code, scan_code, 0, 0, ctypes.pointer(extra))
                            x = Input(ctypes.c_ulong(1), ii_)
                            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                            time.sleep(0.01)
                            
                            # KEYUP
                            ii_.ki = KeyBdInput(vk_code, scan_code, 2, 0, ctypes.pointer(extra))  # 2 = KEYEVENTF_KEYUP
                            x = Input(ctypes.c_ulong(1), ii_)
                            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                            time.sleep(0.01)
                    
                    print(f"✓ Hardware-level SendInput ile yazıldı: '{text}'")
                    return
                except Exception as e:
                    print(f"Hardware-level SendInput hatası: {e}, diğer yöntemler deneniyor...")
            
            # Yöntem 2: keyboard kütüphanesi (düşük seviye, gerçek klavye input)
            try:
                import keyboard
                print(f"Yöntem 2: keyboard kütüphanesi ile yazılıyor...")
                keyboard.write(text, delay=0.05)
                print(f"✓ keyboard kütüphanesi ile yazıldı: '{text}'")
                return
            except ImportError:
                print("keyboard kütüphanesi bulunamadı, diğer yöntemler deneniyor...")
            except Exception as e:
                print(f"keyboard hatası: {e}, diğer yöntemler deneniyor...")
            
            # Yöntem 3: Standart SendInput API
            if WIN32_AVAILABLE:
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
                    
                    print(f"Yöntem 3: Standart SendInput API ile yazılıyor...")
                    for char in text:
                        if char.isdigit() or char.isalpha():
                            vk_code = ord(char.upper())
                            
                            extra = ctypes.c_ulong(0)
                            ii_ = Input_I()
                            
                            # KEYDOWN
                            ii_.ki = KeyBdInput(vk_code, 0, 0, 0, ctypes.pointer(extra))
                            x = Input(ctypes.c_ulong(1), ii_)
                            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                            time.sleep(0.03)
                            
                            # KEYUP
                            ii_.ki = KeyBdInput(vk_code, 0, 2, 0, ctypes.pointer(extra))
                            x = Input(ctypes.c_ulong(1), ii_)
                            user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                            time.sleep(0.05)
                    
                    print(f"✓ Standart SendInput API ile yazıldı: '{text}'")
                    return
                except Exception as e:
                    print(f"Standart SendInput hatası: {e}, pyautogui fallback kullanılıyor...")
            
            # Yöntem 4: pyautogui (fallback)
            try:
                original_failsafe = pyautogui.FAILSAFE
                pyautogui.FAILSAFE = False
                pyautogui.write(text, interval=0.05)
                pyautogui.FAILSAFE = original_failsafe
                print(f"✓ Pyautogui ile yazıldı: '{text}'")
            except Exception as e2:
                print(f"Pyautogui hatası: {e2}")
        except Exception as e:
            print(f"Genel yazma hatası: {e}")


def find_game_window():
    """Oyun penceresini bulur (genel arama)"""
    if not WIN32_AVAILABLE:
        return None
    
    # Yaygın oyun pencere isimleri
    common_names = [
        "game", "oyun", "client", "launcher", 
        "metin", "metin2", "lineage", "aion",
        "mmorpg", "rpg", "online"
    ]
    
    windows = []
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text and len(window_text) > 0:
                windows.append((hwnd, window_text))
    
    win32gui.EnumWindows(callback, windows)
    
    # Önce aktif pencereyi kontrol et
    try:
        active_hwnd = win32gui.GetForegroundWindow()
        active_title = win32gui.GetWindowText(active_hwnd)
        if active_title:
            active_title_lower = active_title.lower()
            for name in common_names:
                if name in active_title_lower:
                    return active_hwnd, active_title
    except:
        pass
    
    # Oyun benzeri pencereleri bul
    for hwnd, title in windows:
        title_lower = title.lower()
        for name in common_names:
            if name in title_lower:
                return hwnd, title
    
    # Eğer bulunamazsa, en büyük pencereyi dene (genellikle oyun)
    try:
        largest_window = None
        largest_size = 0
        
        for hwnd, title in windows:
            try:
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                size = width * height
                
                # Çok küçük pencereleri atla
                if size > 100000 and size > largest_size:
                    largest_size = size
                    largest_window = (hwnd, title)
            except:
                continue
        
        if largest_window:
            return largest_window
    except:
        pass
    
    return None


if __name__ == "__main__":
    # Test
    print("Oyun penceresi aranıyor...")
    result = find_game_window()
    if result:
        hwnd, title = result
        print(f"Pencere bulundu: {title}")
        
        wm = WindowManager()
        wm.window_handle = hwnd
        rect = wm.get_window_rect()
        client_rect = wm.get_client_rect()
        
        print(f"Pencere koordinatları: {rect}")
        print(f"Client koordinatları: {client_rect}")
    else:
        print("Oyun penceresi bulunamadı!")

