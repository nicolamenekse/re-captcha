"""
ReCAPTCHA Çözücü - Ana Akış
Screenshot -> OCR -> Yazma -> Enter döngüsü
"""
import json
import time
import pyautogui
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader
from input_simulator import InputSimulator
from window_manager import WindowManager, find_game_window

# WIN32_AVAILABLE kontrolü
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class ReCaptchaSolver:
    """ReCAPTCHA çözücü ana sınıfı"""
    
    def __init__(self, config_path="config.json"):
        """
        Çözücüyü başlatır
        
        Args:
            config_path: Konfigürasyon dosyası yolu
        """
        self.config_path = config_path
        self.config = self.load_config()
        
        # Modülleri başlat
        print("Modüller yükleniyor...")
        self.screenshot = ScreenshotCapture()
        self.ocr = OCRReader()
        self.input_sim = InputSimulator()
        
        # Oyun penceresi yöneticisi
        game_settings = self.config.get("game_settings", {})
        window_name = game_settings.get("window_name", "")
        
        self.window_manager = WindowManager(window_name)
        if window_name:
            print(f"Oyun penceresi aranıyor: {window_name}")
            self.window_manager.find_window(window_name)
        else:
            print("Oyun penceresi otomatik aranıyor...")
            result = find_game_window()
            if result:
                hwnd, title = result
                print(f"Pencere bulundu: {title}")
                self.window_manager.window_handle = hwnd
        
        print("Tüm modüller hazır!")
    
    def load_config(self):
        """Konfigürasyon dosyasını yükler"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config dosyası bulunamadı: {self.config_path}")
            return {}
    
    def read_number_from_ocr_area(self):
        """
        OCR alanından numarayı okur
        
        Returns:
            Okunan numara (string)
        """
        print("\n" + "=" * 60)
        print("OCR İLE NUMARA OKUMA")
        print("=" * 60)
        
        coordinates = self.config.get("coordinates", {})
        ocr_area = coordinates.get("ocr_area", {})
        
        if not ocr_area or ocr_area.get("x") == 0:
            print("Uyarı: OCR alanı koordinatları tanımlı değil!")
            return None
        
        x = ocr_area.get("x", 0)
        y = ocr_area.get("y", 0)
        width = ocr_area.get("width", 200)
        height = ocr_area.get("height", 100)
        
        print(f"OCR alanı (config koordinatları): ({x}, {y}, {width}x{height})")
        
        # Eğer window manager varsa, koordinatları pencere içi olarak kullan
        # Aksi halde ekran koordinatları olarak kullan
        if self.window_manager.window_handle:
            # Pencere client rect'i al
            client_rect = self.window_manager.get_client_rect()
            if client_rect:
                # Koordinatları ekran koordinatlarına çevir
                screen_x = client_rect[0] + x
                screen_y = client_rect[1] + y
                print(f"Pencere client rect: {client_rect}")
                print(f"Ekran koordinatlarına çevrildi: ({screen_x}, {screen_y})")
            else:
                # Fallback: direkt kullan
                screen_x, screen_y = x, y
                print("Client rect alınamadı, direkt koordinatlar kullanılıyor")
        else:
            screen_x, screen_y = x, y
            print("Window manager yok, direkt koordinatlar kullanılıyor")
        
        # OCR ayarları
        ocr_settings = self.config.get("ocr_settings", {})
        preprocess = ocr_settings.get("preprocess", True)
        threshold = ocr_settings.get("threshold", 127)
        invert = ocr_settings.get("invert", False)
        
        # Numara oku - farklı ayarlarla dene
        number = None
        
        # İlk deneme: Varsayılan ayarlar
        number = self.ocr.read_number_from_region(
            screen_x, screen_y, width, height,
            preprocess=preprocess,
            threshold=threshold,
            invert=invert
        )
        
        print(f"Okunan numara (1. deneme): '{number}'")
        
        # Eğer okunamadıysa, farklı ayarlarla dene
        if not number:
            print("\nFarklı OCR ayarları deneniyor...")
            
            # Deneme 2: Threshold değiştir
            for test_threshold in [100, 150, 180]:
                print(f"Threshold {test_threshold} deneniyor...")
                number = self.ocr.read_number_from_region(
                    screen_x, screen_y, width, height,
                    preprocess=True,
                    threshold=test_threshold,
                    invert=False
                )
                if number:
                    print(f"✓ Threshold {test_threshold} ile okundu: '{number}'")
                    break
            
            # Deneme 3: Invert ile
            if not number:
                print("Invert ile deneniyor...")
                for test_threshold in [127, 100, 150]:
                    number = self.ocr.read_number_from_region(
                        screen_x, screen_y, width, height,
                        preprocess=True,
                        threshold=test_threshold,
                        invert=True
                    )
                    if number:
                        print(f"✓ Invert + threshold {test_threshold} ile okundu: '{number}'")
                        break
        
        # Eğer hala okunamadıysa, debug için screenshot kaydet
        if not number:
            print("\n⚠ Numara okunamadı! Debug screenshot kaydediliyor...")
            try:
                region = self.screenshot.capture_region(screen_x, screen_y, width, height)
                self.screenshot.save_screenshot(region, "debug_ocr_failed.png")
                print("Debug screenshot kaydedildi: debug_ocr_failed.png")
                print("Lütfen bu görüntüyü kontrol edin!")
                print(f"Koordinatlar: ({screen_x}, {screen_y}, {width}x{height})")
                print("Kontrol edin:")
                print("1. Captcha görünüyor mu?")
                print("2. Koordinatlar doğru mu?")
                print("3. Oyun penceresi aktif mi?")
            except Exception as e:
                print(f"Screenshot kaydedilemedi: {e}")
        else:
            print(f"\n✓ Final okunan numara: '{number}'")
        
        return number
    
    def solve_once(self, wait_before: float = 1.0):
        """
        Tek bir çözüm döngüsü çalıştırır:
        1. OCR ile numarayı okur (1 numaralı alan)
        2. Input field'e tıklar (2 numaralı alan)
        3. Numarayı yazar
        4. Confirm butonuna tıklar (3 numaralı alan)
        
        Args:
            wait_before: İşlem öncesi bekleme süresi
        
        Returns:
            Okunan numara (string)
        """
        print("\n" + "=" * 60)
        print("ÇÖZÜM DÖNGÜSÜ BAŞLIYOR")
        print("=" * 60)
        
        # Bekle
        if wait_before > 0:
            print(f"\n{wait_before} saniye bekleniyor...")
            time.sleep(wait_before)
        
        # Oyun penceresine odaklan
        game_settings = self.config.get("game_settings", {})
        window_name = game_settings.get("window_name", "")
        
        # Window manager ile odaklan
        if self.window_manager.window_handle:
            print("Oyun penceresine odaklanılıyor (Window Manager)...")
            self.window_manager.focus_window()
            time.sleep(0.5)
        else:
            print("Oyun penceresine odaklanılıyor (manuel)...")
            self.input_sim.focus_window(window_name)
        
        # 1. OCR ile numara oku
        number = self.read_number_from_ocr_area()
        
        if not number:
            print("\nUyarı: Numara okunamadı!")
            return None
        
        # Ayarları al
        typing_delay = game_settings.get("typing_delay_ms", 50) / 1000.0
        click_delay = game_settings.get("click_delay_ms", 100) / 1000.0
        wait_after_ocr = game_settings.get("wait_after_ocr_ms", 200) / 1000.0
        wait_after_typing = game_settings.get("wait_after_typing_ms", 100) / 1000.0
        
        # Koordinatları al
        coordinates = self.config.get("coordinates", {})
        input_field = coordinates.get("input_field", {})
        confirm_button = coordinates.get("confirm_button", {})
        
        # 2. Input field'e tıkla
        print("\n" + "=" * 60)
        print("INPUT FIELD'E TIKLANIYOR")
        print("=" * 60)
        
        if input_field and input_field.get("x") != 0:
            input_x = input_field.get("x", 0)
            input_y = input_field.get("y", 0)
            input_w = input_field.get("width", 200)
            input_h = input_field.get("height", 30)
            input_center_x = input_x + input_w // 2
            input_center_y = input_y + input_h // 2
            
            print(f"Input field koordinatları (config): ({input_x}, {input_y}, {input_w}x{input_h})")
            print(f"Input field merkezi (config): ({input_center_x}, {input_center_y})")
            
            # Koordinatları ekran koordinatlarına çevir
            if self.window_manager.window_handle:
                client_rect = self.window_manager.get_client_rect()
                if client_rect:
                    screen_center_x = client_rect[0] + input_center_x
                    screen_center_y = client_rect[1] + input_center_y
                    print(f"Ekran koordinatları: ({screen_center_x}, {screen_center_y})")
                else:
                    window_rect = self.window_manager.get_window_rect()
                    if window_rect:
                        screen_center_x = window_rect[0] + input_center_x
                        screen_center_y = window_rect[1] + input_center_y
                    else:
                        screen_center_x, screen_center_y = input_center_x, input_center_y
            else:
                screen_center_x, screen_center_y = input_center_x, input_center_y
            
            print(f"Mevcut mouse pozisyonu: {pyautogui.position()}")
            
            # Window manager ile tıkla (oyun penceresi içinde)
            print("Input field'e tıklanıyor (Window Manager ile)...")
            if self.window_manager.window_handle:
                # Pencere içi koordinatları kullan
                self.window_manager.click_in_window(input_center_x, input_center_y, relative=True)
                time.sleep(0.3)
            else:
                # Fallback: Normal tıklama
                print("Window Manager yok, normal tıklama deneniyor...")
                original_failsafe = pyautogui.FAILSAFE
                pyautogui.FAILSAFE = False
                try:
                    pyautogui.moveTo(screen_center_x, screen_center_y, duration=0.5)
                    time.sleep(0.3)
                except:
                    pass
                pyautogui.FAILSAFE = original_failsafe
                self.input_sim.click(screen_center_x, screen_center_y, 0.3)
            
            print(f"Bekleniyor: {wait_after_ocr}s")
            time.sleep(wait_after_ocr)
            
            # Input field'in aktif olduğundan emin olmak için tekrar tıkla
            print("Input field tekrar tıklanıyor (aktif olması için)...")
            if self.window_manager.window_handle:
                self.window_manager.click_in_window(input_center_x, input_center_y, relative=True)
            else:
                pyautogui.click(screen_center_x, screen_center_y, clicks=2, interval=0.1)
            time.sleep(0.5)
        else:
            print("Uyarı: Input field koordinatları tanımlı değil!")
            print("Direkt yazma deneniyor...")
        
        # 3. Numarayı yaz
        print("\n" + "=" * 60)
        print("NUMARA YAZILIYOR")
        print("=" * 60)
        print(f"Yazılacak numara: '{number}'")
        
        # KRİTİK: Input field'e tıkladıktan HEMEN SONRA yaz (timing çok önemli!)
        # Oyun muhtemelen sadece çok kısa bir süre input kabul ediyor
        
        # Pencereye odaklan (son kez)
        if self.window_manager.window_handle:
            self.window_manager.focus_window()
            time.sleep(0.1)  # Çok kısa bekle
        
        # Input field'e tıkla ve HEMEN yaz (timing kritik!)
        if input_field and input_field.get("x") != 0:
            input_center_x = input_field.get("x", 0) + input_field.get("width", 200) // 2
            input_center_y = input_field.get("y", 0) + input_field.get("height", 30) // 2
            
            client_rect = self.window_manager.get_client_rect() if self.window_manager.window_handle else None
            if client_rect:
                screen_x = client_rect[0] + input_center_x
                screen_y = client_rect[1] + input_center_y
            else:
                screen_x, screen_y = input_center_x, input_center_y
            
            print(f"Input field'e tıklanıyor: ({screen_x}, {screen_y})")
            original_failsafe = pyautogui.FAILSAFE
            pyautogui.FAILSAFE = False
            try:
                # Tıkla ve input field'i aktif et
                pyautogui.moveTo(screen_x, screen_y, duration=0.1)
                time.sleep(0.1)
                pyautogui.click(screen_x, screen_y)
                time.sleep(0.2)  # Input field'in aktif olması için bekle
                
                # Pencereye tekrar odaklan (input field aktifken)
                if self.window_manager.window_handle:
                    self.window_manager.focus_window()
                    time.sleep(0.1)
                
                # Hardware-level input ile yaz (tüm yöntemleri dene)
                print("Hardware-level input ile yazılıyor...")
                written = False
                
                # Yöntem 1: Hardware-level SendInput (scan code ile)
                if self.window_manager.window_handle and WIN32_AVAILABLE:
                    try:
                        import ctypes
                        user32 = ctypes.windll.user32
                        
                        PUL = ctypes.POINTER(ctypes.c_ulong)
                        
                        class KeyBdInput(ctypes.Structure):
                            _fields_ = [("wVk", ctypes.c_ushort),
                                       ("wScan", ctypes.c_ushort),
                                       ("dwFlags", ctypes.c_ulong),
                                       ("time", ctypes.c_ulong),
                                       ("dwExtraInfo", PUL)]
                        
                        class Input_I(ctypes.Union):
                            _fields_ = [("ki", KeyBdInput)]
                        
                        class Input(ctypes.Structure):
                            _fields_ = [("type", ctypes.c_ulong),
                                       ("ii", Input_I)]
                        
                        print("  → Hardware-level SendInput (scan code) deneniyor...")
                        for char in number:
                            if char.isdigit():
                                vk_code = ord(char)
                                scan_code = user32.MapVirtualKeyW(vk_code, 0)
                                
                                extra = ctypes.c_ulong(0)
                                ii_ = Input_I()
                                
                                # KEYDOWN
                                ii_.ki = KeyBdInput(vk_code, scan_code, 0, 0, ctypes.pointer(extra))
                                x = Input(ctypes.c_ulong(1), ii_)
                                result_down = user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                                time.sleep(0.01)
                                
                                # KEYUP
                                ii_.ki = KeyBdInput(vk_code, scan_code, 2, 0, ctypes.pointer(extra))
                                x = Input(ctypes.c_ulong(1), ii_)
                                result_up = user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                                time.sleep(0.01)
                                
                                print(f"    '{char}' gönderildi (down={result_down}, up={result_up})")
                        
                        written = True
                        print("  ✓ Hardware-level SendInput tamamlandı")
                    except Exception as e:
                        print(f"  ✗ Hardware-level SendInput hatası: {e}")
                
                # Yöntem 2: keyboard kütüphanesi
                if not written:
                    try:
                        import keyboard
                        print("  → keyboard kütüphanesi deneniyor...")
                        for char in number:
                            keyboard.write(char, delay=0.05)
                            time.sleep(0.05)
                            print(f"    '{char}' gönderildi")
                        written = True
                        print("  ✓ keyboard kütüphanesi tamamlandı")
                    except ImportError:
                        print("  ✗ keyboard kütüphanesi bulunamadı")
                    except Exception as e:
                        print(f"  ✗ keyboard hatası: {e}")
                
                # Yöntem 3: Window Manager
                if not written and self.window_manager.window_handle:
                    print("  → Window Manager send_text_to_window deneniyor...")
                    try:
                        self.window_manager.send_text_to_window(number)
                        written = True
                        print("  ✓ Window Manager tamamlandı")
                    except Exception as e:
                        print(f"  ✗ Window Manager hatası: {e}")
                
                # Yöntem 4: PyAutoGUI (son çare)
                if not written:
                    print("  → PyAutoGUI deneniyor (son çare)...")
                    try:
                        original_failsafe = pyautogui.FAILSAFE
                        pyautogui.FAILSAFE = False
                        for char in number:
                            pyautogui.write(char, interval=0.1)
                            time.sleep(0.1)
                            print(f"    '{char}' gönderildi")
                        pyautogui.FAILSAFE = original_failsafe
                        written = True
                        print("  ✓ PyAutoGUI tamamlandı")
                    except Exception as e:
                        print(f"  ✗ PyAutoGUI hatası: {e}")
                
                if written:
                    print(f"✓ Yazma işlemi tamamlandı (ancak oyun input'u kabul etmeyebilir!)")
                else:
                    print("✗ Tüm yöntemler başarısız!")
                
            except Exception as e:
                print(f"Yazma hatası: {e}")
            finally:
                pyautogui.FAILSAFE = original_failsafe
        
        time.sleep(wait_after_typing)
        print("✓ Yazma işlemi tamamlandı")
        time.sleep(0.3)
        
        # 4. Confirm butonuna tıkla
        print("\n" + "=" * 60)
        print("CONFIRM BUTONUNA TIKLANIYOR")
        print("=" * 60)
        
        if confirm_button and confirm_button.get("x") != 0:
            confirm_x = confirm_button.get("x", 0)
            confirm_y = confirm_button.get("y", 0)
            confirm_w = confirm_button.get("width", 100)
            confirm_h = confirm_button.get("height", 30)
            confirm_center_x = confirm_x + confirm_w // 2
            confirm_center_y = confirm_y + confirm_h // 2
            
            print(f"Confirm button koordinatları (config): ({confirm_x}, {confirm_y}, {confirm_w}x{confirm_h})")
            print(f"Confirm button merkezi (config): ({confirm_center_x}, {confirm_center_y})")
            
            # Koordinatları ekran koordinatlarına çevir
            if self.window_manager.window_handle:
                client_rect = self.window_manager.get_client_rect()
                if client_rect:
                    screen_center_x = client_rect[0] + confirm_center_x
                    screen_center_y = client_rect[1] + confirm_center_y
                    print(f"Ekran koordinatları: ({screen_center_x}, {screen_center_y})")
                else:
                    window_rect = self.window_manager.get_window_rect()
                    if window_rect:
                        screen_center_x = window_rect[0] + confirm_center_x
                        screen_center_y = window_rect[1] + confirm_center_y
                    else:
                        screen_center_x, screen_center_y = confirm_center_x, confirm_center_y
            else:
                screen_center_x, screen_center_y = confirm_center_x, confirm_center_y
            
            print(f"Mevcut mouse pozisyonu: {pyautogui.position()}")
            
            # Window manager ile tıkla (oyun penceresi içinde)
            print("Confirm butonuna tıklanıyor (Window Manager ile)...")
            if self.window_manager.window_handle:
                # Pencere içi koordinatları kullan
                self.window_manager.click_in_window(confirm_center_x, confirm_center_y, relative=True)
                time.sleep(click_delay)
            else:
                # Fallback: Normal tıklama
                print("Window Manager yok, normal tıklama deneniyor...")
                original_failsafe = pyautogui.FAILSAFE
                pyautogui.FAILSAFE = False
                try:
                    pyautogui.moveTo(screen_center_x, screen_center_y, duration=0.5)
                    time.sleep(0.3)
                except:
                    pass
                pyautogui.FAILSAFE = original_failsafe
                self.input_sim.click(screen_center_x, screen_center_y, click_delay)
            
            print("\n✓ İşlem tamamlandı!")
        else:
            print("Uyarı: Confirm button koordinatları tanımlı değil!")
            print("ENTER tuşu kullanılıyor...")
            self.input_sim.press_enter(click_delay)
        
        return number
    
    def solve_continuous(self, interval: float = 2.0, max_iterations: int = None):
        """
        Sürekli çözüm döngüsü (otomatik tekrar)
        
        Args:
            interval: Her döngü arası bekleme süresi (saniye)
            max_iterations: Maksimum tekrar sayısı (None = sınırsız)
        """
        print("\n" + "=" * 60)
        print("SÜREKLI ÇÖZÜM MODU")
        print("=" * 60)
        print(f"Bekleme süresi: {interval} saniye")
        if max_iterations:
            print(f"Maksimum tekrar: {max_iterations}")
        else:
            print("Sınırsız tekrar (Ctrl+C ile durdurun)")
        print("=" * 60)
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n>>> İTERASYON {iteration} <<<")
                
                self.solve_once(wait_before=1.0)
                
                if max_iterations and iteration >= max_iterations:
                    print(f"\nMaksimum iterasyon sayısına ulaşıldı: {max_iterations}")
                    break
                
                print(f"\n{interval} saniye bekleniyor...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu.")


def main():
    """Ana program"""
    import sys
    
    print("=" * 60)
    print("ReCAPTCHA ÇÖZÜCÜ")
    print("=" * 60)
    
    solver = ReCaptchaSolver()
    
    # Komut satırı argümanları
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "once":
            # Tek seferlik çözüm
            solver.solve_once()
        elif command == "loop":
            # Sürekli döngü
            interval = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
            max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else None
            solver.solve_continuous(interval, max_iter)
        else:
            print(f"Bilinmeyen komut: {command}")
            print("Kullanım: python recaptcha_solver.py [once|loop] [interval] [max_iterations]")
    else:
        # İnteraktif mod
        print("\nMod seçin:")
        print("1. Tek seferlik çözüm")
        print("2. Sürekli döngü")
        
        choice = input("\nSeçiminiz (1/2): ").strip()
        
        if choice == "1":
            solver.solve_once()
        elif choice == "2":
            interval = input("Döngü arası bekleme (saniye, varsayılan 2.0): ").strip()
            interval = float(interval) if interval else 2.0
            max_iter = input("Maksimum tekrar (boş = sınırsız): ").strip()
            max_iter = int(max_iter) if max_iter else None
            solver.solve_continuous(interval, max_iter)
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()

