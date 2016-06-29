#!/usr/bin/env python

from lib.devmem import MapReg
from cons import *

import pdb
import logging


class Bank:
    def __init__(self, ctrl, iomux, pull, drv):
        self.ctrl   = ctrl
        self.iomux  = iomux
        self.pull   = pull
        self.drv    = drv

    def __str__(self):
        return '\nctrl\t%s\niomux\t%s\npull\t%s\ndrv\t%s' % (self.ctrl, self.iomux, self.pull, self.drv)
    __repr__ = __str__

class Gpio(GpioLevel, GpioDir, GpioMux, GpioPull, GpioDrv):
    _inited = 0

    @staticmethod
    def _set_mapreg(mapname, addr, size):
        mr=MapReg(mapname, addr, size)
        setattr(Gpio, '_' + mapname, mr)

    @staticmethod
    def init():
        """
        Init GPIO function
        implement it before using Gpio
        """
        if Gpio._inited > 0:
            logging.error("Gpio have inited!")
            return None
        Gpio._inited = 1

        Gpio._set_mapreg('gpio0_ctrl',0xff750000,0x100)
       #Gpio._set_mapreg('gpio0_iomux',0xff730084,0x0c)
       #Gpio._set_mapreg('gpio0_pull',0xff730064,0x0c)
       #Gpio._set_mapreg('gpio0_drv',0xff730070,0x0c)
       #Gpio._set_mapreg('gpio18_iomux',0xff770000,0x140)
       #Gpio._set_mapreg('gpio18_pull',0xff770140,0x80)
       #Gpio._set_mapreg('gpio18_drv',0xff7701c0,0x80)
        Gpio._set_mapreg('gpio0_base',0xff730000,0x7c)
        Gpio._set_mapreg('gpio18_base',0xff770000,0x240)

        Gpio._set_mapreg('gpio1_ctrl',0xff780000,0x100)
        Gpio._set_mapreg('gpio2_ctrl',0xff790000,0x100)
        Gpio._set_mapreg('gpio3_ctrl',0xff7a0000,0x100)
        Gpio._set_mapreg('gpio4_ctrl',0xff7b0000,0x100)
        Gpio._set_mapreg('gpio5_ctrl',0xff7c0000,0x100)
        Gpio._set_mapreg('gpio6_ctrl',0xff7d0000,0x100)
        Gpio._set_mapreg('gpio7_ctrl',0xff7e0000,0x100)
        Gpio._set_mapreg('gpio8_ctrl',0xff7f0000,0x100)
        Gpio._set_mapreg('gpio15_ctrl',0xff7f2000,0x100)

        Gpio._regs= {
            "GPIO0": 
                Bank(Gpio._gpio0_ctrl, Gpio._gpio0_base, Gpio._gpio0_base, Gpio._gpio0_base),
            "GPIO1": 
                Bank(Gpio._gpio1_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO2": 
                Bank(Gpio._gpio2_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO3": 
                Bank(Gpio._gpio3_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO4": 
                Bank(Gpio._gpio4_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO5": 
                Bank(Gpio._gpio5_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO6": 
                Bank(Gpio._gpio6_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO7": 
                Bank(Gpio._gpio7_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
            "GPIO8": 
                Bank(Gpio._gpio8_ctrl, Gpio._gpio18_base, Gpio._gpio18_base, Gpio._gpio18_base),
        }
    @staticmethod
    def exit():
        Gpio._inited = 0
        pass

    def __init__(self, gpio):
        self.gpio = gpio

        sbank = gpio[:5]
        self.bank = BANK[sbank]
        self.pin = PIN[gpio[5:]]
        self._regs = Gpio._regs[sbank]

    def __str__(self):
        return self.gpio

    def __repr__(self):
        return '%s: bank=%d, pin=%d\n%s' % (self.gpio, self.bank, self.pin, self._regs)


    def set_dir(self, dir):
        """
        set GPIO direction
        :dir: refer to GpioDir
        """
        logging.debug("set_dir: set <%s>=%d" % (self.gpio, dir))
        assert dir in cons_list(GpioDir)

        self.set_mux(GpioMux.MUX_GPIO)   #set iomux=gpio default

        reg = self._regs.ctrl
        val = reg.read(RegCtrl.GPIO_SWPORT_DDR)
        val &= (~(1<<self.pin))
        val |= (dir<<self.pin)
        reg.write(RegCtrl.GPIO_SWPORT_DDR, val)

    def get_level(self):
        """
        Returns the level of the pin for input direction
        or return setting of the DR register for output gpios.
        """

        reg = self._regs.ctrl
        val = reg.read(RegCtrl.GPIO_EXT_PORT)
        val >>=self.pin
        val &=1
        logging.debug("get_level: <%s>=%d" % (self.gpio, val))
        return val

    def set_level(self, level):
        """
        set GPIO output signal
        :level: refer to GpioLevel
        """
        logging.debug("set_level: set <%s>=%d" % (self.gpio, level))
        assert level in cons_list(GpioLevel)

        reg = self._regs.ctrl
        val = reg.read(RegCtrl.GPIO_SWPORT_DR)
        reg.write(RegCtrl.GPIO_SWPORT_DR, (val & (~(1<<self.pin))) | (level<<self.pin))

    def set_mux(self, mux):
        """
        set GPIO mux
        :mux: refer to GpioMux
        """
        logging.debug("set_mux: set <%s>=%d" % (self.gpio, mux))
        assert mux in cons_list(GpioMux)

        try:
            offset,bits = get_mux_offset_bits(self.gpio)
        except:
            logging.warn("set_mux: unknow mux of <%s>" % (self.gpio))
            return None

        set_rk32_iomux(self.bank, self.pin, self._regs.iomux, offset, bits, mux)

    def set_pull(self, pull):
        """
        set GPIO pull
        :pull: refer to GpioPull
        """
        logging.debug("set_pull: set <%s>=%d" % (self.gpio, pull))
        assert pull in cons_list(GpioPull)

        try:
            offset= get_pull_offset_bits(self.gpio)
        except:
            logging.warn("set_pull: unknow pull of <%s>" % (self.gpio))
            return None

        set_rk32_pull(self.pin, self._regs.pull, offset, pull)

    def set_drv(self, drv):
        """
        set GPIO drv
        :drv: refer to GpioDrv
        """
        logging.debug("set_drv: set <%s>=%d" % (self.gpio, drv))
        assert drv in cons_list(GpioDrv)

        try:
            offset= get_drv_offset_bits(self.gpio)
        except:
            logging.warn("set_drv: unknow drv of <%s>" % (self.gpio))
            return None

        set_rk32_drv(self.pin, self._regs.drv, offset, drv)


def get_pull_offset_bits(gpio):
    offset = -1
    offset = getattr(RegPull, "GRF_" + gpio[:6] + "_P")
    return offset

def set_rk32_pull(pin, reg, offset, pull):
    bit = (pin % 8)
    bit *= 2
                
    # enable the write to the equivalent lower bits 
    data = 3 << (bit + 16)
    data |= (pull << bit)

    reg.write(offset, data)

def get_drv_offset_bits(gpio):
    offset = -1
    offset = getattr(RegDrv, "GRF_" + gpio[:6] + "_E")
    return offset

set_rk32_drv = set_rk32_pull

def get_mux_offset_bits(gpio):
    offset = -1
    bits = 0
    try:
        offset = getattr(RegMux, "GRF_" + gpio[:6] + "_IOMUX")
        bits = 2
    except:
        if gpio[6] < 4:
            offset = getattr(RegMux, "GRF_" + gpio[:6] + "L_IOMUX")
        else:
            offset = getattr(RegMux, "GRF_" + gpio[:6] + "H_IOMUX")
        bits=4
    return offset,bits

def set_rk32_iomux(bank, pin, reg, offset, bits, mux):
    if bits == 2:
        bit = (pin % 8) * 2
        mask = 0x3
    elif bits == 4:
        bit = (pin % 4) * 4
        mask = 0xf
    else:
        logging.warn("set_rk32_iomux: unknow bits of <%s-%s>" % (bank, pin, mux))
        return None

    if bank == 0:
        data = reg.read(offset)
        data &= ~(mask<<bit)
        data |= (mux & mask) << bit
    else:
        data = (mask<< (bit + 16))
        data |= (mux & mask) << bit
    reg.write(offset, data)

def gpio_init():
    return gpio()

if __name__ ==  '__main__':
    gpio_init()

import unittest
import logging

class TestGpio(unittest.TestCase):
    '''
    run the follow cmd to auto test:
    python -m unittest rk3288.gpio
    '''
    def test_pull(self):
        '''
        Make sure GPIO5B1(UART1_TX) connect nothing!!
        Make sure GPIO0B5 connect nothing!!
        '''
        def _test_pull(ioname):
            gpio=Gpio(ioname)
            gpio.set_dir(GpioDir.INPUT)

            gpio.set_pull(GpioPull.DOWN)
            self.assertEqual(gpio.get_level(), GpioLevel.LOW)
            gpio.set_pull(GpioPull.UP)
            self.assertEqual(gpio.get_level(), GpioLevel.HIGH)

        _test_pull('GPIO5B1')
        _test_pull('GPIO0B5')

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        Gpio.init()
        logging.debug("setup gpio")

    def tearDown(self):
        pass

