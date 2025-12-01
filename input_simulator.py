"""
Klavye ve Mouse Simülasyonu Modülü
Oyun penceresine yazı yazma ve ENTER gönderme
"""
import pyautogui
import time
import json
from typing import List, Optional


class InputSimulator:
    """Klavye simülasyonu sınıfı"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True  # Güvenlik: Mouse köşeye götürünce dur
        pyautogui.PAUSE = 0.05  # Her işlem arası kısa bekleme
    
    def focus_window(self, window_name: Optional[str] = None):
        """
        Belirli bir pencereye odaklanır
        
        Args:
            window_name: Pencere adı (opsiyonel, şimdilik kullanılmıyor)
        
        Note:
            Windows'ta pencere odaklama için win32gui gerekebilir
            Şimdilik manuel odaklanma bekleniyor
        """
        if window_name:
            print(f"Pencereye odaklanılıyor: {window_name}")
            # TODO: win32gui ile pencere odaklama eklenebilir
            print("Lütfen oyun penceresine manuel olarak odaklanın...")
            time.sleep(1)  # Kullanıcının odaklanması için bekle
        else:
            print("Oyun penceresine odaklanın...")
            time.sleep(1)
    
    def type_text(self, text: str, delay: float = 0.05):
        """
        Metni yazar
        
        Args:
            text: Yazılacak metin
            delay: Her karakter arası gecikme (saniye)
        """
        print(f"Yazılıyor: '{text}' (delay: {delay}s)")
        try:
            # Önce pyautogui.write deneyelim
            pyautogui.write(text, interval=delay)
            print("✓ Yazma tamamlandı (pyautogui.write)")
        except Exception as e:
            print(f"pyautogui.write başarısız: {e}")
            print("Alternatif yöntem deneniyor (karakter karakter)...")
            # Alternatif yöntem: karakter karakter yaz
            for char in text:
                try:
                    pyautogui.press(char)
                    time.sleep(delay)
                except Exception as e2:
                    print(f"Karakter '{char}' yazılamadı: {e2}")
            print("✓ Yazma tamamlandı (alternatif yöntem)")
    
    def type_numbers(self, numbers: str, delay: float = 0.05):
        """
        Sadece rakamları yazar
        
        Args:
            numbers: Yazılacak rakamlar (string)
            delay: Her karakter arası gecikme (saniye)
        """
        # Sadece rakamları filtrele
        numbers_only = ''.join(filter(str.isdigit, numbers))
        if numbers_only:
            self.type_text(numbers_only, delay)
        else:
            print("Uyarı: Yazılacak rakam bulunamadı!")
    
    def press_enter(self, delay_after: float = 0.1):
        """
        ENTER tuşuna basar
        
        Args:
            delay_after: ENTER'dan sonra bekleme süresi (saniye)
        """
        pyautogui.press('enter')
        time.sleep(delay_after)
    
    def send_numbers_and_enter(self, numbers: str, typing_delay: float = 0.05, enter_delay: float = 0.1):
        """
        Rakamları yazar ve ENTER'a basar
        
        Args:
            numbers: Yazılacak rakamlar
            typing_delay: Yazma gecikmesi
            enter_delay: ENTER sonrası gecikme
        """
        print(f"Yazılıyor: '{numbers}'")
        self.type_numbers(numbers, typing_delay)
        time.sleep(0.1)  # Yazma bitince kısa bekle
        print("ENTER'a basılıyor...")
        self.press_enter(enter_delay)
    
    def send_multiple_numbers(self, number_list: List[str], typing_delay: float = 0.05, enter_delay: float = 0.1, between_delay: float = 0.2):
        """
        Birden fazla numarayı sırayla yazar ve her birinden sonra ENTER'a basar
        
        Args:
            number_list: Yazılacak numaralar listesi
            typing_delay: Yazma gecikmesi
            enter_delay: ENTER sonrası gecikme
            between_delay: Her numara arası gecikme
        """
        for i, numbers in enumerate(number_list, 1):
            print(f"\n[{i}/{len(number_list)}] Numara yazılıyor...")
            self.send_numbers_and_enter(numbers, typing_delay, enter_delay)
            if i < len(number_list):  # Son numara değilse bekle
                time.sleep(between_delay)
    
    def wait_for_ready(self, wait_time: float = 1.0):
        """
        Oyunun hazır olmasını bekler
        
        Args:
            wait_time: Bekleme süresi (saniye)
        """
        print(f"Oyunun hazır olması bekleniyor ({wait_time}s)...")
        time.sleep(wait_time)
    
    def get_mouse_position(self):
        """Mevcut mouse pozisyonunu döndürür"""
        return pyautogui.position()
    
    def click(self, x: int, y: int, delay_after: float = 0.1):
        """
        Belirli bir koordinata tıklar
        
        Args:
            x: X koordinatı
            y: Y koordinatı
            delay_after: Tıklama sonrası bekleme süresi (saniye)
        """
        print(f"Tıklanıyor: ({x}, {y})")
        print(f"Mevcut mouse pozisyonu: {pyautogui.position()}")
        
        try:
            # Önce mouse'u hareket ettir (daha yavaş)
            print(f"Mouse hareket ettiriliyor: ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.1)
            
            # Mouse pozisyonunu kontrol et
            current_pos = pyautogui.position()
            print(f"Mouse pozisyonu: {current_pos}")
            
            # Sonra tıkla (hem sol hem de sağ tıklama denemesi)
            print("Tıklama yapılıyor...")
            pyautogui.click(x, y, button='left')
            time.sleep(0.1)
            
            # Çift tıklama da deneyelim (input field için)
            pyautogui.click(x, y, button='left', clicks=2, interval=0.1)
            
            print(f"✓ Tıklama tamamlandı: ({x}, {y})")
            time.sleep(delay_after)
        except Exception as e:
            print(f"Hata: Tıklama başarısız: {e}")
            # Alternatif: direkt click
            try:
                pyautogui.click(x, y)
                print("✓ Alternatif tıklama yöntemi başarılı")
            except Exception as e2:
                print(f"Alternatif tıklama da başarısız: {e2}")
    
    def click_center(self, x: int, y: int, width: int, height: int, delay_after: float = 0.1):
        """
        Belirli bir alanın merkezine tıklar
        
        Args:
            x, y: Alanın sol üst köşesi
            width, height: Alan boyutları
            delay_after: Tıklama sonrası bekleme süresi
        """
        center_x = x + width // 2
        center_y = y + height // 2
        print(f"Alan merkezi: ({center_x}, {center_y}) - Alan: ({x}, {y}, {width}x{height})")
        self.click(center_x, center_y, delay_after)


class WindowManager:
    """Windows pencere yönetimi (gelecekte eklenebilir)"""
    
    @staticmethod
    def find_window_by_name(window_name: str):
        """
        Pencere adına göre pencere bulur
        
        Note: win32gui gerekli, şimdilik placeholder
        """
        try:
            import win32gui
            # TODO: win32gui ile pencere bulma implementasyonu
            return None
        except ImportError:
            print("win32gui bulunamadı. Pencere yönetimi için: pip install pywin32")
            return None


if __name__ == "__main__":
    # Test kodu
    print("=" * 60)
    print("INPUT SIMULATOR TEST")
    print("=" * 60)
    
    simulator = InputSimulator()
    
    print("\nTest modu - 5 saniye içinde oyun penceresine odaklanın!")
    print("5 saniye sonra '123' yazılacak ve ENTER'a basılacak...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nTest başlıyor...")
    simulator.focus_window()
    simulator.send_numbers_and_enter("123")
    
    print("\nTest tamamlandı!")

