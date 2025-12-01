"""
Ekran görüntüsü alma modülü
"""
import mss
import numpy as np
from PIL import Image
import cv2


class ScreenshotCapture:
    """Ekran görüntüsü alma sınıfı"""
    
    def __init__(self):
        self.sct = mss.mss()
    
    def capture_full_screen(self):
        """Tüm ekranın görüntüsünü alır"""
        monitor = self.sct.monitors[1]  # Birincil monitör
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return np.array(img)
    
    def capture_region(self, x, y, width, height):
        """
        Belirli bir bölgenin görüntüsünü alır
        
        Args:
            x: Sol üst köşe X koordinatı
            y: Sol üst köşe Y koordinatı
            width: Genişlik
            height: Yükseklik
        
        Returns:
            numpy array olarak görüntü
        """
        monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return np.array(img)
    
    def capture_window(self, window_name=None):
        """
        Belirli bir pencereyi yakalar (gelecekte eklenebilir)
        Şimdilik tüm ekranı yakalar
        """
        return self.capture_full_screen()
    
    def save_screenshot(self, image, filename="screenshot.png"):
        """Görüntüyü dosyaya kaydeder"""
        if isinstance(image, np.ndarray):
            img = Image.fromarray(image)
        else:
            img = image
        img.save(filename)
        print(f"Görüntü kaydedildi: {filename}")
    
    def get_screen_size(self):
        """Ekran boyutlarını döndürür"""
        monitor = self.sct.monitors[1]
        return {
            "width": monitor["width"],
            "height": monitor["height"]
        }


if __name__ == "__main__":
    # Test kodu
    print("Ekran görüntüsü alma testi başlatılıyor...")
    
    capture = ScreenshotCapture()
    
    # Ekran boyutunu göster
    size = capture.get_screen_size()
    print(f"Ekran boyutu: {size['width']}x{size['height']}")
    
    # Tüm ekranın görüntüsünü al
    print("Tüm ekranın görüntüsü alınıyor...")
    screenshot = capture.capture_full_screen()
    capture.save_screenshot(screenshot, "test_full_screen.png")
    
    # Küçük bir bölge yakalama testi (sol üst 500x500)
    print("Bölge görüntüsü alınıyor (500x500)...")
    region = capture.capture_region(0, 0, 500, 500)
    capture.save_screenshot(region, "test_region.png")
    
    print("Test tamamlandı! Dosyaları kontrol edin.")

