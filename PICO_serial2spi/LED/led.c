#include "led.h"
#include <hardware/gpio.h>


#define GPIO_INBUILD_LED    25

void LED_init(){
    gpio_init(GPIO_INBUILD_LED);
    gpio_set_dir(GPIO_INBUILD_LED, GPIO_OUT);
}

void LED_on(){
    gpio_put(GPIO_INBUILD_LED, 1);
}

void LED_off(){
    gpio_put(GPIO_INBUILD_LED, 1);
}

void LED_toggle(){
    gpio_put(GPIO_INBUILD_LED, !gpio_get(GPIO_INBUILD_LED));
}