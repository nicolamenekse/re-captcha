"""
Hardware-Level Input Simülasyonu
En düşük seviye klavye input simülasyonu
"""
import ctypes
import time
from ctypes import wintypes


class HardwareInput:
    """Hardware-level input simülasyonu"""
    
    # Windows API constants
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self._setup_structures()
    
    def _setup_structures(self):
        """Windows API structure'larını hazırla"""
        PUL = ctypes.POINTER(ctypes.c_ulong)
        
        class KeyBdInput(ctypes.Structure):
            _fields_ = [
                ("wVk", ctypes.c_ushort),      # Virtual key code
                ("wScan", ctypes.c_ushort),    # Hardware scan code
                ("dwFlags", ctypes.c_ulong),   # Flags
                ("time", ctypes.c_ulong),      # Timestamp
                ("dwExtraInfo", PUL)           # Extra info
            ]
        
        class HardwareInput(ctypes.Structure):
            _fields_ = [
                ("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)
            ]
        
        class MouseInput(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)
            ]
        
        class Input_I(ctypes.Union):
            _fields_ = [
                ("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)
            ]
        
        class Input(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.c_ulong),
                ("ii", Input_I)
            ]
        
        self.KeyBdInput = KeyBdInput
        self.Input_I = Input_I
        self.Input = Input
        self.PUL = PUL
    
    def send_key(self, vk_code, scan_code=None, key_up=False):
        """
        Tek bir tuş gönderir
        
        Args:
            vk_code: Virtual key code (örn: ord('1') = 49)
            scan_code: Hardware scan code (None ise otomatik)
            key_up: True ise KEYUP, False ise KEYDOWN
        """
        extra = ctypes.c_ulong(0)
        ii_ = self.Input_I()
        
        flags = self.KEYEVENTF_KEYUP if key_up else 0
        
        if scan_code is None:
            # Scan code'u otomatik al
            scan_code = self.user32.MapVirtualKeyW(vk_code, 0)
        
        ii_.ki = self.KeyBdInput(
            vk_code,
            scan_code,
            flags,
            0,
            ctypes.pointer(extra)
        )
        
        x = self.Input(self.INPUT_KEYBOARD, ii_)
        result = self.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        
        return result == 1
    
    def send_char(self, char):
        """
        Bir karakter gönderir (KEYDOWN + KEYUP)
        
        Args:
            char: Gönderilecek karakter (string, tek karakter)
        """
        if not char:
            return False
        
        vk_code = ord(char.upper())
        
        # KEYDOWN
        self.send_key(vk_code, key_up=False)
        time.sleep(0.01)  # Çok kısa bekleme
        
        # KEYUP
        self.send_key(vk_code, key_up=True)
        time.sleep(0.01)
        
        return True
    
    def send_text(self, text, delay=0.05):
        """
        Metin gönderir (her karakter için KEYDOWN + KEYUP)
        
        Args:
            text: Gönderilecek metin
            delay: Her karakter arası gecikme (saniye)
        """
        for char in text:
            if char.isdigit() or char.isalpha():
                self.send_char(char)
                time.sleep(delay)
        return True
    
    def send_text_fast(self, text):
        """
        Metni hızlı gönderir (minimum delay)
        
        Args:
            text: Gönderilecek metin
        """
        for char in text:
            if char.isdigit() or char.isalpha():
                vk_code = ord(char.upper())
                
                # KEYDOWN
                self.send_key(vk_code, key_up=False)
                time.sleep(0.01)
                
                # KEYUP
                self.send_key(vk_code, key_up=True)
                time.sleep(0.01)
        
        return True


def test_hardware_input():
    """Hardware input'u test eder"""
    print("=" * 60)
    print("HARDWARE-LEVEL INPUT TEST")
    print("=" * 60)
    
    print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!")
    print("5 saniye içinde oyun penceresine geçin ve input field'e tıklayın...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    hw_input = HardwareInput()
    test_text = "1234"
    
    print(f"\nTest edilecek metin: '{test_text}'")
    print("Hardware-level input gönderiliyor...")
    
    # Test 1: Normal hız
    print("\n1️⃣ Normal hız (delay=0.05)")
    hw_input.send_text(test_text, delay=0.05)
    time.sleep(2)
    
    # Test 2: Hızlı
    print("\n2️⃣ Hızlı (delay=0.01)")
    hw_input.send_text(test_text, delay=0.01)
    time.sleep(2)
    
    # Test 3: Çok hızlı
    print("\n3️⃣ Çok hızlı (minimum delay)")
    hw_input.send_text_fast(test_text)
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print("\nOyun penceresinde kontrol edin:")
    print("1. Input field'de '1234' yazıldı mı?")
    print("2. Hangi hız çalıştı?")
    print("3. Hiçbiri çalışmadıysa, oyun input'ları tamamen engelliyor olabilir")


if __name__ == "__main__":
    test_hardware_input()

