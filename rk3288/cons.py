#!/usr/bin/env python



# GPIO control registers
class BaseReg:
    GPIO_SWPORT_DR     =0x00
    GPIO_SWPORT_DDR    =0x04
    GPIO_INTEN         =0x30
    GPIO_INTMASK       =0x34
    GPIO_INTTYPE_LEVEL =0x38
    GPIO_INT_POLARITY  =0x3c
    GPIO_INT_STATUS    =0x40
    GPIO_INT_RAWSTATUS =0x44
    GPIO_DEBOUNCE      =0x48
    GPIO_PORTS_EOI     =0x4c
    GPIO_EXT_PORT      =0x50
    GPIO_LS_SYNC       =0x60

class GpioLevel:
    LOW = 0
    HIGH = 1

class GpioDir:
    INPUT = 0
    OUTPUT = 1

PIN={
    'A0': 0,    'A1': 1,    'A2': 2,    'A3': 3,    'A4': 4,    'A5': 5,    'A6': 6,    'A7': 7,
    'B0': 8,    'B1': 9,    'B2':10,    'B3':11,    'B4':12,    'B5':13,    'B6':14,    'B7':15,
    'C0':16,    'C1':17,    'C2':18,    'C3':19,    'C4':20,    'C5':21,    'C6':22,    'C7':23,
    'D0':24,    'D1':25,    'D2':26,    'D3':27,    'D4':28,    'D5':29,    'D6':30,    'D7':31,
}


def cons_list(obj):
    l=[]
    for d in dir(obj):
        if d[:2]!='__' and d[-2:]!="__":
            l.append(getattr(obj,d))
    return l
