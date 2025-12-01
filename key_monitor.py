"""
Key Monitor - Oyun içinde manuel yazdığınızda key aktivitelerini izler
"""
import time
import pyautogui
try:
    import win32gui
    import win32con
    import ctypes
    from ctypes import wintypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Uyarı: win32 modülleri bulunamadı")


class KeyMonitor:
    """Key aktivitelerini izler"""
    
    def __init__(self):
        self.logged_keys = []
        self.monitoring = False
    
    def log_key_press(self, key_code, key_name):
        """Tuş basımını loglar"""
        timestamp = time.time()
        self.logged_keys.append({
            'time': timestamp,
            'code': key_code,
            'name': key_name
        })
        print(f"[{timestamp:.3f}] Key: {key_name} (Code: {key_code})")
    
    def monitor_pyautogui(self, duration=10):
        """Pyautogui ile key monitoring (basit)"""
        print("=" * 60)
        print("KEY MONITOR - PYAUTOGUI")
        print("=" * 60)
        print("\n⚠ Bu monitor sadece pyautogui'nin görebildiği tuşları izler")
        print("Oyun içinde manuel olarak yazdığınızda tuşları görmeyebilir")
        print(f"\n{duration} saniye izlenecek...")
        print("Oyun penceresine geçin ve numara yazın...")
        
        time.sleep(2)
        
        # Pyautogui ile key monitoring yapamayız çünkü sadece gönderebiliriz
        # Bunun yerine Windows API hook kullanmalıyız
        print("\nPyautogui ile key monitoring yapılamaz.")
        print("Windows API hook kullanılacak...")
    
    def monitor_win32_hook(self, duration=10):
        """Win32 API hook ile key monitoring"""
        if not WIN32_AVAILABLE:
            print("Win32 modülleri bulunamadı!")
            return
        
        print("=" * 60)
        print("KEY MONITOR - WIN32 HOOK")
        print("=" * 60)
        print(f"\n{duration} saniye izlenecek...")
        print("Oyun penceresine geçin ve numara yazın...")
        print("Her tuş basımı loglanacak.")
        print("\n5 saniye içinde oyun penceresine geçin...")
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\nİzleme başladı! Tuşları basın...")
        print("Durdurmak için Ctrl+C basın\n")
        
        # Low-level keyboard hook
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        
        HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        
        def low_level_keyboard_proc(nCode, wParam, lParam):
            if nCode >= 0:
                # WM_KEYDOWN = 0x0100, WM_KEYUP = 0x0101
                if wParam == 0x0100:  # KEYDOWN
                    vk_code = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong))[0] & 0xFF
                    key_name = self.get_key_name(vk_code)
                    self.log_key_press(vk_code, key_name)
            return user32.CallNextHookExW(None, nCode, wParam, lParam)
        
        hook_proc = HOOKPROC(low_level_keyboard_proc)
        
        # Install hook
        hHook = user32.SetWindowsHookExW(
            13,  # WH_KEYBOARD_LL
            hook_proc,
            kernel32.GetModuleHandleW(None),
            0
        )
        
        if not hHook:
            print("Hook kurulamadı!")
            return
        
        try:
            # Message loop
            start_time = time.time()
            msg = wintypes.MSG()
            while (time.time() - start_time) < duration:
                bRet = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if bRet == 0:
                    break
                elif bRet == -1:
                    break
                else:
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
        except KeyboardInterrupt:
            print("\nİzleme durduruldu!")
        finally:
            user32.UnhookWindowsHookExW(hHook)
        
        print("\n" + "=" * 60)
        print("İZLEME SONUÇLARI")
        print("=" * 60)
        print(f"Toplam {len(self.logged_keys)} tuş basımı kaydedildi:")
        for i, key in enumerate(self.logged_keys, 1):
            print(f"{i}. {key['name']} (Code: {key['code']})")
        
        return self.logged_keys
    
    def get_key_name(self, vk_code):
        """VK kodundan tuş adını alır"""
        key_names = {
            48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
            53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
            96: 'Numpad 0', 97: 'Numpad 1', 98: 'Numpad 2', 99: 'Numpad 3',
            100: 'Numpad 4', 101: 'Numpad 5', 102: 'Numpad 6',
            103: 'Numpad 7', 104: 'Numpad 8', 105: 'Numpad 9',
            13: 'Enter', 27: 'Escape', 8: 'Backspace', 9: 'Tab',
            32: 'Space', 16: 'Shift', 17: 'Ctrl', 18: 'Alt'
        }
        return key_names.get(vk_code, f'Unknown({vk_code})')
    
    def monitor_mouse_clicks(self, duration=10):
        """Mouse tıklamalarını izler"""
        if not WIN32_AVAILABLE:
            print("Win32 modülleri bulunamadı!")
            return
        
        print("=" * 60)
        print("MOUSE CLICK MONITOR")
        print("=" * 60)
        print(f"\n{duration} saniye izlenecek...")
        print("Oyun penceresine geçin ve confirm butonuna tıklayın...")
        print("\n5 saniye içinde oyun penceresine geçin...")
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\nİzleme başladı! Tıklamaları yapın...")
        print("Durdurmak için Ctrl+C basın\n")
        
        clicks = []
        start_pos = pyautogui.position()
        
        def on_click(x, y, button, pressed):
            if pressed:
                timestamp = time.time()
                clicks.append({
                    'time': timestamp,
                    'x': x,
                    'y': y,
                    'button': str(button)
                })
                print(f"[{timestamp:.3f}] Click: ({x}, {y}) - {button}")
        
        try:
            from pynput import mouse
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            
            time.sleep(duration)
            listener.stop()
        except ImportError:
            print("pynput bulunamadı! Basit monitoring yapılıyor...")
            start_time = time.time()
            last_pos = start_pos
            while (time.time() - start_time) < duration:
                current_pos = pyautogui.position()
                if current_pos != last_pos:
                    print(f"Mouse hareket: {current_pos}")
                    last_pos = current_pos
                time.sleep(0.1)
        
        print("\n" + "=" * 60)
        print("TIKLAMA SONUÇLARI")
        print("=" * 60)
        print(f"Toplam {len(clicks)} tıklama kaydedildi:")
        for i, click in enumerate(clicks, 1):
            print(f"{i}. ({click['x']}, {click['y']}) - {click['button']}")
        
        return clicks


def main():
    """Ana program"""
    print("=" * 60)
    print("KEY & MOUSE MONITOR")
    print("=" * 60)
    print("\nBu araç oyun içinde manuel yazdığınızda")
    print("key aktivitelerini ve mouse tıklamalarını izler.")
    print("\nSeçenekler:")
    print("1. Key monitoring (tuş basımları)")
    print("2. Mouse click monitoring (tıklamalar)")
    print("3. Her ikisi")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    duration = input("İzleme süresi (saniye, varsayılan 10): ").strip()
    duration = int(duration) if duration else 10
    
    monitor = KeyMonitor()
    
    if choice == "1":
        monitor.monitor_win32_hook(duration)
    elif choice == "2":
        monitor.monitor_mouse_clicks(duration)
    elif choice == "3":
        print("\nÖnce key monitoring...")
        monitor.monitor_win32_hook(duration)
        print("\nŞimdi mouse click monitoring...")
        monitor.monitor_mouse_clicks(duration)
    else:
        print("Geçersiz seçim!")


if __name__ == "__main__":
    main()

