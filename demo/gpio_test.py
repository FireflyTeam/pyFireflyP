#!/usr/bin/env python

from fireflyP import Gpio

import time
import pdb


LED_BLUE="GPIO8A1"
LED_YELLOW="GPIO8A2"

PWM1="GPIO7A1"
GPIO7A1_IOMUX_GPIO=0
GPIO7A1_IOMUX_PWM1=1


if __name__ ==  '__main__':
    #pdb.set_trace()
    Gpio.init()

    g0b5=Gpio('GPIO0B5')
    g5b1=Gpio('GPIO5B1')
    # except test for error gpio
    # Gpio('GPIO9A15').set_mux(0)	

    g0b5.set_dir(Gpio.OUTPUT)
    g0b5.set_drv(Gpio.E_2MA)
    g0b5.set_drv(Gpio.E_12MA)


    gpio_blue_led=Gpio(LED_BLUE)
    gpio_yellow_led=Gpio(LED_YELLOW)
    gpio_blue_led.set_dir(Gpio.OUTPUT)
    gpio_yellow_led.set_dir(Gpio.OUTPUT)
    while(True):
        gpio_blue_led.set_level(Gpio.HIGH)
        gpio_yellow_led.set_level(Gpio.LOW)
        time.sleep(0.5)
        gpio_blue_led.set_level(Gpio.LOW)
        gpio_yellow_led.set_level(Gpio.HIGH)
        time.sleep(0.5)

