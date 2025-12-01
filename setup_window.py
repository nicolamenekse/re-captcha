"""
Oyun Penceresi Kurulum Aracı
Oyun penceresini bulur ve config'e kaydeder
"""
import json
from window_manager import find_game_window, WindowManager


def setup_window():
    """Oyun penceresini bulur ve config'e kaydeder"""
    print("=" * 60)
    print("OYUN PENCERESİ KURULUMU")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve aktif edin!")
    print("Oyun penceresine geçmeniz için 10 saniye bekleniyor...")
    
    import time
    for i in range(10, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nOyun penceresi aranıyor...")
    result = find_game_window()
    
    if result:
        hwnd, title = result
        print(f"\n✓ Pencere bulundu: {title}")
        
        wm = WindowManager()
        wm.window_handle = hwnd
        
        window_rect = wm.get_window_rect()
        client_rect = wm.get_client_rect()
        
        if window_rect:
            print(f"\nPencere koordinatları: {window_rect}")
            print(f"  Sol: {window_rect[0]}, Üst: {window_rect[1]}")
            print(f"  Sağ: {window_rect[2]}, Alt: {window_rect[3]}")
        
        if client_rect:
            print(f"\nClient koordinatları: {client_rect}")
            print(f"  Sol: {client_rect[0]}, Üst: {client_rect[1]}")
            print(f"  Sağ: {client_rect[2]}, Alt: {client_rect[3]}")
        
        # Config'e kaydet
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        
        if "game_settings" not in config:
            config["game_settings"] = {}
        
        config["game_settings"]["window_name"] = title
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"\n✓ Pencere adı config'e kaydedildi: {title}")
        print("\nNot: Koordinatlarınız pencere içi (relative) koordinatlar olmalı!")
        print("Eğer ekran koordinatları kullanıyorsanız, pencere başlangıç noktasını çıkarın.")
        
    else:
        print("\n⚠ Oyun penceresi otomatik bulunamadı!")
        print("\nTüm açık pencereler listeleniyor...")
        
        # Tüm pencereleri listele
        try:
            import win32gui
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:
                        windows.append((hwnd, window_text))
            
            all_windows = []
            win32gui.EnumWindows(callback, all_windows)
            
            print("\nAçık pencereler:")
            for i, (hwnd, title) in enumerate(all_windows[:20], 1):  # İlk 20 pencere
                print(f"  {i}. {title}")
            
            if len(all_windows) > 20:
                print(f"  ... ve {len(all_windows) - 20} pencere daha")
        
        except:
            pass
        
        print("\nManuel olarak pencere adını girebilirsiniz:")
        window_name = input("Pencere adı (boş bırakırsanız atlanır): ").strip()
        
        if window_name:
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            if "game_settings" not in config:
                config["game_settings"] = {}
            
            config["game_settings"]["window_name"] = window_name
            
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"✓ Pencere adı kaydedildi: {window_name}")


if __name__ == "__main__":
    setup_window()

