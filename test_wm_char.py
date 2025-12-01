"""
WM_CHAR Mesajı Test
Oyun penceresine direkt WM_CHAR mesajı gönderir
"""
import time
try:
    import win32gui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Win32 modülleri bulunamadı!")


def send_wm_char_to_window(window_name, text):
    """
    Oyun penceresine WM_CHAR mesajı gönderir
    
    Args:
        window_name: Pencere adı
        text: Gönderilecek metin
    """
    if not WIN32_AVAILABLE:
        print("Win32 modülleri bulunamadı!")
        return False
    
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
        return False
    
    hwnd, title = windows[0]
    print(f"✓ Pencere bulundu: {title}")
    
    # Pencereye odaklan
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.2)
    
    print(f"\nWM_CHAR mesajları gönderiliyor: '{text}'")
    
    # Child window'ları bul (input field olabilir)
    child_windows = []
    def enum_child_proc(child_hwnd, lParam):
        if win32gui.IsWindowVisible(child_hwnd):
            child_text = win32gui.GetWindowText(child_hwnd)
            class_name = win32gui.GetClassName(child_hwnd)
            child_windows.append((child_hwnd, child_text, class_name))
        return True
    
    win32gui.EnumChildWindows(hwnd, enum_child_proc, None)
    
    if child_windows:
        print(f"  {len(child_windows)} child window bulundu")
        # Edit veya Input ile ilgili child window'ları bul
        input_windows = [cw for cw in child_windows if 'edit' in cw[2].lower() or 'input' in cw[2].lower()]
        if input_windows:
            print(f"  {len(input_windows)} input window bulundu")
            target_hwnd = input_windows[0][0]
            print(f"  Input window'a mesaj gönderiliyor: {input_windows[0][2]}")
        else:
            target_hwnd = hwnd
            print(f"  Ana pencereye mesaj gönderiliyor")
    else:
        target_hwnd = hwnd
        print(f"  Ana pencereye mesaj gönderiliyor")
    
    # Ana pencereye de mesaj göndermeyi dene (child window engelleniyorsa)
    print(f"\n  Ana pencereye de mesaj göndermeyi deniyoruz...")
    
    # Her karakter için WM_CHAR gönder (hem PostMessage hem SendMessage)
    for char in text:
        if char.isdigit() or char.isalpha():
            char_code = ord(char)
            vk_code = ord(char.upper())
            print(f"  '{char}' gönderiliyor (code: {char_code}, vk: {vk_code})...")
            
            # Yöntem 1: Ana pencereye PostMessage (child window engelleniyorsa)
            try:
                result1 = win32gui.PostMessage(hwnd, win32con.WM_CHAR, char_code, 0)
                print(f"    ✓ Ana pencere PostMessage: {result1}")
            except Exception as e:
                print(f"    ✗ Ana pencere PostMessage: {e}")
            
            # Yöntem 2: Child window'a PostMessage (try-except ile)
            try:
                result2 = win32gui.PostMessage(target_hwnd, win32con.WM_CHAR, char_code, 0)
                print(f"    ✓ Child PostMessage: {result2}")
            except Exception as e:
                print(f"    ✗ Child PostMessage: {e}")
            
            # Yöntem 3: Ana pencereye SendMessage
            try:
                result3 = win32gui.SendMessage(hwnd, win32con.WM_CHAR, char_code, 0)
                print(f"    ✓ Ana pencere SendMessage: {result3}")
            except Exception as e:
                print(f"    ✗ Ana pencere SendMessage: {e}")
            
            # Yöntem 4: Child window'a SendMessage
            try:
                result4 = win32gui.SendMessage(target_hwnd, win32con.WM_CHAR, char_code, 0)
                print(f"    ✓ Child SendMessage: {result4}")
            except Exception as e:
                print(f"    ✗ Child SendMessage: {e}")
            
            # Yöntem 5: WM_KEYDOWN + WM_KEYUP (ana pencere)
            try:
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(0.01)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
                print(f"    ✓ Ana pencere WM_KEYDOWN/UP: {vk_code}")
            except Exception as e:
                print(f"    ✗ Ana pencere WM_KEYDOWN/UP: {e}")
            
            # Yöntem 6: WM_KEYDOWN + WM_KEYUP (child window)
            try:
                win32gui.PostMessage(target_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(0.01)
                win32gui.PostMessage(target_hwnd, win32con.WM_KEYUP, vk_code, 0)
                print(f"    ✓ Child WM_KEYDOWN/UP: {vk_code}")
            except Exception as e:
                print(f"    ✗ Child WM_KEYDOWN/UP: {e}")
            
            time.sleep(0.1)
    
    print("\n✓ WM_CHAR mesajları gönderildi")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("WM_CHAR MESAJI TEST")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!")
    print("5 saniye içinde oyun penceresine geçin ve input field'e tıklayın...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    test_text = "1234"
    window_name = "SeaSRO2025"
    
    print(f"\nTest edilecek metin: '{test_text}'")
    print(f"Pencere adı: {window_name}")
    
    send_wm_char_to_window(window_name, test_text)
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nOyun penceresinde kontrol edin:")
    print("1. Input field'de '1234' yazıldı mı?")
    print("2. WM_CHAR mesajı çalıştı mı?")

