#include <Arduino.h>
#include "FreeRTOS.h"
#include "task.h"

void vTask1(void *pvParameters)
{
  Serial.println("Task1");
  printf("TASK 1\n");
  while (1)
  {
    Serial.printf("Millis = %u\n", millis());
    printf("TICKS  = %lu\n", xTaskGetTickCount());
    delay(4000);
  }
}

void vTask2(void *pvParameters)
{
  Serial.println("Task2");
  printf("TASK 2\n");
  pinMode(LED, OUTPUT);
  while (1)
  {
    static int led = 0;
    digitalWrite(LED, led);
    led ^= 1;
    delay(100);
  }
}

void setup()
{
  Serial.begin(115200, true);
  Serial.printf("\n\nArdiuno Raspberrypi PI Pico");
  printf(" 2021 Georgi Angelov\n");

  xTaskCreate(
      vTask1,  /* Function that implements the task. */
      "Task1", /* Text name for the task. */
      512,     /* Stack size in words, not bytes. */
      NULL,    /* Parameter passed into the task. */
      1,       /* Priority at which the task is created. */
      0);

  xTaskCreate(
      vTask2,   /* Function that implements the task. */
      "vTask2", /* Text name for the task. */
      512,      /* Stack size in words, not bytes. */
      NULL,     /* Parameter passed into the task. */
      1,        /* Priority at which the task is created. */
      0);

  vTaskStartScheduler();
}

void loop() {}