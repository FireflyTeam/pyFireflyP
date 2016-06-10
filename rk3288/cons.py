#!/usr/bin/env python


# GPIO iomux registers
class MuxReg:
	GRF_GPIO0A_IOMUX	=0x0084
	GRF_GPIO0B_IOMUX	=0x0088
	GRF_GPIO0C_IOMUX	=0x008c

	GRF_GPIO1D_IOMUX    =0x000c

	GRF_GPIO2A_IOMUX    =0x0010
	GRF_GPIO2B_IOMUX    =0x0014
	GRF_GPIO2C_IOMUX    =0x0018

	GRF_GPIO3A_IOMUX    =0x0020
	GRF_GPIO3B_IOMUX    =0x0024
	GRF_GPIO3C_IOMUX    =0x0028
	GRF_GPIO3DL_IOMUX   =0x002c
	GRF_GPIO3DH_IOMUX   =0x0030

	GRF_GPIO4AL_IOMUX   =0x0034
	GRF_GPIO4AH_IOMUX   =0x0038
	GRF_GPIO4BL_IOMUX   =0x003c
	GRF_GPIO4C_IOMUX    =0x0044
	GRF_GPIO4D_IOMUX    =0x0048

	GRF_GPIO5B_IOMUX    =0x0050
	GRF_GPIO5C_IOMUX    =0x0054

	GRF_GPIO6A_IOMUX    =0x005c
	GRF_GPIO6B_IOMUX    =0x0060
	GRF_GPIO6C_IOMUX    =0x0064

	GRF_GPIO7A_IOMUX    =0x006c
	GRF_GPIO7B_IOMUX    =0x0070
	GRF_GPIO7CL_IOMUX   =0x0074
	GRF_GPIO7CH_IOMUX   =0x0078

	GRF_GPIO8A_IOMUX    =0x0080
	GRF_GPIO8B_IOMUX    =0x0084



# GPIO control registers
class CtrlReg:
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
