"""
Ekran Klavyesi (On-Screen Keyboard) Input Yöntemi
Windows ekran klavyesini kullanarak input gönderir
KGuard'ı atlatabilir çünkü gerçek mouse tıklamaları kullanır
"""
import time
import pyautogui
import subprocess
import os
import json

try:
    import win32gui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class OnScreenKeyboard:
    """Windows ekran klavyesi kontrolü"""
    
    def __init__(self):
        self.osk_process = None
        self.osk_hwnd = None
        self.key_positions = {}
        # Kalibrasyon dosyası (kalıcı)
        self.calibration_file = os.path.join(os.path.dirname(__file__), "osk_calibration.json")
        # Varsa önceki kalibrasyonu yükle
        self._load_calibration()

    def _load_calibration(self):
        """Daha önce kaydedilmiş tuş pozisyonlarını yükler"""
        try:
            if os.path.exists(self.calibration_file):
                with open(self.calibration_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and data:
                    # Anahtarlar string, değerler [x, y] listesi bekleniyor
                    self.key_positions = {k: tuple(v) for k, v in data.items()}
                    print(f"✓ OSK kalibrasyonu yüklendi ({len(self.key_positions)} tuş)")
        except Exception as e:
            print(f"Kalibrasyon yükleme hatası (yoksayılıyor): {e}")

    def _save_calibration(self):
        """Mevcut tuş pozisyonlarını kalıcı dosyaya kaydeder"""
        try:
            if self.key_positions:
                with open(self.calibration_file, "w", encoding="utf-8") as f:
                    json.dump(self.key_positions, f, ensure_ascii=False, indent=2)
                print(f"✓ OSK kalibrasyonu kaydedildi: {self.calibration_file}")
        except Exception as e:
            print(f"Kalibrasyon kaydetme hatası (yoksayılıyor): {e}")
        
    def start_osk(self):
        """Ekran klavyesini bulur (manuel açık olmalı) ve GEREKİRSE kalibre eder"""
        try:
            # Artık OSK'yi biz başlatmıyoruz, sadece var mı diye bakıyoruz
            if self.find_osk_window():
                print("✓ Ekran klavyesi bulundu (manuel açık)")
                # Eğer daha önce kalibrasyon yapılmadıysa şimdi iste
                if not self.key_positions:
                    self.calculate_key_positions()
                    self._save_calibration()
                else:
                    print("✓ Mevcut kalibrasyon kullanılacak (yeniden sormayacak)")
                return True

            print("✗ Ekran klavyesi bulunamadı.")
            print("  ➜ Lütfen Windows ekran klavyesini (osk.exe) MANUEL olarak açın")
            print("  ➜ Sonra scripti tekrar çalıştırın")
            return False
        except Exception as e:
            print(f"✗ Ekran klavyesi bulma hatası: {e}")
            return False
    
    def find_osk_window(self):
        """Ekran klavyesi penceresini bulur"""
        if not WIN32_AVAILABLE:
            return False
        
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                class_name = win32gui.GetClassName(hwnd)
                window_text = win32gui.GetWindowText(hwnd)
                # Ekran klavyesi penceresi
                if "OSK" in class_name.upper() or "On-Screen Keyboard" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            self.osk_hwnd = windows[0]
            return True
        return False
    
    def calculate_key_positions(self):
        """Klavye tuşlarının ekran koordinatlarını hesaplar (manuel kalibrasyon)"""
        # win32 koordinatları -32000 gibi anlamsız geldiği için
        # doğrudan kullanıcıdan mouse pozisyonu ile kalibre ediyoruz.
        try:
            print("=== EKRAN KLAVYESİ TUŞ KALİBRASYONU ===")
            print("Lütfen ekran klavyesini görünür ve sabit bir yerde tut.")
            print("Şimdi sırasıyla tuşların ÜZERİNE mouse'u getir ve ENTER'a bas.")
            print("Her tuş için mouse'u tuşun üstüne getirip terminal'e dön ve ENTER'a bas.\n")
            time.sleep(2)

            # 0-9 sırasıyla
            for digit in range(10):
                key = str(digit)
                print(f"\n[{key}] tuşu için:")
                print(f"  1. Mouse'u OSK'deki '{key}' tuşunun ÜZERİNE getir")
                print(f"  2. Terminal'e dön ve ENTER'a bas")
                input("  Hazır olduğunuzda ENTER'a basın...")
                x, y = pyautogui.position()
                self.key_positions[key] = (x, y)
                print(f"  ✓ '{key}' tuşu kaydedildi: ({x}, {y})")

            print("\n✓ Tüm tuş pozisyonları kaydedildi.")
        except Exception as e:
            print(f"✗ Tuş pozisyonları hesaplama hatası: {e}")
    
    def click_key(self, key):
        """
        Ekran klavyesinde bir tuşa tıklar
        
        Args:
            key: Tıklanacak tuş (0-9 veya karakter)
        """
        if not self.osk_hwnd:
            print("✗ Ekran klavyesi bulunamadı")
            return False
        
        try:
            # Tuş pozisyonunu al
            if key in self.key_positions:
                x, y = self.key_positions[key]
            else:
                # Eğer pozisyon bilinmiyorsa, ekran klavyesi penceresine tıkla
                # ve sonra tuşu bulmaya çalış
                rect = win32gui.GetWindowRect(self.osk_hwnd)
                # Yaklaşık pozisyon (ekran klavyesinin layout'una göre)
                x = rect[0] + 100 + (ord(key) - ord('0')) * 40
                y = rect[1] + 100
            
            # Tuşa tıkla
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(x, y, duration=0.1)
            time.sleep(0.1)
            pyautogui.click(x, y)
            time.sleep(0.1)
            
            print(f"✓ Tuş '{key}' tıklandı: ({x}, {y})")
            return True
        except Exception as e:
            print(f"✗ Tuş tıklama hatası: {e}")
            return False
    
    def type_text(self, text):
        """
        Ekran klavyesi ile metin yazar
        
        Args:
            text: Yazılacak metin
        """
        if not self.start_osk():
            return False
        
        print(f"Ekran klavyesi ile yazılıyor: '{text}'")
        
        for char in text:
            # Hem rakam hem harfleri destekle
            self.click_key(char)
            time.sleep(0.15)  # Her tuş arası bekleme
        
        print("✓ Ekran klavyesi ile yazma tamamlandı")
        return True
    
    def close_osk(self):
        """Ekran klavyesini kapatır (sadece bizim açtığımızı)"""
        try:
            if self.osk_process:
                self.osk_process.terminate()
                self.osk_process = None
                self.osk_hwnd = None
                print("✓ Ekran klavyesi kapatıldı (bizim açtığımız)")
            else:
                # Manuel açılmış OSK'ye dokunma
                print("ℹ Ekran klavyesi manuel açık, script kapatmayacak")
        except Exception as e:
            print(f"✗ Ekran klavyesi kapatma hatası: {e}")


class OnScreenKeyboardAuto:
    """
    Otomatik ekran klavyesi kontrolü
    Ekran klavyesini açıp tuşları otomatik tıklar
    """
    
    def __init__(self):
        self.osk = OnScreenKeyboard()
    
    def type_with_osk(self, text, input_field_pos=None):
        """
        Ekran klavyesi ile metin yazar
        
        Args:
            text: Yazılacak metin
            input_field_pos: Input field koordinatları (x, y) - önce tıklanır
        """
        try:
            # 1. Input field'e tıkla (eğer koordinatlar verildiyse)
            if input_field_pos:
                x, y = input_field_pos
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(x, y, duration=0.1)
                time.sleep(0.1)
                pyautogui.click(x, y)
                time.sleep(0.3)
                print(f"✓ Input field'e tıklandı: ({x}, {y})")
            
            # 2. Ekran klavyesini başlat
            if not self.osk.start_osk():
                print("✗ Ekran klavyesi başlatılamadı")
                return False
            
            # 3. Ekran klavyesi penceresini öne getir (ama input field'e odak kalır)
            if self.osk.osk_hwnd and WIN32_AVAILABLE:
                try:
                    # Ekran klavyesini göster ama input field'e odak kal
                    win32gui.ShowWindow(self.osk.osk_hwnd, win32con.SW_SHOW)
                    time.sleep(0.2)
                except:
                    pass
            
            # 4. Her karakter için tuşa tıkla
            print(f"Ekran klavyesi ile yazılıyor: '{text}'")
            for char in text:
                # Hem rakam hem harfleri destekle
                self.osk.click_key(char)
                time.sleep(0.2)  # Her tuş arası bekleme
            
            print("✓ Ekran klavyesi ile yazma tamamlandı")
            return True
        except Exception as e:
            print(f"✗ Ekran klavyesi yazma hatası: {e}")
            return False
    
    def cleanup(self):
        """Temizlik"""
        self.osk.close_osk()


def test_onscreen_keyboard():
    """Ekran klavyesi testi"""
    print("=" * 60)
    print("EKRAN KLAVYESİ TEST")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ:")
    print("1. Oyun penceresini açın")
    print("2. Input field'e tıklayın")
    print("3. 5 saniye içinde hazır olun...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Test
    osk_auto = OnScreenKeyboardAuto()

    # Input field koordinatlarını config.json'dan almaya çalış
    input_field_pos = None
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        inp = cfg.get("coordinates", {}).get("input_field", {})
        cx = inp.get("x")
        cy = inp.get("y")
        if cx is not None and cy is not None:
            # Kutu merkezini al
            w = inp.get("width", 0)
            h = inp.get("height", 0)
            input_field_pos = (cx + w // 2, cy + h // 2)
    except Exception as e:
        print(f"ℹ config.json okunamadı, ekran ortası kullanılacak: {e}")

    # Eğer config yoksa ekran ortasını kullan
    if input_field_pos is None:
        screen_width, screen_height = pyautogui.size()
        input_field_pos = (screen_width // 2, screen_height // 2)
    
    print(f"\nInput field pozisyonu: {input_field_pos}")
    print("Ekran klavyesi ile yazılıyor...")
    
    result = osk_auto.type_with_osk("1234", input_field_pos)
    
    if result:
        print("\n✓ Test başarılı!")
    else:
        print("\n✗ Test başarısız!")
    
    # Temizlik
    time.sleep(2)
    osk_auto.cleanup()


if __name__ == "__main__":
    test_onscreen_keyboard()

