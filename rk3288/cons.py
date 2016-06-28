#!/usr/bin/env python


# GPIO iomux registers
class RegMux:
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

# GPIO slew rate control registers
class RegSlew:
	GRF_GPIO1H_SR           =0x0104
	GRF_GPIO2L_SR           =0x0108
	GRF_GPIO2H_SR           =0x010c
	GRF_GPIO3L_SR           =0x0110
	GRF_GPIO3H_SR           =0x0114
	GRF_GPIO4L_SR           =0x0118
	GRF_GPIO4H_SR           =0x011c
	GRF_GPIO5L_SR           =0x0120
	GRF_GPIO5H_SR           =0x0124
	GRF_GPIO6L_SR           =0x0128
	GRF_GPIO6H_SR           =0x012c
	GRF_GPIO7L_SR           =0x0130
	GRF_GPIO7H_SR           =0x0134
	GRF_GPIO8L_SR           =0x0138

# GPIO pull up/pull down registers
class RegPull:
	GRF_GPIO0A_P            =0x0064
	GRF_GPIO0B_P            =0x0068
	GRF_GPIO0C_P            =0x006c

	GRF_GPIO1D_P            =0x014c

	GRF_GPIO2A_P            =0x0150
	GRF_GPIO2B_P            =0x0154
	GRF_GPIO2C_P            =0x0158

	GRF_GPIO3A_P            =0x0160
	GRF_GPIO3B_P            =0x0164
	GRF_GPIO3C_P            =0x0168
	GRF_GPIO3D_P            =0x016c

	GRF_GPIO4A_P            =0x0170
	GRF_GPIO4B_P            =0x0174
	GRF_GPIO4C_P            =0x0178
	GRF_GPIO4D_P            =0x017c

	GRF_GPIO5B_P            =0x0184
	GRF_GPIO5C_P            =0x0188

	GRF_GPIO6A_P            =0x0190
	GRF_GPIO6B_P            =0x0194
	GRF_GPIO6C_P            =0x0198

	GRF_GPIO7A_P            =0x01a0
	GRF_GPIO7B_P            =0x01a4
	GRF_GPIO7C_P            =0x01a8

	GRF_GPIO8A_P            =0x01b0
	GRF_GPIO8B_P            =0x01b4

# GPIO drive strength control registers
class RegDrv:
	GRF_GPIO0A_E            =0x0070
	GRF_GPIO0B_E            =0x0074
	GRF_GPIO0C_E            =0x0078

	GRF_GPIO1D_E            =0x01cc
	
	GRF_GPIO2A_E            =0x01d0
	GRF_GPIO2B_E            =0x01d4
	GRF_GPIO2C_E            =0x01d8

	GRF_GPIO3A_E            =0x01e0
	GRF_GPIO3B_E            =0x01e4
	GRF_GPIO3C_E            =0x01e8
	GRF_GPIO3D_E            =0x01ec

	GRF_GPIO4A_E            =0x01f0
	GRF_GPIO4B_E            =0x01f4
	GRF_GPIO4C_E            =0x01f8
	GRF_GPIO4D_E            =0x01fc

	GRF_GPIO5B_E            =0x0204
	GRF_GPIO5C_E            =0x0208

	GRF_GPIO6A_E            =0x0210
	GRF_GPIO6B_E            =0x0214
	GRF_GPIO6C_E            =0x0218

	GRF_GPIO7A_E            =0x0220
	GRF_GPIO7B_E            =0x0224
	GRF_GPIO7C_E            =0x0228

	GRF_GPIO8A_E            =0x0230
	GRF_GPIO8B_E            =0x0234

# GPIO control registers
class RegCtrl:
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

# PWM registers
class RegPwm:
    PWM_REG_CNTR       =0x00
    PWM_REG_PERIOD     =0x04       #PWM_REG_HRC
    PWM_REG_DUTY       =0x08       #PWM_REG_LRC   
    PWM_REG_CTRL       =0x0c


class GpioLevel:
    LOW = 0
    HIGH = 1

class GpioDir:
    INPUT = 0
    OUTPUT = 1

class GpioMux:
	MUX_GPIO	=0
	MUX_1		=1
	MUX_2		=2
	MUX_3		=3
	MUX_4		=4
	MUX_5		=5
	MUX_6		=6
	MUX_7		=7

class GpioPull:
	NORAML		=0
	UP			=1
	DOWN		=2
	BUS_HOLD	=3

class GpioDrv:
	DRV_2MA		=0
	DRV_4MA		=1
	DRV_8MA		=2
	DRV_12MA	=3

class PwmCtrl:
    PWM_DISABLE         =(0 << 0) 
    PWM_ENABLE          =(1 << 0)

    PWM_SHOT               =(0 << 1)
    PWM_CONTINUMOUS        =(1 << 1)
    PWM_CAPTURE         =(1 << 2)

    PWM_DUTY_POSTIVE       =(1 << 3)
    PWM_DUTY_NEGATIVE      =(0 << 3)

    PWM_INACTIVE_POSTIVE   =(1 << 4)
    PWM_INACTIVE_NEGATIVE  =(0 << 4)

    PWM_OUTPUT_LEFT        =(0 << 5)
    PWM_OUTPUT_ENTER       =(1 << 5)

    PWM_LP_ENABLE          =(1<<8)
    PWM_LP_DISABLE         =(0<<8)

	
BANK={
	'GPIO0':0,
	'GPIO1':1,
	'GPIO2':2,
	'GPIO3':3,
	'GPIO4':4,
	'GPIO5':5,
	'GPIO6':6,
	'GPIO7':7,
	'GPIO8':8,
}

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
