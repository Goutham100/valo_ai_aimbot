#include <Mouse.h>

void setup() {
  Serial.begin(115200);
  Mouse.begin();
  delay(1000);
}

void loop() {
  if (Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data == "C") {
      Mouse.click(MOUSE_LEFT);
      return;
    }

    if (data.length() >= 3)
    {
      int colonIndex = data.indexOf(':');
      int commaIndex = data.indexOf(',');

      if (colonIndex != -1 && commaIndex != -1 && commaIndex > colonIndex)
      {
        int dx = data.substring(colonIndex + 1, commaIndex).toInt();
        int dy = data.substring(commaIndex + 1).toInt();
        Mouse.move(dx, dy);
      }
    }
  }
}





