/*
 * USB HID Klavye Simülatörü
 * Arduino Leonardo / Pro Micro için
 * 
 * Python'dan seri port üzerinden komut alır ve klavye input'u gönderir
 * 
 * Kullanım:
 * 1. Arduino Leonardo veya Pro Micro kullanın (USB HID destekli)
 * 2. Bu kodu yükleyin
 * 3. Python script'i seri port üzerinden komut gönderir
 * 
 * Komut formatı:
 * - "TYPE:1234" -> 1234 yazar
 * - "KEY:ENTER" -> Enter tuşuna basar
 * - "DELAY:100" -> 100ms bekler
 */

#include "Keyboard.h"

void setup() {
  // Seri port başlat (9600 baud)
  Serial.begin(9600);
  
  // Klavye başlat
  Keyboard.begin();
  
  // Hazır sinyali gönder
  Serial.println("READY");
}

void loop() {
  // Seri porttan komut bekle
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    // Komutu işle
    if (command.startsWith("TYPE:")) {
      // Metin yazma komutu
      String text = command.substring(5); // "TYPE:" sonrası
      
      for (int i = 0; i < text.length(); i++) {
        char c = text.charAt(i);
        
        // Sadece rakam ve harf karakterleri
        if (isDigit(c) || isAlpha(c)) {
          Keyboard.write(c);
          delay(50); // Her karakter arası 50ms bekleme
        }
      }
      
      Serial.println("OK");
      
    } else if (command.startsWith("KEY:")) {
      // Tuş basma komutu
      String key = command.substring(4); // "KEY:" sonrası
      key.toUpperCase();
      
      if (key == "ENTER") {
        Keyboard.press(KEY_RETURN);
        delay(10);
        Keyboard.release(KEY_RETURN);
      } else if (key == "BACKSPACE") {
        Keyboard.press(KEY_BACKSPACE);
        delay(10);
        Keyboard.release(KEY_BACKSPACE);
      } else if (key == "TAB") {
        Keyboard.press(KEY_TAB);
        delay(10);
        Keyboard.release(KEY_TAB);
      } else if (key == "ESC") {
        Keyboard.press(KEY_ESC);
        delay(10);
        Keyboard.release(KEY_ESC);
      }
      
      Serial.println("OK");
      
    } else if (command.startsWith("DELAY:")) {
      // Bekleme komutu
      int delay_ms = command.substring(6).toInt();
      delay(delay_ms);
      Serial.println("OK");
      
    } else if (command == "RESET") {
      // Klavyeyi sıfırla
      Keyboard.releaseAll();
      Serial.println("OK");
    }
  }
}

