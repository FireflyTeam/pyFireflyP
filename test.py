#!/usr/bin/env python

from rk3288.gpio import Gpio
from rk3288.cons import *
import time
import logging

logging.basicConfig(level=logging.DEBUG)

LED_BLUE="GPIO8A1"
LED_YELLOW="GPIO8A2"

PWM1="GPIO7A1"
GPIO7A1_IOMUX_GPIO=0
GPIO7A1_IOMUX_PWM1=1


if __name__ ==  '__main__':
    gpio = Gpio()
    gpio.set_mux(PWM1, GPIO7A1_IOMUX_PWM1)

    gpio.set_dir(LED_BLUE, GpioDir.OUTPUT)
    gpio.set_dir(LED_YELLOW, GpioDir.OUTPUT)
    while(True):
        gpio.set_level(LED_BLUE, GpioLevel.HIGH)
        gpio.set_level(LED_YELLOW, GpioLevel.LOW)
        gpio.get_level(LED_YELLOW)
        time.sleep(0.5)
        gpio.set_level(LED_BLUE, GpioLevel.LOW)
        gpio.set_level(LED_YELLOW, GpioLevel.HIGH)
        gpio.get_level(LED_YELLOW)
        time.sleep(0.5)
    1#gpio.set_level("GPIO7C5", GpioLevel.LOW)
