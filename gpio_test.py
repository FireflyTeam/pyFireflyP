#!/usr/bin/env python

from rk3288.gpio import Gpio
from rk3288.cons import *

import unittest
import time
import logging
import pdb

logging.basicConfig(level=logging.DEBUG)

LED_BLUE="GPIO8A1"
LED_YELLOW="GPIO8A2"

PWM1="GPIO7A1"
GPIO7A1_IOMUX_GPIO=0
GPIO7A1_IOMUX_PWM1=1


if __name__ ==  '__main__':
    gpio = Gpio()

    G0='GPIO0B5'
    G5='GPIO5B1'

    gpio.set_dir(G5, GpioDir.OUTPUT)
    pdb.set_trace()
    gpio.set_drv(G5, GpioDrv.DRV_2MA)
    gpio.set_drv(G5, GpioDrv.DRV_12MA)


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
    #gpio.set_level("GPIO7C5", GpioLevel.LOW)
    #gpio.set_mux('GPIO9A15', 0)	# except test for error gpio

class TestGpio(unittest.TestCase):
    '''
    run the follow cmd to auto test:
    python -m unittest gpio_test
    '''
    def test_pull(self):
        '''
        Make sure GPIO5B1(UART1_TX) connect nothing!!
        Make sure GPIO0B5 connect nothing!!
        '''
        def _test_pull(gpio, pin):
            gpio.set_dir(pin, GpioDir.INPUT)

            gpio.set_pull(pin, GpioPull.DOWN)
            self.assertEqual(gpio.get_level(pin), GpioLevel.LOW)
            gpio.set_pull(pin, GpioPull.UP)
            self.assertEqual(gpio.get_level(pin), GpioLevel.HIGH)

        gpio=Gpio()
        _test_pull(gpio, 'GPIO5B1')
        _test_pull(gpio, 'GPIO0B5')
