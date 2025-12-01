"""
Görsel Analizi ile Koordinat Bulucu
Görsel üzerinden numara alanlarının koordinatlarını otomatik bulur
"""
import cv2
import numpy as np
import json
from PIL import Image
import os


class ImageCoordinateFinder:
    """Görsel analizi ile koordinat bulucu"""
    
    def __init__(self):
        self.image = None
        self.image_path = None
        self.coordinates = []
    
    def load_image(self, image_path):
        """
        Görseli yükler
        
        Args:
            image_path: Görsel dosya yolu
        
        Returns:
            Yüklenen görsel (numpy array)
        """
        if not os.path.exists(image_path):
            print(f"Hata: Görsel bulunamadı: {image_path}")
            return None
        
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        
        if self.image is None:
            print(f"Hata: Görsel yüklenemedi: {image_path}")
            return None
        
        print(f"Görsel yüklendi: {image_path}")
        print(f"Boyut: {self.image.shape[1]}x{self.image.shape[0]}")
        return self.image
    
    def show_image_with_instructions(self):
        """Görseli gösterir ve talimatları yazdırır"""
        if self.image is None:
            print("Önce bir görsel yükleyin!")
            return
        
        print("\n" + "=" * 60)
        print("GÖRSEL ANALİZİ")
        print("=" * 60)
        print("\nGörsel açılıyor...")
        print("Talimatlar:")
        print("1. Görsel açıldığında, numara alanlarını belirleyin")
        print("2. Her numara alanı için koordinatları girin")
        print("3. 'q' ile çıkın")
        print("=" * 60)
        
        # Görseli göster
        cv2.imshow("Görsel - Koordinat Seçimi (Kapatmak için 'q' basın)", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def interactive_coordinate_selection(self):
        """
        İnteraktif koordinat seçimi
        Kullanıcıdan her numara alanı için koordinat ister
        """
        if self.image is None:
            print("Önce bir görsel yükleyin!")
            return
        
        height, width = self.image.shape[:2]
        print(f"\nGörsel boyutu: {width}x{height}")
        print("\nKoordinat seçimi başlıyor...")
        print("Her numara alanı için X, Y, Genişlik, Yükseklik değerlerini girin")
        print("Çıkmak için 'q' yazın\n")
        
        coord_id = 1
        
        while True:
            print(f"\n--- Koordinat {coord_id} ---")
            print("X koordinatı (sol üst köşe): ", end="")
            x_input = input().strip()
            
            if x_input.lower() == 'q':
                break
            
            try:
                x = int(x_input)
                y = int(input("Y koordinatı (sol üst köşe): ").strip())
                w = int(input("Genişlik: ").strip())
                h = int(input("Yükseklik: ").strip())
                desc = input("Açıklama (opsiyonel): ").strip()
                
                # Sınır kontrolü
                if x < 0 or y < 0 or x + w > width or y + h > height:
                    print("Uyarı: Koordinatlar görsel sınırları dışında!")
                    continue_choice = input("Yine de eklemek ister misiniz? (e/h): ").strip().lower()
                    if continue_choice != 'e':
                        continue
                
                coord = {
                    "id": coord_id,
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "description": desc if desc else f"Numara alanı {coord_id}"
                }
                
                self.coordinates.append(coord)
                
                # Önizleme göster
                self.show_coordinate_preview(coord)
                
                coord_id += 1
                
                add_more = input("\nBaşka koordinat eklemek ister misiniz? (e/h): ").strip().lower()
                if add_more != 'e':
                    break
            
            except ValueError:
                print("Hata: Geçerli bir sayı girin!")
                continue
        
        print(f"\nToplam {len(self.coordinates)} koordinat seçildi.")
        return self.coordinates
    
    def show_coordinate_preview(self, coord):
        """Seçilen koordinatın önizlemesini gösterir"""
        x, y, w, h = coord["x"], coord["y"], coord["width"], coord["height"]
        
        # Görselin kopyasını al
        preview = self.image.copy()
        
        # Dikdörtgen çiz
        cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # ID yaz
        cv2.putText(preview, f"ID: {coord['id']}", (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Bölgeyi kırp ve kaydet
        region = self.image[y:y+h, x:x+w]
        preview_filename = f"preview_coord_{coord['id']}.png"
        cv2.imwrite(preview_filename, region)
        
        print(f"\nKoordinat {coord['id']} önizlemesi:")
        print(f"  X: {x}, Y: {y}, Genişlik: {w}, Yükseklik: {h}")
        print(f"  Önizleme kaydedildi: {preview_filename}")
        
        # Görseli göster
        cv2.imshow(f"Koordinat {coord['id']} - Kapatmak için herhangi bir tuşa basın", preview)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def save_coordinates_to_config(self, config_path="config.json"):
        """Koordinatları config dosyasına kaydeder"""
        if not self.coordinates:
            print("Kaydedilecek koordinat yok!")
            return False
        
        try:
            # Mevcut config'i yükle
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            # Koordinatları güncelle
            config["coordinates"] = {
                "number_positions": self.coordinates
            }
            
            # Kaydet
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"\n✓ Koordinatlar kaydedildi: {config_path}")
            print(f"  Toplam {len(self.coordinates)} koordinat")
            return True
        
        except Exception as e:
            print(f"Hata: Koordinatlar kaydedilemedi: {e}")
            return False
    
    def analyze_image_for_text_regions(self):
        """
        Görseli analiz ederek metin alanlarını otomatik tespit eder
        (Deneysel - OCR ile metin alanlarını bulur)
        """
        if self.image is None:
            print("Önce bir görsel yükleyin!")
            return
        
        print("\nGörsel analiz ediliyor (metin alanları tespit ediliyor)...")
        
        # Gri tonlamaya çevir
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Threshold
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Kontur bulma
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Metin benzeri alanları filtrele
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Çok küçük veya çok büyük alanları filtrele
            if 100 < area < 50000 and 10 < w < 500 and 10 < h < 200:
                text_regions.append((x, y, w, h))
        
        print(f"Tespit edilen {len(text_regions)} potansiyel metin alanı")
        
        # Görseli göster
        preview = self.image.copy()
        for i, (x, y, w, h) in enumerate(text_regions, 1):
            cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(preview, str(i), (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imshow("Tespit Edilen Metin Alanları - Kapatmak için 'q' basın", preview)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return text_regions


def main():
    """Ana program"""
    import sys
    
    print("=" * 60)
    print("GÖRSEL KOORDİNAT BULUCU")
    print("=" * 60)
    
    finder = ImageCoordinateFinder()
    
    # Komut satırı argümanı varsa
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("\nGörsel dosya yolu: ").strip().strip('"')
    
    # Görseli yükle
    if not finder.load_image(image_path):
        return
    
    # Görseli göster
    finder.show_image_with_instructions()
    
    # İnteraktif koordinat seçimi
    print("\nKoordinat seçim modu:")
    print("1. Manuel koordinat girişi")
    print("2. Otomatik metin alanı tespiti (deneysel)")
    
    choice = input("\nSeçiminiz (1/2): ").strip()
    
    if choice == "2":
        # Otomatik tespit
        regions = finder.analyze_image_for_text_regions()
        if regions:
            use_auto = input("\nOtomatik tespit edilen alanları kullanmak ister misiniz? (e/h): ").strip().lower()
            if use_auto == 'e':
                for i, (x, y, w, h) in enumerate(regions, 1):
                    finder.coordinates.append({
                        "id": i,
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "description": f"Otomatik tespit edilen alan {i}"
                    })
    
    # Manuel seçim (her zaman)
    finder.interactive_coordinate_selection()
    
    # Kaydet
    if finder.coordinates:
        save = input("\nKoordinatları config.json'a kaydetmek ister misiniz? (e/h): ").strip().lower()
        if save == 'e':
            finder.save_coordinates_to_config()
    
    print("\nİşlem tamamlandı!")


if __name__ == "__main__":
    main()

