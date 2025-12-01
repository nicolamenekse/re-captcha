"""
Koordinat seçme aracı - Mouse ile tıklayarak koordinat belirleme
"""
import json
import pyautogui
from screenshot import ScreenshotCapture


class CoordinateSelector:
    """Koordinat seçme sınıfı"""
    
    def __init__(self):
        self.coordinates = []
        self.screenshot = ScreenshotCapture()
        pyautogui.FAILSAFE = True  # Güvenlik: Mouse köşeye götürünce dur
    
    def get_mouse_position(self):
        """Mevcut mouse pozisyonunu döndürür"""
        return pyautogui.position()
    
    def add_coordinate(self, x, y, width=100, height=50, description=""):
        """Yeni bir koordinat ekler"""
        coord = {
            "id": len(self.coordinates) + 1,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "description": description
        }
        self.coordinates.append(coord)
        return coord
    
    def save_coordinates(self, filename="config.json"):
        """Koordinatları config dosyasına kaydeder"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        
        config["coordinates"] = {
            "number_positions": self.coordinates
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"\nKoordinatlar kaydedildi: {filename}")
    
    def interactive_select(self):
        """İnteraktif koordinat seçme"""
        print("\n" + "=" * 60)
        print("KOORDİNAT SEÇME ARACI")
        print("=" * 60)
        print("\nTalimatlar:")
        print("1. Bu pencereyi açık tutun")
        print("2. Oyun penceresine geçin")
        print("3. Numara alanının SOL ÜST köşesine mouse'u getirin")
        print("4. Buraya dönüp ENTER'a basın")
        print("5. Numara alanının SAĞ ALT köşesine mouse'u getirin")
        print("6. Buraya dönüp ENTER'a basın")
        print("\nÇıkmak için 'q' yazıp ENTER'a basın")
        print("=" * 60)
        
        while True:
            command = input("\nKomut (ENTER=koordinat al, 'q'=çık, 's'=kaydet): ").strip().lower()
            
            if command == 'q':
                break
            elif command == 's':
                if self.coordinates:
                    self.save_coordinates()
                else:
                    print("Kaydedilecek koordinat yok!")
                continue
            elif command == '' or command == 'enter':
                # İlk köşe (sol üst)
                input("Mouse'u SOL ÜST köşeye getirin ve ENTER'a basın...")
                pos1 = self.get_mouse_position()
                print(f"Sol üst köşe: ({pos1.x}, {pos1.y})")
                
                # İkinci köşe (sağ alt)
                input("Mouse'u SAĞ ALT köşeye getirin ve ENTER'a basın...")
                pos2 = self.get_mouse_position()
                print(f"Sağ alt köşe: ({pos2.x}, {pos2.y})")
                
                # Koordinatları hesapla
                x = min(pos1.x, pos2.x)
                y = min(pos1.y, pos2.y)
                width = abs(pos2.x - pos1.x)
                height = abs(pos2.y - pos1.y)
                
                description = input("Açıklama (opsiyonel): ").strip()
                
                coord = self.add_coordinate(x, y, width, height, description)
                print(f"\nKoordinat eklendi: ID={coord['id']}, X={x}, Y={y}, W={width}, H={height}")
                
                # Önizleme için screenshot al
                preview = self.screenshot.capture_region(x, y, width, height)
                preview_filename = f"preview_coord_{coord['id']}.png"
                self.screenshot.save_screenshot(preview, preview_filename)
                print(f"Önizleme kaydedildi: {preview_filename}")
            else:
                print("Geçersiz komut!")
        
        # Çıkışta kaydet
        if self.coordinates:
            save = input("\nKoordinatları kaydetmek ister misiniz? (e/h): ").strip().lower()
            if save == 'e':
                self.save_coordinates()
        
        print(f"\nToplam {len(self.coordinates)} koordinat seçildi.")


if __name__ == "__main__":
    selector = CoordinateSelector()
    selector.interactive_select()

