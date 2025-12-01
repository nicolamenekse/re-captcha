"""
Derinlemesine Oyun Analizi
Oyunun input handling mekanizmasını anlamak için detaylı analiz
"""
import os
import json
import subprocess
from pathlib import Path
try:
    import win32gui
    import win32process
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def analyze_game_deep(game_folder_path, window_name="SeaSRO2025"):
    """
    Oyunu derinlemesine analiz eder
    
    Args:
        game_folder_path: Oyun klasörünün yolu
        window_name: Oyun penceresinin adı
    """
    print("=" * 60)
    print("DERİNLEMESİNE OYUN ANALİZİ")
    print("=" * 60)
    
    game_path = Path(game_folder_path)
    results = {}
    
    # 1. Executable analizi
    print("\n1️⃣ EXECUTABLE ANALİZİ")
    print("-" * 60)
    exe_path = game_path / "SRO_Client.exe"
    if exe_path.exists():
        stat = exe_path.stat()
        results["executable"] = {
            "path": str(exe_path),
            "size_mb": round(stat.st_size / (1024*1024), 2),
            "modified": stat.st_mtime
        }
        print(f"✓ Executable bulundu: {exe_path}")
        print(f"  Boyut: {results['executable']['size_mb']} MB")
        
        # Executable içinde input ile ilgili string'ler
        try:
            with open(exe_path, 'rb') as f:
                content = f.read(500000)  # İlk 500KB
                text_content = content.decode('utf-8', errors='ignore')
                
                input_keywords = {
                    'dinput': 'DirectInput',
                    'rawinput': 'Raw Input',
                    'sendinput': 'SendInput',
                    'keyboard': 'Keyboard',
                    'mouse': 'Mouse',
                    'hook': 'Hook',
                    'wndproc': 'Window Procedure',
                    'message': 'Message',
                    'wm_char': 'WM_CHAR',
                    'wm_keydown': 'WM_KEYDOWN'
                }
                
                found_keywords = {}
                for keyword, name in input_keywords.items():
                    if keyword in text_content.lower():
                        found_keywords[name] = True
                
                results["executable"]["input_keywords"] = found_keywords
                if found_keywords:
                    print(f"  Input ile ilgili bulunan keyword'ler:")
                    for name in found_keywords.keys():
                        print(f"    - {name}")
                else:
                    print("  ⚠ Input ile ilgili keyword bulunamadı")
        except Exception as e:
            print(f"  ✗ Executable analiz hatası: {e}")
    
    # 2. DLL analizi
    print("\n2️⃣ DLL ANALİZİ")
    print("-" * 60)
    dll_files = list(game_path.rglob("*.dll"))
    input_dlls = []
    for dll in dll_files:
        dll_name = dll.name.lower()
        if any(kw in dll_name for kw in ['input', 'key', 'mouse', 'dinput', 'raw', 'hook']):
            input_dlls.append(str(dll.relative_to(game_path)))
    
    results["dlls"] = {
        "total": len(dll_files),
        "input_related": input_dlls
    }
    
    if input_dlls:
        print(f"✓ Input ile ilgili DLL'ler bulundu ({len(input_dlls)}):")
        for dll in input_dlls:
            print(f"  - {dll}")
    else:
        print("  ⚠ Input ile ilgili DLL bulunamadı")
    
    # 3. Pencere analizi (oyun çalışıyorsa)
    print("\n3️⃣ PENCERE ANALİZİ")
    print("-" * 60)
    if WIN32_AVAILABLE:
        def find_window_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_name.lower() in window_text.lower():
                    windows.append((hwnd, window_text))
        
        windows = []
        win32gui.EnumWindows(find_window_callback, windows)
        
        if windows:
            hwnd, title = windows[0]
            print(f"✓ Oyun penceresi bulundu: {title}")
            
            # Pencere bilgileri
            window_rect = win32gui.GetWindowRect(hwnd)
            client_rect = win32gui.GetClientRect(hwnd)
            
            # Process bilgileri
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process_handle = win32api.OpenProcess(0x0410, False, pid)  # PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
                
                results["window"] = {
                    "title": title,
                    "hwnd": hwnd,
                    "pid": pid,
                    "window_rect": window_rect,
                    "client_rect": client_rect,
                    "is_fullscreen": (window_rect[2] - window_rect[0] >= 1920 and window_rect[3] - window_rect[1] >= 1080)
                }
                
                print(f"  Process ID: {pid}")
                print(f"  Window Rect: {window_rect}")
                print(f"  Client Rect: {client_rect}")
                print(f"  Fullscreen: {results['window']['is_fullscreen']}")
                
                win32api.CloseHandle(process_handle)
            except Exception as e:
                print(f"  ✗ Process bilgisi alınamadı: {e}")
        else:
            print("  ⚠ Oyun penceresi bulunamadı (oyun çalışmıyor olabilir)")
            print("  Lütfen oyunu açın ve tekrar deneyin")
    
    # 4. Config dosyaları detaylı analiz
    print("\n4️⃣ CONFIG DOSYALARI DETAYLI ANALİZ")
    print("-" * 60)
    config_files = [
        "setting/SROptionSet.dat",
        "setting/SRExtQSOption.dat",
        "setting/KGuardSettings.ini"
    ]
    
    config_analysis = {}
    for config_file in config_files:
        config_path = game_path / config_file
        if config_path.exists():
            try:
                # Binary mi text mi kontrol et
                with open(config_path, 'rb') as f:
                    first_bytes = f.read(100)
                    is_binary = any(b < 32 and b not in [9, 10, 13] for b in first_bytes)
                
                config_analysis[config_file] = {
                    "exists": True,
                    "is_binary": is_binary,
                    "size": config_path.stat().st_size
                }
                
                if not is_binary:
                    with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(5000)
                        # Input ile ilgili satırları bul
                        input_lines = [line.strip() for line in content.split('\n') 
                                      if any(kw in line.lower() for kw in ['input', 'key', 'mouse', 'raw', 'direct'])]
                        if input_lines:
                            config_analysis[config_file]["input_lines"] = input_lines[:10]
                
                print(f"✓ {config_file}: {'Binary' if is_binary else 'Text'} ({config_analysis[config_file]['size']} bytes)")
            except Exception as e:
                print(f"✗ {config_file} analiz hatası: {e}")
    
    results["configs"] = config_analysis
    
    # 5. Öneriler
    print("\n" + "=" * 60)
    print("ÖNERİLER VE ÇÖZÜM YÖNTEMLERİ")
    print("=" * 60)
    
    recommendations = []
    
    if results.get("window", {}).get("is_fullscreen"):
        recommendations.append("⚠ Oyun fullscreen modda - windowed moda geçmeyi deneyin")
    
    if not results.get("executable", {}).get("input_keywords"):
        recommendations.append("⚠ Executable'da input keyword'leri bulunamadı - oyun özel bir input sistemi kullanıyor olabilir")
    
    if input_dlls:
        recommendations.append(f"✓ {len(input_dlls)} input DLL bulundu - oyun bu DLL'leri kullanıyor olabilir")
    
    recommendations.append("💡 Çözüm önerileri:")
    recommendations.append("  1. Oyunu windowed moda geçirin (fullscreen input'ları engelleyebilir)")
    recommendations.append("  2. Oyun ayarlarında 'Raw Input' veya 'DirectInput' seçeneğini kapatın/açın")
    recommendations.append("  3. Oyunu yönetici olarak çalıştırın")
    recommendations.append("  4. KGuard'ı geçici olarak devre dışı bırakmayı deneyin (mümkünse)")
    recommendations.append("  5. Oyun penceresine direkt WM_CHAR mesajı göndermeyi deneyin")
    recommendations.append("  6. Oyunun input thread'ine mesaj göndermeyi deneyin")
    
    for rec in recommendations:
        print(rec)
    
    # Sonuçları kaydet
    output_file = "deep_game_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✓ Detaylı analiz sonuçları kaydedildi: {output_file}")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python deep_game_analysis.py <oyun_klasörü_yolu> [pencere_adı]")
        print("\nÖrnek:")
        print("  python deep_game_analysis.py \"C:\\Program Files\\SRO\" SeaSRO2025")
        sys.exit(1)
    
    game_folder = sys.argv[1]
    window_name = sys.argv[2] if len(sys.argv) > 2 else "SeaSRO2025"
    
    print("\n⚠ ÖNEMLİ: Analiz için oyunun çalışıyor olması gerekiyor!")
    print("Oyunu açın ve 5 saniye bekleyin...\n")
    
    import time
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    analyze_game_deep(game_folder, window_name)

