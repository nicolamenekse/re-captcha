"""
Input Window Bulucu
Oyun içindeki input field ve button'u bulur
"""
import json
import time
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def find_input_windows():
    """Input field ve button window'larını bulur"""
    if not WIN32_AVAILABLE:
        print("Win32 modülleri bulunamadı!")
        return
    
    # Config yükle
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Hata: config.json bulunamadı!")
        return
    
    game_settings = config.get("game_settings", {})
    window_name = game_settings.get("window_name", "")
    coordinates = config.get("coordinates", {})
    input_field = coordinates.get("input_field", {})
    confirm_button = coordinates.get("confirm_button", {})
    
    # Ana pencereyi bul
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
    
    parent_hwnd, title = windows[0]
    print(f"✓ Ana pencere bulundu: {title}")
    
    # Pencere koordinatlarını al
    window_rect = win32gui.GetWindowRect(parent_hwnd)
    client_rect = win32gui.GetClientRect(parent_hwnd)
    client_point = win32gui.ClientToScreen(parent_hwnd, (0, 0))
    
    print(f"Pencere rect: {window_rect}")
    print(f"Client rect: {client_rect}")
    print(f"Client point (ekran): {client_point}")
    
    # Child window'ları bul
    child_windows = []
    
    def enum_child_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            window_text = win32gui.GetWindowText(hwnd)
            
            # Client koordinatlarını al
            try:
                child_client_rect = win32gui.GetClientRect(hwnd)
                child_client_point = win32gui.ClientToScreen(hwnd, (0, 0))
                
                # Window rect'i al
                child_window_rect = win32gui.GetWindowRect(hwnd)
                
                child_windows.append({
                    'hwnd': hwnd,
                    'class': class_name,
                    'text': window_text,
                    'client_rect': child_client_rect,
                    'client_point': child_client_point,
                    'window_rect': child_window_rect
                })
            except:
                pass
        return True
    
    win32gui.EnumChildWindows(parent_hwnd, enum_child_proc, None)
    
    print(f"\nBulunan child window sayısı: {len(child_windows)}")
    
    # Input field koordinatlarına yakın olanları bul
    if input_field and input_field.get("x") != 0:
        input_x = input_field.get("x", 0)
        input_y = input_field.get("y", 0)
        input_w = input_field.get("width", 200)
        input_h = input_field.get("height", 30)
        input_center_x = input_x + input_w // 2
        input_center_y = input_y + input_h // 2
        
        # Ekran koordinatlarına çevir
        screen_input_x = client_point[0] + input_center_x
        screen_input_y = client_point[1] + input_center_y
        
        print(f"\nInput field koordinatları:")
        print(f"  Pencere içi: ({input_center_x}, {input_center_y})")
        print(f"  Ekran: ({screen_input_x}, {screen_input_y})")
        
        # Yakın child window'ları bul
        print("\nYakın child window'lar:")
        for i, child in enumerate(child_windows, 1):
            child_x = child['client_point'][0]
            child_y = child['client_point'][1]
            distance = ((child_x - screen_input_x)**2 + (child_y - screen_input_y)**2)**0.5
            
            print(f"  {i}. Class: {child['class']}, Text: '{child['text']}'")
            print(f"     Client point: {child['client_point']}")
            print(f"     Window rect: {child['window_rect']}")
            print(f"     Distance: {distance:.1f}px")
            
            # Eğer Edit class'ıysa ve yakınsa, bu input field olabilir
            if child['class'] == 'Edit' and distance < 100:
                print(f"     ⭐ Potansiyel input field!")
    
    # Confirm button koordinatlarına yakın olanları bul
    if confirm_button and confirm_button.get("x") != 0:
        confirm_x = confirm_button.get("x", 0)
        confirm_y = confirm_button.get("y", 0)
        confirm_w = confirm_button.get("width", 100)
        confirm_h = confirm_button.get("height", 30)
        confirm_center_x = confirm_x + confirm_w // 2
        confirm_center_y = confirm_y + confirm_h // 2
        
        # Ekran koordinatlarına çevir
        screen_confirm_x = client_point[0] + confirm_center_x
        screen_confirm_y = client_point[1] + confirm_center_y
        
        print(f"\nConfirm button koordinatları:")
        print(f"  Pencere içi: ({confirm_center_x}, {confirm_center_y})")
        print(f"  Ekran: ({screen_confirm_x}, {screen_confirm_y})")
        
        # Yakın child window'ları bul
        print("\nYakın child window'lar:")
        for i, child in enumerate(child_windows, 1):
            child_x = child['client_point'][0]
            child_y = child['client_point'][1]
            distance = ((child_x - screen_confirm_x)**2 + (child_y - screen_confirm_y)**2)**0.5
            
            if distance < 100:
                print(f"  {i}. Class: {child['class']}, Text: '{child['text']}'")
                print(f"     Client point: {child['client_point']}")
                print(f"     Distance: {distance:.1f}px")
                print(f"     ⭐ Potansiyel confirm button!")
    
    # Test: Child window'a direkt mesaj gönder
    print("\n" + "=" * 60)
    print("TEST: CHILD WINDOW'A DİREKT MESAJ GÖNDERME")
    print("=" * 60)
    
    if child_windows:
        # İlk Edit window'u bul
        edit_windows = [c for c in child_windows if c['class'] == 'Edit']
        if edit_windows:
            test_window = edit_windows[0]
            print(f"\nTest window: Class={test_window['class']}, HWND={test_window['hwnd']}")
            
            print("\n5 saniye içinde oyun penceresine geçin...")
            time.sleep(5)
            
            # Pencereye odaklan
            win32gui.ShowWindow(parent_hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(parent_hwnd)
            time.sleep(0.5)
            
            # Child window'a focus gönder
            print("\nChild window'a focus gönderiliyor...")
            try:
                win32gui.SetFocus(test_window['hwnd'])
                time.sleep(0.3)
                print("✓ Focus gönderildi")
            except Exception as e:
                print(f"Focus hatası: {e}")
            
            # WM_CHAR mesajı gönder
            print("\nWM_CHAR mesajı gönderiliyor (test: '5')...")
            try:
                win32gui.SendMessage(test_window['hwnd'], win32con.WM_CHAR, ord('5'), 0)
                time.sleep(0.1)
                win32gui.SendMessage(test_window['hwnd'], win32con.WM_CHAR, ord('5'), 0)
                time.sleep(0.1)
                win32gui.SendMessage(test_window['hwnd'], win32con.WM_CHAR, ord('7'), 0)
                time.sleep(0.1)
                win32gui.SendMessage(test_window['hwnd'], win32con.WM_CHAR, ord('8'), 0)
                print("✓ WM_CHAR mesajları gönderildi")
            except Exception as e:
                print(f"WM_CHAR hatası: {e}")
            
            print("\nOyun penceresinde kontrol edin: '5578' yazıldı mı?")


if __name__ == "__main__":
    find_input_window()

