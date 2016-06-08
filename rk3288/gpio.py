#!/usr/bin/env python

from lib import devmem
from cons import *

import pdb
import logging


class MapReg:
    def __init__(self, addr, size):
        self.addr = addr
        self.size = size
        self.mem = devmem.DevMem(addr, size, "/dev/mem", 0)
    def write(self, offset, val):
        logging.debug("write: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        self.mem.write(offset, [val,])
        pass

    def read(self, offset):
        val = 0xac00ac01
        val = self.mem.read(offset, 1)[0]
        logging.debug("read: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        return val
        pass

class Bank:
    def __init__(self, base, iomux, pull, drv):
        self.base   = base
        self.iomux  = iomux
        self.pull   = pull
        self.drv    = drv

class Gpio:
    def __init__(self):
        self.gpio0_base =   MapReg(0xff750000,0x100)
        self.gpio0_iomux =  MapReg(0xff730084,0x0c)
        self.gpio0_pull =   MapReg(0xff730064,0x0c)
        self.gpio0_drv =    MapReg(0xff730070,0x0c)

        self.gpio18_iomux = MapReg(0xff770000,0x140)
        self.gpio18_pull =  MapReg(0xff770140,0x80)
        self.gpio18_drv =   MapReg(0xff7701c0,0x80)
        
        self.gpio1_base =   MapReg(0xff780000,0x100)
        self.gpio2_base =   MapReg(0xff790000,0x100)
        self.gpio3_base =   MapReg(0xff7a0000,0x100)
        self.gpio4_base =   MapReg(0xff7b0000,0x100)
        self.gpio5_base =   MapReg(0xff7c0000,0x100)
        self.gpio6_base =   MapReg(0xff7d0000,0x100)
        self.gpio7_base =   MapReg(0xff7e0000,0x100)
        self.gpio8_base =   MapReg(0xff7f0000,0x100)
        self.gpio15_base =  MapReg(0xff7f2000,0x100)
        self.regs= {
            "GPIO0": Bank(self.gpio0_base, self.gpio0_iomux, self.gpio0_pull, self.gpio0_drv),
            "GPIO8": Bank(self.gpio8_base, self.gpio18_iomux, self.gpio18_pull, self.gpio18_drv),
        }
    def _get_bank_pin(self, gpio):
        bank = gpio[:5]
        pin = PIN[gpio[5:]]
        regs = self.regs[bank]
        return bank,pin,regs

    def set_dir(self, gpio, dir):
        """
        set GPIO direction
        :dir: refer to GpioDir
        """
        logging.debug("set_dir: set <%s>=%d" % (gpio, dir))
        assert dir in cons_list(GpioDir)

        try:
            bank,pin,regs = self._get_bank_pin(gpio)
        except:
            logging.error("set_dir: set <%s>=%d error!" % (gpio, dir))
            return None

        reg = regs.base
        val = reg.read(BaseReg.GPIO_SWPORT_DDR)
        val &= (~(1<<pin))
        val |= (dir<<pin)
        reg.write(BaseReg.GPIO_SWPORT_DDR, val)

    def get_level(self, gpio):
        """
        Returns the level of the pin for input direction
        or return setting of the DR register for output gpios.
        """
        try:
            bank,pin,regs = self._get_bank_pin(gpio)
        except:
            logging.error("get_level: get <%s> error!" % (gpio))
            return None
        reg = regs.base
        val = reg.read(BaseReg.GPIO_EXT_PORT)
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

        try:
            bank,pin,regs = self._get_bank_pin(gpio)
        except:
            logging.error("set_level: set <%s>=%d error!" % (gpio, level))
            return None
        reg = regs.base
        val = reg.read(BaseReg.GPIO_SWPORT_DR)
        reg.write(BaseReg.GPIO_SWPORT_DR, (val & (~(1<<pin))) | (level<<pin))

    def set_mux(self, gpio, mux):
        pass

    def set_pull(self, gpio, pd):
        pass

    def set_drv(self, gpio, drv):
        pass

def gpio_init():
    return gpio()

if __name__ ==  '__main__':
    gpio_init()




