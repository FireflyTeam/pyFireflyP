#!/usr/bin/env python

from lib.devmem import MapReg
from cons import *

import pdb
import logging


RK_PWM_PRESCALE     =16

PWMCR_MIN_PRESCALE  =0x00
PWMCR_MAX_PRESCALE  =0x07

PWMDCR_MIN_DUTY     =0x0000
PWMDCR_MAX_DUTY     =0xFFFFFFFF

PWMPCR_MIN_PERIOD   =0x0001
PWMPCR_MAX_PERIOD   =0xFFFFFFFF

class Pwm(PwmCtrl):
    _inited = 0

    @staticmethod
    def _set_mapreg(mapname, addr, size):
        mr=MapReg(mapname, addr, size)
        setattr(Pwm, '_' + mapname, mr)

    @staticmethod
    def init():
        """
        Init PWM function
        implement it before using Pwm
        """
        if Pwm._inited > 0:
            logging.error("Pwm have inited!")
            return None
        Pwm._inited = 1

        Pwm._clk = get_pwm_clk()

        Pwm._set_mapreg('pwm0',0xff680000,0x10)
        Pwm._set_mapreg('pwm1',0xff680010,0x10)
        Pwm._set_mapreg('pwm2',0xff680020,0x10)
        Pwm._set_mapreg('pwm3',0xff680030,0x10)

        Pwm._regs= {
            'PWM0': Pwm._pwm0,
            'PWM1': Pwm._pwm1,
            'PWM2': Pwm._pwm2,
            'PWM3': Pwm._pwm3,
        }

    @staticmethod
    def exit():
        Pwm._inited = 0
        pass

    def __init__(self, pwm):
        self.pwm = pwm
        try:
            self._reg = Pwm._regs[pwm]
        except KeyError:
            raise ValueError('have not find PWM(%s)' % pwm)

    def __str__(self):
        return self.pwm

    def __repr__(self):
        return '%s:\n\t%s\n' % (self.pwm, self._reg)


    def start(self):
        """Start PWM
        """
        logging.debug("Start %s" % (self.pwm))

        reg = self._reg
        val = reg.read(RegPwm.PWM_REG_CTRL)
        val |= 0x1
        reg.write(RegPwm.PWM_REG_CTRL, val)

    def stop(self):
        """Stop PWM
        """
        logging.debug("Stop %s" % (self.pwm))

        reg = self._reg
        val = reg.read(RegPwm.PWM_REG_CTRL)
        val &= ~0x1
        reg.write(RegPwm.PWM_REG_CTRL, val)
        
    def set_counter(self, counter):
        """
        set PWM counter
        """
        logging.debug("set_counter: set <%s> counter=%d" % (self.pwm, counter))

        reg = self._reg
        reg.write(RegPwm.PWM_REG_CNTR, counter)

    def get_counter(self):
        """
        Get PWM counter
        """

        reg = self._reg
        counter = reg.read(RegPwm.PWM_REG_CNTR)

        logging.debug("get_counter: get <%s> counter=%d" % (self.pwm, counter))
        return counter

    def set_config(self, period, duty,
            config = PwmCtrl.PWM_OUTPUT_LEFT |
            PwmCtrl.PWM_LP_DISABLE |
            PwmCtrl.PWM_CONTINUMOUS |
            PwmCtrl.PWM_DUTY_POSTIVE |
            PwmCtrl.PWM_INACTIVE_NEGATIVE):
        """set PWM period and duty.
        :period: ns 
        :duty: ns 
        :config: set PWMx_CTRL value except PWMx_CTRL.scale
        """
        logging.debug("set_period: set <%s> period=%d(ns), duty=%d(ns)" % (self.pwm, period, duty))

        # config = PwmCtrl.PWM_OUTPUT_LEFT | PwmCtrl.PWM_LP_DISABLE | PwmCtrl.PWM_CONTINUMOUS | PwmCtrl.PWM_DUTY_POSTIVE | PwmCtrl.PWM_INACTIVE_NEGATIVE
        
        '''
        Find pv, dc and prescale to suit duty_ns and period_ns. This is done
        according to formulas described below:
        
        period_ns = 10^9 * (PRESCALE ) * PV / PWM_CLK_RATE
        duty_ns = 10^9 * (PRESCALE + 1) * DC / PWM_CLK_RATE
        
        PV = (PWM_CLK_RATE * period_ns) / (10^9 * (PRESCALE + 1))
        DC = (PWM_CLK_RATE * duty_ns) / (10^9 * (PRESCALE + 1))
        '''
        clk_rate = Pwm._clk
        prescale = PWMCR_MIN_PRESCALE
        while True:
            div = 1000000000
            div *= 1 + prescale
            val = clk_rate * period
            pv = val/div
            val = clk_rate * duty
            dc = val/div

            # if duty_ns and period_ns are not achievable then return
            if pv < PWMPCR_MIN_PERIOD or  dc < PWMDCR_MIN_DUTY:
                return -1

            '''
            if pv and dc have crossed their upper limit, then increase
            prescale and recalculate pv and dc.
            '''
            if pv > PWMPCR_MAX_PERIOD or  dc > PWMDCR_MAX_DUTY:
                if ++prescale > PWMCR_MAX_PRESCALE:
                    return -2
                continue
            break

        config |= (prescale << RK_PWM_PRESCALE);  

        reg = self._reg
        reg.write(RegPwm.PWM_REG_DUTY,dc)
        reg.write(RegPwm.PWM_REG_PERIOD,pv)
        reg.write(RegPwm.PWM_REG_CNTR,0)
        reg.write(RegPwm.PWM_REG_CTRL,config)
     

def get_pwm_clk():
    path = '/sys/kernel/debug/clk/xin24m/clk_gpll/aclk_bus_src/aclk_bus/pclk_bus/g_pclk_pwm/clk_rate'
    with open(path, 'r') as f:
        clk = f.read()

    return int(clk)


import unittest
import logging

class TestPwm(unittest.TestCase):
    '''
    run the follow cmd to auto test:
    python -m unittest rk3288.pwm
    '''
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        Pwm.init()
        logging.debug("setup pwm")

    def tearDown(self):
        pass

