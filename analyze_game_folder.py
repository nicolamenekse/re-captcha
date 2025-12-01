"""
Oyun Klasörü Analiz Aracı
Oyun klasöründeki input sistemi ile ilgili dosyaları bulur
"""
import os
import json
from pathlib import Path


def analyze_game_folder(game_folder_path):
    """
    Oyun klasörünü analiz eder ve input sistemi ile ilgili dosyaları bulur
    
    Args:
        game_folder_path: Oyun klasörünün yolu
    """
    print("=" * 60)
    print("OYUN KLASÖRÜ ANALİZİ")
    print("=" * 60)
    
    if not os.path.exists(game_folder_path):
        print(f"❌ Klasör bulunamadı: {game_folder_path}")
        return
    
    game_path = Path(game_folder_path)
    
    print(f"\n📁 Analiz edilen klasör: {game_folder_path}")
    print(f"📊 Toplam dosya sayısı: {sum(1 for _ in game_path.rglob('*') if _.is_file())}")
    
    # İlgili dosya türlerini ara
    relevant_files = {
        "executables": [],
        "config_files": [],
        "dll_files": [],
        "ini_files": [],
        "xml_files": [],
        "json_files": [],
        "log_files": [],
        "input_related": []
    }
    
    # İlgili dosya isimleri (input ile ilgili)
    input_keywords = [
        "input", "keyboard", "mouse", "key", "config", "setting", 
        "option", "control", "raw", "direct", "dinput", "wininput"
    ]
    
    print("\n🔍 Dosyalar aranıyor...")
    
    for file_path in game_path.rglob('*'):
        if file_path.is_file():
            file_name_lower = file_path.name.lower()
            file_ext = file_path.suffix.lower()
            
            # Executable dosyalar
            if file_ext in ['.exe', '.bin']:
                relevant_files["executables"].append(str(file_path.relative_to(game_path)))
            
            # DLL dosyalar
            elif file_ext == '.dll':
                relevant_files["dll_files"].append(str(file_path.relative_to(game_path)))
            
            # Config dosyalar
            elif file_ext in ['.ini', '.cfg', '.conf', '.config']:
                relevant_files["config_files"].append(str(file_path.relative_to(game_path)))
                relevant_files["ini_files"].append(str(file_path.relative_to(game_path)))
            
            # XML dosyalar
            elif file_ext == '.xml':
                relevant_files["xml_files"].append(str(file_path.relative_to(game_path)))
            
            # JSON dosyalar
            elif file_ext == '.json':
                relevant_files["json_files"].append(str(file_path.relative_to(game_path)))
            
            # Log dosyalar
            elif file_ext == '.log' or 'log' in file_name_lower:
                relevant_files["log_files"].append(str(file_path.relative_to(game_path)))
            
            # Input ile ilgili dosyalar
            if any(keyword in file_name_lower for keyword in input_keywords):
                relevant_files["input_related"].append(str(file_path.relative_to(game_path)))
    
    # Sonuçları göster
    print("\n" + "=" * 60)
    print("BULUNAN DOSYALAR")
    print("=" * 60)
    
    # Executable dosyalar
    if relevant_files["executables"]:
        print(f"\n📦 Executable Dosyalar ({len(relevant_files['executables'])}):")
        for exe in relevant_files["executables"][:10]:  # İlk 10'unu göster
            print(f"   - {exe}")
        if len(relevant_files["executables"]) > 10:
            print(f"   ... ve {len(relevant_files['executables']) - 10} tane daha")
    
    # Config dosyalar
    if relevant_files["config_files"]:
        print(f"\n⚙️  Config Dosyalar ({len(relevant_files['config_files'])}):")
        for cfg in relevant_files["config_files"][:20]:
            print(f"   - {cfg}")
        if len(relevant_files["config_files"]) > 20:
            print(f"   ... ve {len(relevant_files['config_files']) - 20} tane daha")
    
    # DLL dosyalar (input ile ilgili olanlar)
    input_dlls = [dll for dll in relevant_files["dll_files"] 
                  if any(kw in dll.lower() for kw in ['input', 'key', 'mouse', 'dinput', 'raw'])]
    if input_dlls:
        print(f"\n🔧 Input ile İlgili DLL Dosyalar ({len(input_dlls)}):")
        for dll in input_dlls:
            print(f"   - {dll}")
    
    # Input ile ilgili dosyalar
    if relevant_files["input_related"]:
        print(f"\n⌨️  Input ile İlgili Dosyalar ({len(relevant_files['input_related'])}):")
        for inp in relevant_files["input_related"][:20]:
            print(f"   - {inp}")
        if len(relevant_files["input_related"]) > 20:
            print(f"   ... ve {len(relevant_files['input_related']) - 20} tane daha")
    
    # Config dosyalarının içeriğini oku (ilk 5 tanesini)
    print("\n" + "=" * 60)
    print("CONFIG DOSYALARININ İÇERİĞİ")
    print("=" * 60)
    
    config_samples = []
    for cfg_file in relevant_files["config_files"][:5]:
        cfg_path = game_path / cfg_file
        try:
            with open(cfg_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)  # İlk 2000 karakter
                if any(kw in content.lower() for kw in ['input', 'keyboard', 'mouse', 'raw', 'direct']):
                    config_samples.append({
                        "file": cfg_file,
                        "preview": content[:500]  # İlk 500 karakter
                    })
        except:
            pass
    
    if config_samples:
        for sample in config_samples:
            print(f"\n📄 {sample['file']}:")
            print("-" * 60)
            print(sample['preview'])
            print("...")
    
    # Sonuçları JSON'a kaydet
    output_file = "game_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(relevant_files, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Analiz sonuçları kaydedildi: {output_file}")
    print("\n" + "=" * 60)
    print("ÖNERİLER")
    print("=" * 60)
    print("1. Config dosyalarını kontrol edin (input ayarları)")
    print("2. Executable dosyasını kontrol edin (oyunun ana dosyası)")
    print("3. DLL dosyalarını kontrol edin (input handling)")
    print("4. Log dosyalarını kontrol edin (input event'leri)")
    print("\nBu bilgileri paylaşın, input sistemini anlayabiliriz!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Kullanım: python analyze_game_folder.py <oyun_klasörü_yolu>")
        print("\nÖrnek:")
        print("  python analyze_game_folder.py \"C:\\Program Files\\Game\"")
        print("  python analyze_game_folder.py \"C:\\Users\\Kullanici\\Desktop\\SRO\"")
        sys.exit(1)
    
    game_folder = sys.argv[1]
    analyze_game_folder(game_folder)

