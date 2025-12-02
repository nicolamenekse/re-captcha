"""
OCR (Optik Karakter Tanıma) Modülü
Koordinatlardan numara okuma işlemleri
"""
import cv2
import numpy as np
import easyocr
from PIL import Image
from screenshot import ScreenshotCapture


class OCRReader:
    """OCR ile numara okuma sınıfı"""
    
    def __init__(self, languages=['en']):
        """
        OCR reader'ı başlatır
        
        Args:
            languages: Okunacak diller listesi (örn: ['en', 'tr'])
        """
        print("EasyOCR yükleniyor (ilk kullanımda modeller indirilecek)...")
        self.reader = easyocr.Reader(languages, gpu=False)  # GPU yoksa False
        print("EasyOCR hazır!")
        self.screenshot = ScreenshotCapture()
    
    def preprocess_image(self, image, threshold=127, invert=False, denoise=True):
        """
        Görüntüyü OCR için ön işleme yapar
        
        Args:
            image: numpy array görüntü
            threshold: Eşik değeri (0-255)
            invert: Renkleri tersine çevir (siyah-beyaz)
            denoise: Gürültü azaltma uygula
        
        Returns:
            İşlenmiş görüntü
        """
        # Gri tonlamaya çevir
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Gürültü azaltma
        if denoise:
            gray = cv2.medianBlur(gray, 3)
        
        # Threshold (eşikleme) - siyah-beyaz yap
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        
        # İnvert (tersine çevir)
        if invert:
            thresh = cv2.bitwise_not(thresh)
        
        return thresh
    
    def read_text_from_image(self, image, preprocess=True, threshold=127, invert=False):
        """
        Görüntüden metin okur
        
        Args:
            image: numpy array görüntü
            preprocess: Ön işleme uygula
            threshold: Eşik değeri
            invert: Renkleri tersine çevir
        
        Returns:
            Okunan metin (string)
        """
        # Ön işleme
        if preprocess:
            processed = self.preprocess_image(image, threshold, invert)
        else:
            processed = image
        
        # OCR ile oku
        results = self.reader.readtext(processed)
        
        # Sonuçları birleştir
        text = ""
        for (bbox, text_result, confidence) in results:
            if confidence > 0.5:  # Güven eşiği
                text += text_result + " "

        return text.strip()

    def read_text_from_region(self, x, y, width, height, preprocess=True, threshold=127, invert=False):
        """
        Belirli bir bölgeden SERBEST METİN okur (sadece rakam değil).

        Args:
            x, y, width, height: Bölge koordinatları
            preprocess: Ön işleme uygula
            threshold: Eşik değeri
            invert: Renkleri tersine çevir

        Returns:
            Okunan metin (string)
        """
        region = self.screenshot.capture_region(x, y, width, height)
        return self.read_text_from_image(region, preprocess=preprocess, threshold=threshold, invert=invert)
    
    def read_number_from_region(self, x, y, width, height, preprocess=True, threshold=127, invert=False):
        """
        Belirli bir bölgeden numara okur
        
        Args:
            x, y, width, height: Bölge koordinatları
            preprocess: Ön işleme uygula
            threshold: Eşik değeri
            invert: Renkleri tersine çevir
        
        Returns:
            Okunan numara (string)
        """
        # Bölgeyi yakala
        region = self.screenshot.capture_region(x, y, width, height)
        
        # OCR ile oku
        text = self.read_text_from_image(region, preprocess, threshold, invert)
        
        # Sadece rakamları al
        number = ''.join(filter(str.isdigit, text))
        
        return number
    
    def read_numbers_from_config(self, config_path="config.json", preprocess=True):
        """
        Config dosyasındaki tüm koordinatlardan numaraları okur
        
        Args:
            config_path: Config dosyası yolu
            preprocess: Ön işleme uygula
        
        Returns:
            Koordinat ID'si ve okunan numara dict'i
        """
        import json
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            print(f"Config dosyası bulunamadı: {config_path}")
            return {}
        
        coordinates = config.get("coordinates", {}).get("number_positions", [])
        ocr_settings = config.get("ocr_settings", {})
        
        threshold = ocr_settings.get("threshold", 127)
        invert = ocr_settings.get("invert", False)
        
        results = {}
        
        for coord in coordinates:
            coord_id = coord.get("id", 0)
            x = coord.get("x", 0)
            y = coord.get("y", 0)
            width = coord.get("width", 100)
            height = coord.get("height", 50)
            
            print(f"Koordinat {coord_id} okunuyor... ({x}, {y}, {width}x{height})")
            
            number = self.read_number_from_region(
                x, y, width, height,
                preprocess=preprocess if ocr_settings.get("preprocess", True) else False,
                threshold=threshold,
                invert=invert
            )
            
            results[coord_id] = number
            print(f"  → Okunan: '{number}'")
        
        return results
    
    def save_preprocessed_image(self, image, filename="preprocessed.png", threshold=127, invert=False):
        """Ön işlenmiş görüntüyü kaydeder (test için)"""
        processed = self.preprocess_image(image, threshold, invert)
        Image.fromarray(processed).save(filename)
        print(f"Ön işlenmiş görüntü kaydedildi: {filename}")


if __name__ == "__main__":
    # Test kodu
    print("=" * 60)
    print("OCR READER TEST")
    print("=" * 60)
    
    # OCR reader'ı başlat
    ocr = OCRReader()
    
    # Test görüntüsü yükle (varsa)
    import os
    if os.path.exists("test_region.png"):
        print("\nTest görüntüsü yükleniyor: test_region.png")
        test_image = cv2.imread("test_region.png")
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        
        # Ön işleme testi
        print("\nÖn işleme uygulanıyor...")
        ocr.save_preprocessed_image(test_image, "test_preprocessed.png")
        
        # OCR testi
        print("\nOCR ile okunuyor...")
        text = ocr.read_text_from_image(test_image)
        print(f"Okunan metin: '{text}'")
        
        # Sadece rakamlar
        numbers = ''.join(filter(str.isdigit, text))
        print(f"Okunan rakamlar: '{numbers}'")
    else:
        print("\nTest görüntüsü bulunamadı (test_region.png)")
        print("Önce 'python screenshot.py' çalıştırın")
    
    # Config'den okuma testi
    print("\n" + "=" * 60)
    print("Config'den koordinat okuma testi:")
    print("=" * 60)
    results = ocr.read_numbers_from_config()
    
    if results:
        print("\nSonuçlar:")
        for coord_id, number in results.items():
            print(f"  Koordinat {coord_id}: {number}")
    else:
        print("Config'de koordinat bulunamadı veya okunamadı")

