#include <Arduino.h>
#include <PWM.h>

PWMClass PWM(LED);

int duty = 0, direction = 1;

void setup()
{
  Serial.begin(115200, true); // true - retarget prinf() to Serial
  Serial.println("\nArdiuno Raspberrypi PI Pico 2021 Georgi Angelov");
  //PWM.setFreq(2000); // other freq
}

void loop()
{
  duty += direction;
  if (duty > 255)
  {
    duty = 255;
    direction = -1;
  }
  if (duty < 0)
  {
    duty = 0;
    direction = 1;
  }
  PWM.setDuty(duty * duty);
  delay(2);
}
