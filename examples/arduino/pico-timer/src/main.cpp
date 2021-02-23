#include <Arduino.h>
#include <TIMER.h>

void toggle();
void onTimer(int);

TIMERClass T1(TIMER_MODE_PERIODIC, onTimer);
TIMERClass T2(TIMER_MODE_PERIODIC, onTimer);

void onTimer(int id)
{
  printf("%d ", id);
}

void toggle()
{
  static int led = -1;
  if (-1 == led)
  {
    led = 0;
    pinMode(LED, OUTPUT);
  }
  digitalWrite(LED, led);
  led ^= 1;
}

void setup()
{
  Serial.begin(115200, true);
  Serial.println("\nArdiuno Raspberrypi PI Pico 2021 Georgi Angelov");
  T1.begin(1); // Hz
  T2.begin(2); // Hz
}

void loop()
{
  delay(100);
  toggle();
}