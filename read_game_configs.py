"""
Oyun Config Dosyalarını Okuma Aracı
Input ayarlarını bulur
"""
import os
from pathlib import Path


def read_game_configs(game_folder_path):
    """
    Oyun config dosyalarını okur
    
    Args:
        game_folder_path: Oyun klasörünün yolu
    """
    print("=" * 60)
    print("OYUN CONFIG DOSYALARI OKUNUYOR")
    print("=" * 60)
    
    game_path = Path(game_folder_path)
    
    # Önemli config dosyaları
    config_files = [
        "setting/SROptionSet.dat",
        "setting/SRExtQSOption.dat",
        "setting/KGuardSettings.ini"
    ]
    
    for config_file in config_files:
        config_path = game_path / config_file
        if config_path.exists():
            print(f"\n{'='*60}")
            print(f"📄 {config_file}")
            print('='*60)
            
            try:
                # Binary dosya olabilir, önce text olarak dene
                with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if content.strip():
                        print(content[:2000])  # İlk 2000 karakter
                        if len(content) > 2000:
                            print("\n... (devamı var)")
                    else:
                        print("(Dosya boş veya binary)")
            except:
                # Binary dosya olabilir, hex olarak göster
                try:
                    with open(config_path, 'rb') as f:
                        content = f.read(500)  # İlk 500 byte
                        print("(Binary dosya - hex gösterimi):")
                        print(content.hex()[:200])
                        print("\n(Text olarak okunabilir kısımlar):")
                        # Text karakterleri bul
                        text_chars = ''.join(chr(b) if 32 <= b < 127 else '.' for b in content)
                        print(text_chars[:200])
                except Exception as e:
                    print(f"❌ Okunamadı: {e}")
            
            # Input ile ilgili satırları ara
            try:
                with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    input_lines = []
                    for i, line in enumerate(lines, 1):
                        line_lower = line.lower()
                        if any(keyword in line_lower for keyword in 
                               ['input', 'keyboard', 'mouse', 'key', 'raw', 'direct', 
                                'dinput', 'wininput', 'capture', 'hook']):
                            input_lines.append((i, line.strip()))
                    
                    if input_lines:
                        print(f"\n🔍 Input ile ilgili satırlar:")
                        for line_num, line_content in input_lines[:20]:
                            print(f"   Satır {line_num}: {line_content}")
            except:
                pass
    
    # Executable dosyasını kontrol et
    exe_path = game_path / "SRO_Client.exe"
    if exe_path.exists():
        print(f"\n{'='*60}")
        print("📦 SRO_Client.exe Bilgileri")
        print('='*60)
        stat = exe_path.stat()
        print(f"Boyut: {stat.st_size / (1024*1024):.2f} MB")
        print(f"Son değiştirilme: {stat.st_mtime}")
        
        # Dosya içinde string arama (input ile ilgili)
        try:
            with open(exe_path, 'rb') as f:
                content = f.read(100000)  # İlk 100KB
                # Text string'leri bul
                text_content = content.decode('utf-8', errors='ignore')
                input_strings = []
                keywords = ['input', 'keyboard', 'mouse', 'raw', 'direct', 'dinput']
                for keyword in keywords:
                    if keyword in text_content.lower():
                        # Keyword'ün etrafındaki text'i bul
                        idx = text_content.lower().find(keyword)
                        if idx != -1:
                            start = max(0, idx - 50)
                            end = min(len(text_content), idx + 100)
                            snippet = text_content[start:end].replace('\x00', ' ').strip()
                            if snippet and len(snippet) > 10:
                                input_strings.append(snippet[:150])
                
                if input_strings:
                    print(f"\n🔍 Executable içinde input ile ilgili string'ler:")
                    for i, s in enumerate(input_strings[:10], 1):
                        print(f"   {i}. {s[:100]}...")
        except Exception as e:
            print(f"Executable analiz hatası: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python read_game_configs.py <oyun_klasörü_yolu>")
        sys.exit(1)
    
    game_folder = sys.argv[1]
    read_game_configs(game_folder)

