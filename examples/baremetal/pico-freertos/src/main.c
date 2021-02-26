#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/divider.h" 
#include "FreeRTOS.h"
#include "task.h"

void vTaskCode(void *pvParameters)
{
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    for (;;)
    {
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(1000);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(1000);
        printf("Ticks  = %lu\n", xTaskGetTickCount());
        printf("Millis = %llu\n", div_u64u64(time_us_64(), 1000));
    }
}

int main(void)
{
    stdio_init_all();
    printf("\n\nHello World\n");
    TaskHandle_t xHandle = NULL;
    BaseType_t xReturned = xTaskCreate(
        vTaskCode,        /* Function that implements the task. */
        "Blinky task",    /* Text name for the task. */
        512,              /* Stack size in words, not bytes. */
        (void *)1,        /* Parameter passed into the task. */
        tskIDLE_PRIORITY, /* Priority at which the task is created. */
        &xHandle);
    vTaskStartScheduler();
    while (1)
    {
        configASSERT(0); /* We should never get here */
    }
}
