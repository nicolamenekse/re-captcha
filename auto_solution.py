"""
Tam Otomatik ReCAPTCHA Çözücü
Tüm yöntemleri otomatik olarak dener ve en iyi çözümü bulur
"""
import json
import time
import pyautogui
import subprocess
import os
from pathlib import Path
from screenshot import ScreenshotCapture
from ocr_reader import OCRReader
from window_manager import WindowManager, find_game_window
try:
    from advanced_input import AdvancedInput
    ADVANCED_INPUT_AVAILABLE = True
except ImportError:
    ADVANCED_INPUT_AVAILABLE = False

try:
    from onscreen_keyboard import OnScreenKeyboardAuto
    OSK_AVAILABLE = True
except ImportError:
    OSK_AVAILABLE = False

try:
    import win32gui
    import win32con
    import win32process
    import win32api
    import ctypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class AutoReCaptchaSolver:
    """Tam otomatik ReCAPTCHA çözücü"""
    
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        
        # Modülleri başlat
        print("Modüller yükleniyor...")
        self.screenshot = ScreenshotCapture()
        self.ocr = OCRReader()
        
        # Oyun penceresi yöneticisi
        game_settings = self.config.get("game_settings", {})
        window_name = game_settings.get("window_name", "SeaSRO2025")
        self.window_manager = WindowManager(window_name)
        
        if window_name:
            print(f"Oyun penceresi aranıyor: {window_name}")
            self.window_manager.find_window(window_name)
        
        print("Tüm modüller hazır!")
    
    def load_config(self):
        """Config dosyasını yükler"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def read_number_from_ocr(self):
        """
        OCR alanından numarayı okur (daha detaylı log ve fallback'lerle)
        recaptcha_solver içindeki mantığın aynısını kullanır.
        """
        print("\n" + "=" * 60)
        print("OCR İLE NUMARA OKUMA (AUTO)")
        print("=" * 60)

        coordinates = self.config.get("coordinates", {})
        ocr_area = coordinates.get("ocr_area", {})

        if not ocr_area or ocr_area.get("x") == 0:
            print("Hata: OCR alanı koordinatları tanımlı değil!")
            return None

        x = ocr_area.get("x", 0)
        y = ocr_area.get("y", 0)
        width = ocr_area.get("width", 200)
        height = ocr_area.get("height", 100)

        print(f"OCR alanı (config koordinatları): ({x}, {y}, {width}x{height})")

        # Koordinatları ekran koordinatlarına çevir
        if self.window_manager.window_handle:
            client_rect = self.window_manager.get_client_rect()
            if client_rect:
                screen_x = client_rect[0] + x
                screen_y = client_rect[1] + y
                print(f"Pencere client rect: {client_rect}")
                print(f"Ekran koordinatlarına çevrildi: ({screen_x}, {screen_y})")
            else:
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
                self.screenshot.save_screenshot(region, "debug_auto_ocr_failed.png")
                print("Debug screenshot kaydedildi: debug_auto_ocr_failed.png")
                print(f"Koordinatlar: ({screen_x}, {screen_y}, {width}x{height})")
                print("Lütfen bu görüntüyü kontrol edin (captcha doğru alanda mı?)")
            except Exception as e:
                print(f"Screenshot kaydedilemedi: {e}")
        else:
            print(f"\n✓ Final okunan numara: '{number}'")

        return number

    # --------------------------------------------------------
    #  YAZI TETİKLEYİCİ: Ekrandaki belirli yazıyı bekle
    # --------------------------------------------------------
    def wait_for_trigger_text(self, trigger_texts, check_interval: float = 2.0):
        """
        Ekranda belirli bir / birden fazla yazı görünene kadar BEKLER.

        - config.coordinates.trigger_text_area alanını kullanır.
        - Bu alandaki metni OCR ile okuyup, trigger_text içeriyorsa True döner.

        Args:
            trigger_texts: Aranacak yazı(lar) (ör: ['Captcha gerekli', 'Captcha aktif'])
            check_interval: Her kontrol arasında beklenecek süre (saniye)
        """
        # Tek string geldiyse listeye çevir
        if isinstance(trigger_texts, str):
            trigger_texts = [trigger_texts]

        # Boşları temizle
        trigger_texts = [t.strip() for t in trigger_texts if t and t.strip()]

        if not trigger_texts:
            print("✗ trigger_texts boş olamaz!")
            return False

        coords = self.config.get("coordinates", {})
        area = coords.get("trigger_text_area", {})

        if not area or area.get("width", 0) <= 0 or area.get("height", 0) <= 0:
            print("✗ trigger_text_area koordinatları config.json içinde tanımlı değil.")
            print("  → Önce: python setup_trigger_text_area.py")
            return False

        x = area.get("x", 0)
        y = area.get("y", 0)
        width = area.get("width", 200)
        height = area.get("height", 50)

        print("=" * 60)
        print("TETİK YAZI BEKLEME MODU")
        print("=" * 60)
        print("Aranan yazılar:")
        for t in trigger_texts:
            print(f"  - '{t}'")
        print(f"Tetik alanı (config): ({x}, {y}, {width}x{height})")
        print(f"Kontrol aralığı: {check_interval} saniye")
        print("Durdurmak için: Ctrl + C")

        # NOT: setup_trigger_text_area.py koordinatları DOĞRUDAN EKRAN KOORDİNATI olarak kaydediyor.
        # Bu yüzden burada ekstra client_rect ofseti EKLEMİYORUZ.
        screen_x, screen_y = x, y
        print(f"Ekran koordinatları (doğrudan config): ({screen_x}, {screen_y})")

        debug_saved = False
        try:
            while True:
                try:
                    # 1) Config'teki OCR ayarlarıyla dene
                    ocr_settings = self.config.get("ocr_settings", {})
                    preprocess = ocr_settings.get("preprocess", True)
                    threshold = ocr_settings.get("threshold", 127)
                    invert = ocr_settings.get("invert", False)

                    text = self.ocr.read_text_from_region(
                        screen_x,
                        screen_y,
                        width,
                        height,
                        preprocess=preprocess,
                        threshold=threshold,
                        invert=invert,
                    )

                    # 2) Hâlâ boşsa, tetik alanı için özel birkaç kombinasyon daha dene
                    if not text:
                        for test_threshold in [100, 150, 180]:
                            text = self.ocr.read_text_from_region(
                                screen_x,
                                screen_y,
                                width,
                                height,
                                preprocess=True,
                                threshold=test_threshold,
                                invert=False,
                            )
                            if text:
                                break

                    if not text:
                        # Invert ile dene (yazı rengi/zeminine göre bazen işe yarıyor)
                        for test_threshold in [127, 100, 150]:
                            text = self.ocr.read_text_from_region(
                                screen_x,
                                screen_y,
                                width,
                                height,
                                preprocess=True,
                                threshold=test_threshold,
                                invert=True,
                            )
                            if text:
                                break

                    # 3) Hâlâ boşsa, küçük yazılar için özel: resmi büyüt ve ham OCR yap
                    if not text:
                        try:
                            import cv2
                            import numpy as np  # noqa: F401 - gelecekte kullanılabilir

                            region_img = self.screenshot.capture_region(screen_x, screen_y, width, height)
                            # Yazıyı daha okunur yapmak için ölçek büyüt
                            scaled = cv2.resize(region_img, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)

                            results = self.ocr.reader.readtext(scaled)
                            collected = []
                            for (_bbox, t_res, conf) in results:
                                if conf > 0.3:
                                    collected.append(t_res)
                            text = " ".join(collected).strip()
                        except Exception as e:
                            print(f"✗ Küçük yazı özel OCR hatası (yoksayılıyor): {e}")
                except Exception as e:
                    print(f"✗ OCR tetik alanı okuma hatası: {e}")
                    text = ""

                normalized = (text or "").strip().lower()
                targets_norm = [t.lower() for t in trigger_texts]

                print("-" * 60)
                print(f"Tetik alanında okunan: '{text}'")

                # Eğer hiç okuyamıyorsak, bir kere debug ekran görüntüsü kaydedelim
                if not text and not debug_saved:
                    try:
                        print("⚠ Tetik yazı okunamadı, debug görüntü kaydediliyor...")
                        region = self.screenshot.capture_region(screen_x, screen_y, width, height)
                        self.screenshot.save_screenshot(region, "debug_trigger_text_area.png")
                        print("Debug görüntü: debug_trigger_text_area.png")
                        print(f"Koordinatlar: ({screen_x}, {screen_y}, {width}x{height})")
                        debug_saved = True
                    except Exception as e:
                        print(f"Debug görüntü kaydedilemedi: {e}")

                for target_norm in targets_norm:
                    if target_norm and target_norm in normalized:
                        print(f"✓ Tetik yazı bulundu! (eşleşen: '{target_norm}')")
                        return True

                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu (Ctrl + C).")
            return False
    
    def try_all_input_methods(self, text):
        """
        Tüm input yöntemlerini dener (en etkili olanı bulur)
        
        Args:
            text: Yazılacak metin
        
        Returns:
            Başarılı olan yöntem veya None
        """
        if not self.window_manager.window_handle:
            print("Pencere bulunamadı!")
            return None
        
        hwnd = self.window_manager.window_handle
        
        # Pencereye odaklan
        self.window_manager.focus_window()
        time.sleep(0.2)
        
        # Input field koordinatları
        coordinates = self.config.get("coordinates", {})
        input_field = coordinates.get("input_field", {})
        
        if input_field and input_field.get("x", 0) != 0:
            input_center_x = input_field.get("x", 0) + input_field.get("width", 200) // 2
            input_center_y = input_field.get("y", 0) + input_field.get("height", 30) // 2
            
            client_rect = self.window_manager.get_client_rect()
            if client_rect:
                screen_x = client_rect[0] + input_center_x
                screen_y = client_rect[1] + input_center_y
            else:
                screen_x, screen_y = input_center_x, input_center_y
            
            # Input field'e tıkla
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            time.sleep(0.1)
            pyautogui.click(screen_x, screen_y)
            time.sleep(0.3)
        
        # Yöntem 0: Ekran Klavyesi (YENİ - En umut verici!)
        if OSK_AVAILABLE:
            try:
                print("Yöntem 0: Ekran Klavyesi (On-Screen Keyboard) deneniyor...")
                print("  Bu yöntem gerçek mouse tıklamaları kullanır, KGuard'ı atlatabilir!")
                
                # Input field koordinatlarını al
                input_field_pos = None
                if input_field and input_field.get("x", 0) != 0:
                    input_center_x = input_field.get("x", 0) + input_field.get("width", 200) // 2
                    input_center_y = input_field.get("y", 0) + input_field.get("height", 30) // 2
                    
                    client_rect = self.window_manager.get_client_rect()
                    if client_rect:
                        screen_x = client_rect[0] + input_center_x
                        screen_y = client_rect[1] + input_center_y
                    else:
                        screen_x, screen_y = input_center_x, input_center_y
                    
                    input_field_pos = (screen_x, screen_y)
                
                osk_auto = OnScreenKeyboardAuto()
                result = osk_auto.type_with_osk(text, input_field_pos)
                osk_auto.cleanup()
                
                if result:
                    print("✓ Ekran Klavyesi ile yazma başarılı!")
                    return "onscreen_keyboard"
            except Exception as e:
                print(f"✗ Ekran Klavyesi hatası: {e}")
        
        # Yöntem 0.5: Gelişmiş Input Yöntemleri (Arduino gelene kadar)
        if ADVANCED_INPUT_AVAILABLE:
            try:
                print("Yöntem 0: Gelişmiş Input Yöntemleri deneniyor...")
                advanced = AdvancedInput(hwnd)
                result = advanced.try_all_advanced_methods(text, hwnd)
                if result:
                    print(f"✓ Gelişmiş yöntem başarılı: {result}")
                    return result
            except Exception as e:
                print(f"✗ Gelişmiş yöntemler hatası: {e}")
        
        # Yöntem 1: SendMessage WM_CHAR (farklı parametrelerle)
        if WIN32_AVAILABLE:
            print("Yöntem 1: SendMessage WM_CHAR deneniyor (farklı parametrelerle)...")
            try:
                # Child window'ları bul
                child_windows = []
                def enum_child_proc(child_hwnd, lParam):
                    if win32gui.IsWindowVisible(child_hwnd):
                        class_name = win32gui.GetClassName(child_hwnd)
                        if 'edit' in class_name.lower():
                            child_windows.append(child_hwnd)
                    return True
                
                win32gui.EnumChildWindows(hwnd, enum_child_proc, None)
                
                print(f"  {len(child_windows)} child window bulundu")
                
                # Her karakter için farklı yöntemler dene
                for char in text:
                    if char.isdigit():
                        char_code = ord(char)
                        vk_code = ord(char.upper())
                        
                        # Child window'lara öncelik ver (input field olabilir)
                        for child_hwnd in child_windows:
                            try:
                                # WM_CHAR (farklı lParam değerleri)
                                win32gui.SendMessage(child_hwnd, win32con.WM_CHAR, char_code, 0)
                                time.sleep(0.01)
                                win32gui.SendMessage(child_hwnd, win32con.WM_CHAR, char_code, 1)
                                time.sleep(0.01)
                                
                                # WM_KEYDOWN + WM_KEYUP
                                win32gui.SendMessage(child_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                                time.sleep(0.01)
                                win32gui.SendMessage(child_hwnd, win32con.WM_KEYUP, vk_code, 0)
                                time.sleep(0.01)
                                
                                # WM_IME_CHAR (IME karakter mesajı)
                                try:
                                    win32gui.SendMessage(child_hwnd, 0x0286, char_code, 0)  # WM_IME_CHAR
                                except:
                                    pass
                                
                            except Exception as e:
                                pass
                        
                        # Ana pencereye de gönder (fallback)
                        try:
                            win32gui.SendMessage(hwnd, win32con.WM_CHAR, char_code, 0)
                        except:
                            pass
                        
                        time.sleep(0.1)  # Her karakter arası daha uzun bekleme
                
                print("✓ SendMessage WM_CHAR tamamlandı (tüm yöntemler denendi)")
                return "SendMessage"
            except Exception as e:
                print(f"✗ SendMessage hatası: {e}")
        
        # Yöntem 2: Hardware-level SendInput (scan code ile)
        if WIN32_AVAILABLE:
            print("Yöntem 2: Hardware-level SendInput deneniyor...")
            try:
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
                
                for char in text:
                    if char.isdigit():
                        vk_code = ord(char)
                        scan_code = user32.MapVirtualKeyW(vk_code, 0)
                        
                        extra = ctypes.c_ulong(0)
                        ii_ = Input_I()
                        
                        # KEYDOWN
                        ii_.ki = KeyBdInput(vk_code, scan_code, 0, 0, ctypes.pointer(extra))
                        x = Input(ctypes.c_ulong(1), ii_)
                        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                        time.sleep(0.01)
                        
                        # KEYUP
                        ii_.ki = KeyBdInput(vk_code, scan_code, 2, 0, ctypes.pointer(extra))
                        x = Input(ctypes.c_ulong(1), ii_)
                        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                        time.sleep(0.01)
                
                print("✓ Hardware-level SendInput tamamlandı")
                return "SendInput"
            except Exception as e:
                print(f"✗ SendInput hatası: {e}")
        
        # Yöntem 3: keyboard kütüphanesi
        try:
            import keyboard
            print("Yöntem 3: keyboard kütüphanesi deneniyor...")
            keyboard.write(text, delay=0.05)
            print("✓ keyboard kütüphanesi tamamlandı")
            return "keyboard"
        except:
            pass
        
        # Yöntem 4: Arduino USB HID Klavye (en etkili - gerçek hardware)
        try:
            from arduino_keyboard.arduino_controller import ArduinoKeyboard
            print("Yöntem 4: Arduino USB HID Klavye deneniyor...")
            keyboard = ArduinoKeyboard()
            if keyboard.type_text(text, delay_ms=50):
                keyboard.disconnect()
                print("✓ Arduino USB HID Klavye tamamlandı")
                return "arduino"
            keyboard.disconnect()
        except ImportError:
            print("⚠ Arduino kütüphanesi bulunamadı (arduino_keyboard klasörüne bakın)")
        except Exception as e:
            print(f"✗ Arduino hatası: {e}")
        
        # Yöntem 5: PyAutoGUI (son çare)
        print("Yöntem 5: PyAutoGUI deneniyor...")
        try:
            pyautogui.write(text, interval=0.05)
            print("✓ PyAutoGUI tamamlandı")
            return "pyautogui"
        except:
            pass
        
        return None
    
    def click_confirm_button(self):
        """Confirm butonuna tıklar"""
        coordinates = self.config.get("coordinates", {})
        confirm_button = coordinates.get("confirm_button", {})
        
        if not confirm_button or confirm_button.get("x", 0) == 0:
            print("Confirm button koordinatları tanımlı değil!")
            return False
        
        button_center_x = confirm_button.get("x", 0) + confirm_button.get("width", 200) // 2
        button_center_y = confirm_button.get("y", 0) + confirm_button.get("height", 30) // 2
        
        client_rect = self.window_manager.get_client_rect() if self.window_manager.window_handle else None
        if client_rect:
            screen_x = client_rect[0] + button_center_x
            screen_y = client_rect[1] + button_center_y
        else:
            screen_x, screen_y = button_center_x, button_center_y
        
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            time.sleep(0.1)
            pyautogui.click(screen_x, screen_y)
            print(f"✓ Confirm button'a tıklandı: ({screen_x}, {screen_y})")
            return True
        except Exception as e:
            print(f"✗ Confirm button tıklama hatası: {e}")
            return False
        finally:
            pyautogui.FAILSAFE = True
    
    def solve_once(self):
        """Tek seferlik çözüm"""
        print("=" * 60)
        print("OTOMATİK ReCAPTCHA ÇÖZÜCÜ")
        print("=" * 60)
        
        # 1. Numara oku
        print("\n1️⃣ Numara okunuyor...")
        number = self.read_number_from_ocr()
        
        if not number:
            print("✗ Numara okunamadı!")
            return False
        
        print(f"✓ Okunan numara: '{number}'")
        
        # 2. Numara yaz
        print("\n2️⃣ Numara yazılıyor (tüm yöntemler deneniyor)...")
        method = self.try_all_input_methods(number)
        
        if method:
            print(f"✓ Yazma tamamlandı (yöntem: {method})")
        else:
            print("⚠ Yazma yöntemleri denendi ama başarı garantisi yok")
        
        time.sleep(0.5)
        
        # 3. Confirm butonuna tıkla
        print("\n3️⃣ Confirm butonuna tıklanıyor...")
        self.click_confirm_button()
        
        print("\n✓ İşlem tamamlandı!")
        return True

    def solve_full_once(self, wait_after_trigger: float = 2.0):
        """
        TAM AKIŞ (tek sefer):
        1) Oyunda metin kutusuna 'captcha' yaz + ENTER (OSK ile)
        2) Kısa bir süre bekle (captcha penceresinin açılması için)
        3) Ekrandaki captcha numarasını OCR ile oku
        4) OSK ile oyundaki captcha input alanına yaz
        5) Confirm butonuna tıkla
        """
        print("=" * 60)
        print("TAM CAPTCHA AKIŞI (TRIGGER + OCR + YAZ + CONFIRM)")
        print("=" * 60)

        # 1) Chat üzerinden captchayı tetikle
        triggered = self.trigger_captcha_via_chat()
        if not triggered:
            print("✗ Captcha tetiklenemedi, işlem iptal.")
            return False

        # 2) Captcha penceresinin açılması için bekle
        print(f"\nCaptcha penceresinin açılması için {wait_after_trigger} saniye bekleniyor...")
        time.sleep(wait_after_trigger)

        # 3-5) Normal solve_once akışını çalıştır
        return self.solve_once()

    def trigger_captcha_via_chat(self):
        """
        Oyundaki metin kutusuna 'captcha' yazarak captcha penceresini tetikler.
        - coordinates.captcha_trigger_input alanını kullanır.
        - Yazma için On-Screen Keyboard (OSK) kalibrasyonunu kullanır.
        """
        print("=" * 60)
        print("CAPTCHA TETİKLEME (CHAT ÜZERİNDEN)")
        print("=" * 60)

        if not self.window_manager.window_handle:
            print("✗ Oyun penceresi bulunamadı, tetikleme iptal.")
            return False

        coords = self.config.get("coordinates", {})
        trigger = coords.get("captcha_trigger_input", {})

        if not trigger or trigger.get("x", 0) == 0:
            print("✗ captcha_trigger_input koordinatları config.json içinde tanımlı değil.")
            return False

        # Pencereye odaklan
        self.window_manager.focus_window()
        time.sleep(0.3)

        # Metin kutusunun merkezini hesapla
        tx = trigger.get("x", 0)
        ty = trigger.get("y", 0)
        tw = trigger.get("width", 200)
        th = trigger.get("height", 30)
        center_x = tx + tw // 2
        center_y = ty + th // 2

        client_rect = self.window_manager.get_client_rect()
        if client_rect:
            screen_x = client_rect[0] + center_x
            screen_y = client_rect[1] + center_y
        else:
            screen_x, screen_y = center_x, center_y

        print(f"Metin kutusu merkezi (ekran): ({screen_x}, {screen_y})")

        # Kutunun içine tıkla
        try:
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            time.sleep(0.1)
            pyautogui.click(screen_x, screen_y)
            time.sleep(0.3)
            print("✓ Metin kutusuna tıklandı.")
        except Exception as e:
            print(f"✗ Metin kutusuna tıklama hatası: {e}")
            return False

        # OSK ile 'captcha' yaz
        if not OSK_AVAILABLE:
            print("✗ On-Screen Keyboard modülü import edilemedi, tetikleme yapılamıyor.")
            return False

        try:
            print("OSK ile 'captcha' yazılıyor...")
            from onscreen_keyboard import OnScreenKeyboardAuto
            osk_auto = OnScreenKeyboardAuto()
            # input_field_pos olarak metin kutusunun ekran koordinatını veriyoruz
            result = osk_auto.type_with_osk("captcha", input_field_pos=(screen_x, screen_y))

            # Yazma başarılıysa, kalibre edilmiş 'enter' tuşuna da bas
            if result:
                try:
                    print("OSK ile ENTER tuşuna basılıyor...")
                    # OnScreenKeyboardAuto içindeki gerçek OSK nesnesini kullan
                    osk = osk_auto.osk
                    osk.click_key("enter")
                    time.sleep(0.3)
                except Exception as e:
                    print(f"ENTER tıklama hatası (yoksayılıyor): {e}")

                osk_auto.cleanup()
                print("✓ 'captcha' + ENTER gönderildi, captcha penceresinin açılması bekleniyor.")
                return True
            else:
                osk_auto.cleanup()
                print("✗ OSK ile 'captcha' yazma başarısız.")
                return False
        except Exception as e:
            print(f"✗ OSK tetikleme hatası: {e}")
            return False

    def solve_loop(self, interval: float = 2.0):
        """
        Captcha EKRANDAYKEN otomatik çözmeye devam eden döngü.

        Args:
            interval: Her deneme arasında beklenecek süre (saniye).
        """
        print("=" * 60)
        print("SÜREKLİ ReCAPTCHA ÇÖZÜM MODU")
        print("=" * 60)
        print(f"Her deneme arası bekleme: {interval} saniye")
        print("Durdurmak için: Ctrl + C")

        iteration = 0
        try:
            while True:
                iteration += 1
                print("\n" + "-" * 60)
                print(f"İTERASYON #{iteration}")
                print("-" * 60)

                success = self.solve_once()

                if not success:
                    print("Bu iterasyonda çözüm başarısız (muhtemelen captcha yok veya OCR okuyamadı).")

                print(f"\n{interval} saniye bekleniyor...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu (Ctrl + C).")

    def solve_full_loop(self, interval: float = 330.0, wait_after_trigger: float = 2.0):
        """
        TAM AKIŞ döngüsü:
        Her seferinde:
          1) Chat'e 'captcha' yaz + ENTER (OSK)
          2) Kısa bekle (captcha penceresinin açılması için)
          3) OCR + yaz + confirm

        Args:
            interval: Her tam döngü arasında bekleme süresi (saniye) -> 330 ≈ 5.5 dakika
            wait_after_trigger: 'captcha' yazdıktan sonra captcha penceresini bekleme (saniye)
        """
        print("=" * 60)
        print("SÜREKLİ TAM CAPTCHA AKIŞI (TRIGGER + OCR + YAZ + CONFIRM)")
        print("=" * 60)
        print(f"Her döngü arası bekleme: {interval} saniye")
        print("Durdurmak için: Ctrl + C")

        iteration = 0
        try:
            while True:
                iteration += 1
                print("\n" + "-" * 60)
                print(f"FULL İTERASYON #{iteration}")
                print("-" * 60)

                success = self.solve_full_once(wait_after_trigger=wait_after_trigger)
                if not success:
                    print("Bu tam iterasyonda işlem başarısız olabilir (captcha tetiklenemedi veya OCR okuyamadı).")

                print(f"\nSonraki deneme için {interval} saniye bekleniyor...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu (Ctrl + C).")

    def watch_and_solve_on_text(
        self,
        trigger_texts,
        check_interval: float = 2.0,
        wait_after_trigger: float = 2.0,
        rest_after_success: float = 300.0,
    ):
        """
        YENİ MOD:
        - Ekranda belirli bir / birden fazla yazı (trigger_texts) belirlediğin alanda çıkana kadar bekler.
        - Yazı görünce:
            1) Chat'e 'captcha' yaz + ENTER (OSK)
            2) Kısa bekle (captcha penceresinin açılması için)
            3) OCR + yaz + confirm

        Sürekli döngü halinde tekrarlar (Ctrl + C ile durdur).
        Her başarılı captcha çözümünden sonra rest_after_success kadar bekler.
        """
        # Tek string geldiyse listeye çevir
        if isinstance(trigger_texts, str):
            trigger_texts = [trigger_texts]

        # Boşları temizle
        trigger_texts = [t.strip() for t in trigger_texts if t and t.strip()]

        print("=" * 60)
        print("YAZIYA GÖRE OTOMATİK CAPTCHA ÇÖZÜM MODU")
        print("=" * 60)
        print("Tetik yazılar:")
        for t in trigger_texts:
            print(f"  - '{t}'")
        print(f"Kontrol aralığı: {check_interval} saniye")
        print(f"Başarılı çözüm sonrası bekleme: {rest_after_success} saniye")
        print("Durdurmak için: Ctrl + C")

        iteration = 0
        try:
            while True:
                iteration += 1
                print("\n" + "-" * 60)
                print(f"YAZI TETİK İTERASYON #{iteration}")
                print("-" * 60)

                found = self.wait_for_trigger_text(trigger_texts, check_interval=check_interval)
                if not found:
                    print("Tetik yazı bekleme iptal edildi veya hata oluştu.")
                    break

                # Yazı bulundu → tam akışı çalıştır
                success = self.solve_full_once(wait_after_trigger=wait_after_trigger)
                if not success:
                    print("Bu tetikte tam akış başarısız olabilir (captcha tetiklenemedi veya OCR okuyamadı).")
                    # Başarısız durumda kısa bekleme, sonra tekrar tetik beklemeye dön
                    cooldown = 5.0
                    print(f"\nBaşarısız tetik için kısa bekleme: {cooldown} saniye...")
                    time.sleep(cooldown)
                else:
                    # Başarılı captcha çözümü → uzun dinlenme süresi
                    print(f"\n✓ Captcha başarıyla çözüldü. Şimdi {rest_after_success} saniye dinleniyor...")
                    time.sleep(rest_after_success)
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu (Ctrl + C).")


if __name__ == "__main__":
    solver = AutoReCaptchaSolver()

    # Basit CLI:
    #   python auto_solution.py                    -> 1 kez (ekranda captcha varsa çöz)
    #   python auto_solution.py loop [interval]    -> sadece çözüm döngüsü (captcha zaten ekrandaysa)
    #   python auto_solution.py full               -> tek sefer tam akış (captcha'yı tetikle + çöz)
    #   python auto_solution.py full_loop [saniye] -> süreye göre tam akış döngüsü (eski davranış)
    #   python auto_solution.py watch YAZI1 [YAZI2 ...] [interval] -> ekrandaki yazıya göre (birden fazla yazı) tam akış tetikleme
    import sys

    if len(sys.argv) > 1 and sys.argv[1].lower() == "loop":
        interval = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
        solver.solve_loop(interval=interval)
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "trigger":
        # Sadece 'captcha' yazıp pencereyi tetikle
        solver.trigger_captcha_via_chat()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "full":
        # Tek sefer tam akış: trigger + OCR + yaz + confirm
        solver.solve_full_once()
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "full_loop":
        # Sürekli tam akış döngüsü (süreye göre)
        interval = float(sys.argv[2]) if len(sys.argv) > 2 else 330.0
        solver.solve_full_loop(interval=interval)
    elif len(sys.argv) > 1 and sys.argv[1].lower() == "watch":
        # Ekrandaki yazıya göre tetikleme (birden fazla yazı destekli)
        # Örnek:
        #   python auto_solution.py watch "YAZI1" "YAZI2" 2
        #   → 'YAZI1' VEYA 'YAZI2' görünürse tetikler, 2 sn aralıkla kontrol eder
        args = sys.argv[2:]
        if not args:
            trigger_texts = ["captcha"]
            interval = 2.0
        else:
            # Son argüman sayıya çevrilebiliyorsa interval olarak yorumla
            try:
                interval_candidate = float(args[-1])
                interval = interval_candidate
                trigger_texts = args[:-1] if len(args) > 1 else ["captcha"]
            except ValueError:
                interval = 2.0
                trigger_texts = args

        solver.watch_and_solve_on_text(trigger_texts=trigger_texts, check_interval=interval)
    else:
        solver.solve_once()

