#include <Arduino.h>

int printTime()
{
  time_t rawtime;
  struct tm *timeinfo;
  time(&rawtime);
  timeinfo = localtime(&rawtime);
  printf("The current date/time is: %s", asctime(timeinfo));
  return 0;
}

#if 1
#include <FreeRTOS.h>
#include <task.h>

void vTask1(void *pvParameters)
{
  Serial.println("\nTask1");
  printf("TASK 1\n");
  while (1)
  {
    printTime();
    delay(5000);
  }
}

void vTask2(void *pvParameters)
{
  Serial.println("\nTask2");
  printf("TASK 2\n");
  pinMode(PICO_DEFAULT_LED_PIN, OUTPUT);
  while (1)
  {
    static int led = 0;
    digitalWrite(LED, led);
    led ^= 1;
    delay(100);
  }
}

void setup() // called from MainTask ( Arduino hidden task )
{
  Serial.begin(115200, true); // retarget printf()
  Serial.printf("\n\nArdiuno Raspberrypi PI Pico");
  printf(" 2021 Georgi Angelov\n");
  xTaskCreate(
      vTask1,  /* Function that implements the task. */
      "Task1", /* Text name for the task. */
      512,     /* Stack size in words, not bytes. */
      NULL,    /* Parameter passed into the task. */
      1,       /* Priority at which the task is created. */
      NULL);

  xTaskCreate(
      vTask2,   /* Function that implements the task. */
      "vTask2", /* Text name for the task. */
      512,      /* Stack size in words, not bytes. */
      NULL,     /* Parameter passed into the task. */
      1,        /* Priority at which the task is created. */
      NULL);
}

void loop() // called from MainTask ( Arduino hidden task )
{
  printf("millis = %d, %d\n", millis(), micros());
  delay(1000);
}

#else

void setup()
{
  Serial.begin(115200, true); // retarget printf()
  Serial.printf("\n\nArdiuno Raspberrypi PI Pico");
  printf(" 2021 Georgi Angelov\n");
  pinMode(LED, OUTPUT);
}

void loop()
{
  printTime();
  delay(5000);
  static int led = 0;
  digitalWrite(LED, led);
  led ^= 1;
}

#endif
