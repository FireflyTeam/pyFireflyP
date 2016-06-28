#!/usr/bin/env python

from rk3288.gpio import Gpio
from rk3288.pwm import Pwm

import time
import pdb

if __name__ ==  '__main__':
    print('Start PWM example.')

    Gpio.init()
    g7a1=Gpio('GPIO7A1')
    # set pwm1 mux
    g7a1.set_mux(1)

    Pwm.init()
    pwm=Pwm('PWM1')

    print('Set PWM1: freq=1MHz,duty=50%')
    pwm.set_config(1000,500)
    pwm.start()
    time.sleep(5)
    pwm.stop()
    
    print('Set PWM1: freq=100Hz,duty=10%')
    pwm.set_config(10000000,1000000)
    pwm.start()
    time.sleep(5)
    pwm.stop()

    # The shot_counter N means N+1 repeated effective periods.
    shot_counter=2
    print('Set PWM1: freq=1Hz,duty=30%%, repeats=%d' % (shot_counter + 1))
    config = Pwm.PWM_OUTPUT_LEFT | Pwm.PWM_LP_DISABLE | Pwm.PWM_SHOT | Pwm.PWM_DUTY_POSTIVE | Pwm.PWM_INACTIVE_NEGATIVE | (shot_counter << 24)
    pwm.set_config(1000000000, 300000000, config)
    pwm.start()
    
    print('Exit PWM example.')
