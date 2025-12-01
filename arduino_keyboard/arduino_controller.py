"""
Arduino Klavye Kontrolcüsü
Arduino Leonardo/Pro Micro ile USB HID klavye simülasyonu
"""
import serial
import time
import serial.tools.list_ports


class ArduinoKeyboard:
    """Arduino USB HID klavye kontrolcüsü"""
    
    def __init__(self, port=None, baudrate=9600, timeout=2):
        """
        Arduino klavye kontrolcüsünü başlatır
        
        Args:
            port: Seri port adı (None ise otomatik bulur)
            baudrate: Baud rate (varsayılan: 9600)
            timeout: Timeout süresi (saniye)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        
        # Port bulunamazsa otomatik ara
        if not self.port:
            self.port = self.find_arduino_port()
        
        if not self.port:
            raise Exception("Arduino bulunamadı! Lütfen Arduino'yu USB'ye bağlayın.")
        
        # Bağlantıyı aç
        self.connect()
    
    def find_arduino_port(self):
        """
        Arduino portunu otomatik bulur
        
        Returns:
            Port adı veya None
        """
        ports = serial.tools.list_ports.comports()
        
        # Arduino'yu bul (VID/PID veya isim ile)
        for port in ports:
            # Arduino Leonardo, Pro Micro, vb.
            if 'arduino' in port.description.lower() or \
               'leonardo' in port.description.lower() or \
               'pro micro' in port.description.lower() or \
               'CH340' in port.description or \
               'FTDI' in port.description:
                return port.device
        
        # Bulunamazsa ilk portu dene
        if ports:
            return ports[0].device
        
        return None
    
    def connect(self):
        """Arduino'ya bağlanır"""
        try:
            self.serial_connection = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )
            
            # Hazır sinyali bekle
            time.sleep(2)  # Arduino'nun başlaması için bekle
            
            # "READY" mesajını oku
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode('utf-8').strip()
                if "READY" in response:
                    print(f"✓ Arduino bağlandı: {self.port}")
                else:
                    print(f"⚠ Arduino bağlandı ama READY sinyali alınamadı: {self.port}")
            else:
                print(f"✓ Arduino bağlandı: {self.port} (READY sinyali bekleniyor...)")
            
        except Exception as e:
            raise Exception(f"Arduino'ya bağlanılamadı: {e}")
    
    def disconnect(self):
        """Arduino bağlantısını kapatır"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("✓ Arduino bağlantısı kapatıldı")
    
    def send_command(self, command):
        """
        Arduino'ya komut gönderir ve yanıt bekler
        
        Args:
            command: Gönderilecek komut
        
        Returns:
            Yanıt mesajı veya None
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("Arduino bağlantısı yok!")
        
        try:
            # Komutu gönder
            self.serial_connection.write(f"{command}\n".encode('utf-8'))
            self.serial_connection.flush()
            
            # Yanıt bekle
            time.sleep(0.1)
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode('utf-8').strip()
                return response
            
            return None
        except Exception as e:
            print(f"Komut gönderme hatası: {e}")
            return None
    
    def type_text(self, text, delay_ms=50):
        """
        Metin yazar
        
        Args:
            text: Yazılacak metin
            delay_ms: Her karakter arası bekleme (ms)
        """
        # Sadece rakam ve harf karakterleri
        clean_text = ''.join(c for c in text if c.isalnum())
        
        if not clean_text:
            return False
        
        command = f"TYPE:{clean_text}"
        response = self.send_command(command)
        
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        
        return response == "OK"
    
    def press_key(self, key):
        """
        Tuş basar
        
        Args:
            key: Tuş adı (ENTER, BACKSPACE, TAB, ESC)
        """
        command = f"KEY:{key}"
        response = self.send_command(command)
        return response == "OK"
    
    def delay(self, ms):
        """
        Bekler
        
        Args:
            ms: Bekleme süresi (milisaniye)
        """
        command = f"DELAY:{ms}"
        response = self.send_command(command)
        return response == "OK"
    
    def reset(self):
        """Klavyeyi sıfırlar (tüm tuşları bırakır)"""
        command = "RESET"
        response = self.send_command(command)
        return response == "OK"


def test_arduino_keyboard():
    """Arduino klavye testi"""
    print("=" * 60)
    print("ARDUINO KLAVYE TEST")
    print("=" * 60)
    
    try:
        # Arduino'ya bağlan
        keyboard = ArduinoKeyboard()
        
        print("\n⚠ ÖNEMLİ: Oyun penceresini açın ve input field'e tıklayın!")
        print("5 saniye içinde oyun penceresine geçin ve input field'e tıklayın...")
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        # Test metni yaz
        test_text = "1234"
        print(f"\nTest metni yazılıyor: '{test_text}'")
        
        if keyboard.type_text(test_text):
            print("✓ Metin yazıldı")
        else:
            print("✗ Metin yazılamadı")
        
        time.sleep(1)
        
        # Enter tuşuna bas
        print("\nEnter tuşuna basılıyor...")
        if keyboard.press_key("ENTER"):
            print("✓ Enter tuşuna basıldı")
        else:
            print("✗ Enter tuşuna basılamadı")
        
        # Bağlantıyı kapat
        keyboard.disconnect()
        
        print("\n" + "=" * 60)
        print("TEST TAMAMLANDI")
        print("=" * 60)
        print("\nOyun penceresinde kontrol edin:")
        print("1. Input field'de '1234' yazıldı mı?")
        print("2. Enter tuşuna basıldı mı?")
        
    except Exception as e:
        print(f"\n✗ Hata: {e}")
        print("\nKurulum kontrolü:")
        print("1. Arduino Leonardo/Pro Micro USB'ye bağlı mı?")
        print("2. Arduino IDE'de kodu yüklediniz mi?")
        print("3. Doğru port seçili mi?")


if __name__ == "__main__":
    test_arduino_keyboard()

