# Arduino USB HID Klavye Simülatörü

Bu çözüm, Arduino Leonardo veya Pro Micro kullanarak gerçek bir USB klavye gibi input gönderir. KGuard gibi koruma sistemleri bunu engelleyemez çünkü gerçek hardware input gibi görünür.

## Gereksinimler

### Donanım:
- **Arduino Leonardo** veya **Arduino Pro Micro** (USB HID destekli)
- USB kablosu

### Yazılım:
- Arduino IDE
- Python `pyserial` kütüphanesi

## Kurulum

### 1. Arduino IDE Kurulumu

1. [Arduino IDE](https://www.arduino.cc/en/software) indirin ve kurun
2. Arduino Leonardo/Pro Micro'yu USB'ye bağlayın
3. Arduino IDE'de:
   - **Tools > Board > Arduino Leonardo** (veya Pro Micro) seçin
   - **Tools > Port** menüsünden Arduino'nun portunu seçin

### 2. Arduino Kodunu Yükleme

1. `arduino_keyboard.ino` dosyasını Arduino IDE'de açın
2. **Sketch > Upload** ile kodu Arduino'ya yükleyin
3. Arduino'nun "READY" mesajı göndermesini bekleyin

### 3. Python Kütüphanesi Kurulumu

```bash
pip install pyserial
```

## Kullanım

### Test:

```bash
python arduino_controller.py
```

### Ana Programda Kullanım:

`auto_solution.py` dosyasını güncelleyerek Arduino klavye kullanabilirsiniz.

## Nasıl Çalışır?

1. Python script'i Arduino'ya seri port üzerinden komut gönderir
2. Arduino komutu alır ve USB HID klavye olarak input gönderir
3. Bilgisayar bunu gerçek klavye input'u olarak görür
4. KGuard engelleyemez çünkü gerçek hardware input'tur

## Komut Formatı

- `TYPE:1234` - 1234 yazar
- `KEY:ENTER` - Enter tuşuna basar
- `KEY:BACKSPACE` - Backspace tuşuna basar
- `DELAY:100` - 100ms bekler
- `RESET` - Tüm tuşları bırakır

## Sorun Giderme

### Arduino bulunamıyor:
- Arduino'nun USB'ye bağlı olduğundan emin olun
- Arduino IDE'de port seçimini kontrol edin
- Farklı USB portunu deneyin

### Komutlar çalışmıyor:
- Arduino IDE Serial Monitor'ü kapatın (Python ile çakışır)
- Arduino'yu yeniden başlatın
- Kodu tekrar yükleyin

### Input gönderilmiyor:
- Arduino Leonardo/Pro Micro kullandığınızdan emin olun (Uno çalışmaz)
- Oyun penceresine odaklanın
- Input field'e tıklayın

## Alternatif: Raspberry Pi

Raspberry Pi kullanmak isterseniz, USB Gadget modu ile USB HID device olarak çalışabilir. Daha gelişmiş bir çözüm gerekiyorsa Raspberry Pi versiyonunu da hazırlayabiliriz.

