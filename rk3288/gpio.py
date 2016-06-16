#!/usr/bin/env python

from lib import devmem
from cons import *

import pdb
import logging


class MapReg:
    def __init__(self, name, addr, size):
        self.name = name # just for debug
        self.addr = addr
        self.size = size
        self.mem = devmem.DevMem(addr, size, "/dev/mem", 0)

    def write(self, offset, val):
        logging.debug("write: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        self.mem.write(offset, [val,])

    def read(self, offset):
        val = self.mem.read(offset, 1)[0]
        logging.debug("read: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        return val

    def __str__(self):
        return 'MapReg: name=%s, phyaddr=%#010x, len=%#x' % (self.name, self.addr, self.size)
    __repr__ = __str__

class Bank:
    def __init__(self, ctrl, iomux, pull, drv):
        self.ctrl   = ctrl
        self.iomux  = iomux
        self.pull   = pull
        self.drv    = drv

    def __str__(self):
        return 'ctrl\t%s\niomux\t%s\npull\t%s\ndrv\t%s' % (self.ctrl, self.iomux, self.pull, self.drv)
    __repr__ = __str__

class Gpio:
    def __init__(self):
        self._set_mapreg('gpio0_ctrl',0xff750000,0x100)
       #self._set_mapreg('gpio0_iomux',0xff730084,0x0c)
       #self._set_mapreg('gpio0_pull',0xff730064,0x0c)
       #self._set_mapreg('gpio0_drv',0xff730070,0x0c)
       #self._set_mapreg('gpio18_iomux',0xff770000,0x140)
       #self._set_mapreg('gpio18_pull',0xff770140,0x80)
       #self._set_mapreg('gpio18_drv',0xff7701c0,0x80)
        self._set_mapreg('gpio0_base',0xff730000,0x7c)
        self._set_mapreg('gpio18_base',0xff770000,0x240)

        self._set_mapreg('gpio1_ctrl',0xff780000,0x100)
        self._set_mapreg('gpio2_ctrl',0xff790000,0x100)
        self._set_mapreg('gpio3_ctrl',0xff7a0000,0x100)
        self._set_mapreg('gpio4_ctrl',0xff7b0000,0x100)
        self._set_mapreg('gpio5_ctrl',0xff7c0000,0x100)
        self._set_mapreg('gpio6_ctrl',0xff7d0000,0x100)
        self._set_mapreg('gpio7_ctrl',0xff7e0000,0x100)
        self._set_mapreg('gpio8_ctrl',0xff7f0000,0x100)
        self._set_mapreg('gpio15_ctrl',0xff7f2000,0x100)

        self.regs= {
            "GPIO0": Bank(self.gpio0_ctrl, self.gpio0_base, self.gpio0_base, self.gpio0_base),
            "GPIO1": Bank(self.gpio1_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO2": Bank(self.gpio2_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO3": Bank(self.gpio3_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO4": Bank(self.gpio4_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO5": Bank(self.gpio5_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO6": Bank(self.gpio6_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO7": Bank(self.gpio7_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
            "GPIO8": Bank(self.gpio8_ctrl, self.gpio18_base, self.gpio18_base, self.gpio18_base),
        }

    def _set_mapreg(self, mapname, addr, size):
        mr=MapReg(mapname, addr, size)
        setattr(self, mapname, mr)

    def _get_bank_pin(self, gpio):
        sbank = gpio[:5]
        bank = BANK[sbank]
        pin = PIN[gpio[5:]]
        regs = self.regs[sbank]
        return bank,pin,regs

    def set_dir(self, gpio, dir):
        """
        set GPIO direction
        :dir: refer to GpioDir
        """
        logging.debug("set_dir: set <%s>=%d" % (gpio, dir))
        assert dir in cons_list(GpioDir)

        self.set_mux(gpio, GpioMux.MUX_GPIO)   #set iomux=gpio default
        bank,pin,regs = self._get_bank_pin(gpio)

        reg = regs.ctrl
        val = reg.read(RegCtrl.GPIO_SWPORT_DDR)
        val &= (~(1<<pin))
        val |= (dir<<pin)
        reg.write(RegCtrl.GPIO_SWPORT_DDR, val)

    def get_level(self, gpio):
        """
        Returns the level of the pin for input direction
        or return setting of the DR register for output gpios.
        """
        bank,pin,regs = self._get_bank_pin(gpio)

        reg = regs.ctrl
        val = reg.read(RegCtrl.GPIO_EXT_PORT)
        val >>=pin
        val &=1
        logging.debug("get_level: <%s>=%d" % (gpio, val))
        return val

    def set_level(self, gpio, level):
        """
        set GPIO output signal
        :level: refer to GpioLevel
        """
        logging.debug("set_level: set <%s>=%d" % (gpio, level))
        assert level in cons_list(GpioLevel)

        bank,pin,regs = self._get_bank_pin(gpio)

        reg = regs.ctrl
        val = reg.read(RegCtrl.GPIO_SWPORT_DR)
        reg.write(RegCtrl.GPIO_SWPORT_DR, (val & (~(1<<pin))) | (level<<pin))

    def set_mux(self, gpio, mux):
        """
        set GPIO mux
        :mux: refer to GpioMux
        """
        logging.debug("set_mux: set <%s>=%d" % (gpio, mux))
        assert mux in cons_list(GpioMux)

        bank,pin,regs = self._get_bank_pin(gpio)

        try:
            offset,bits = get_mux_offset_bits(gpio)
        except:
            logging.warn("set_mux: unknow mux of <%s>" % (gpio))
            return None

        set_rk32_iomux(bank, pin, regs.iomux, offset, bits, mux)

    def set_pull(self, gpio, pull):
        """
        set GPIO pull
        :pull: refer to GpioPull
        """
        logging.debug("set_pull: set <%s>=%d" % (gpio, pull))
        assert pull in cons_list(GpioPull)

        bank,pin,regs = self._get_bank_pin(gpio)

        try:
            offset= get_pull_offset_bits(gpio)
        except:
            logging.warn("set_pull: unknow pull of <%s>" % (gpio))
            return None

        set_rk32_pull(pin, regs.pull, offset, pull)

    def set_drv(self, gpio, drv):
        """
        set GPIO drv
        :drv: refer to GpioDrv
        """
        logging.debug("set_drv: set <%s>=%d" % (gpio, drv))
        assert drv in cons_list(GpioDrv)

        bank,pin,regs = self._get_bank_pin(gpio)

        try:
            offset= get_drv_offset_bits(gpio)
        except:
            logging.warn("set_drv: unknow drv of <%s>" % (gpio))
            return None

        set_rk32_drv(pin, regs.drv, offset, drv)


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




