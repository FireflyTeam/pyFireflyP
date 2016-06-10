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
        val = 0xac00ac01
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
        self._set_mapreg('gpio0_iomux',0xff730084,0x0c)
        self._set_mapreg('gpio0_pull',0xff730064,0x0c)
        self._set_mapreg('gpio0_drv',0xff730070,0x0c)
        self._set_mapreg('gpio18_iomux',0xff770000,0x140)
        self._set_mapreg('gpio18_pull',0xff770140,0x80)
        self._set_mapreg('gpio18_drv',0xff7701c0,0x80)
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
            "GPIO0": Bank(self.gpio0_ctrl, self.gpio0_iomux, self.gpio0_pull, self.gpio0_drv),
            "GPIO7": Bank(self.gpio7_ctrl, self.gpio18_iomux, self.gpio18_pull, self.gpio18_drv),
            "GPIO8": Bank(self.gpio8_ctrl, self.gpio18_iomux, self.gpio18_pull, self.gpio18_drv),
        }

    def _set_mapreg(self, mapname, addr, size):
        mr=MapReg(mapname, addr, size)
        setattr(self, mapname, mr)

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

        reg = regs.ctrl
        val = reg.read(CtrlReg.GPIO_SWPORT_DDR)
        val &= (~(1<<pin))
        val |= (dir<<pin)
        reg.write(CtrlReg.GPIO_SWPORT_DDR, val)

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
        reg = regs.ctrl
        val = reg.read(CtrlReg.GPIO_EXT_PORT)
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
        reg = regs.ctrl
        val = reg.read(CtrlReg.GPIO_SWPORT_DR)
        reg.write(CtrlReg.GPIO_SWPORT_DR, (val & (~(1<<pin))) | (level<<pin))

    def set_mux(self, gpio, mux):
        """
        set GPIO mux
        :mux: refer to 
        """
        logging.debug("set_mux: set <%s>=%d" % (gpio, mux))
        try:
            offset,bits = get_mux_offset_bits(gpio)
        except AttributeError as e:
            logging.error("set_mux: get <%s> offset error" % (gpio))
            return None

        try:
            bank,pin,regs = self._get_bank_pin(gpio)
        except:
            logging.error("set_rk32_iomux: set <%s>=%d error" % (gpio, mux))
            return None

        set_rk32_iomux(bank, pin, regs.iomux, offset, bits, mux)

    def set_pull(self, gpio, pd):
        pass

    def set_drv(self, gpio, drv):
        pass

def get_mux_offset_bits(gpio):
    offset = -1
    bits = 0
    try:
        offset = getattr(MuxReg, "GRF_" + gpio[:6] + "_IOMUX")
        bits = 2
    except AttributeError as e:
        if gpio[6] < 4:
            offset = getattr(MuxReg, "GRF_" + gpio[:6] + "L_IOMUX")
        else:
            offset = getattr(MuxReg, "GRF_" + gpio[:6] + "H_IOMUX")
        bits=4
    return offset,bits

def set_rk32_iomux(bank, pin, reg, offset, bits, mux):
    if bits == 2:
        bit = (pin % 8) * 2

        if bank == "GPIO0":
            data = reg.read(offset);
            data &= ~(3<<bit);
            data |= (mux & 3) << bit;
            reg.write(offset, data);
        else:
            data = (3 << (bit + 16));
            data |= (mux & 3) << bit;
            reg.write(offset, data);
    elif bits == 4:
        bit = (pin % 4) * 4;

        if bank == "GPIO0":
            data = reg.read(offset);
            data &= ~(0x0f<<bit);
            data |= (mux & 0x0f) << bit;
            reg.write(offset, data);
        else:
            data = (0x0f << (bit + 16));
            data |= (mux & 0x0f) << bit;
            reg.write(offset, data);
    else:
        logging.error("set_mux: set <%s-%s> mux<%s> error" % (bank, pin, mux))

def gpio_init():
    return gpio()

if __name__ ==  '__main__':
    gpio_init()




