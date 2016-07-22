#Python For Firefly Port

fireflyP is designed for using devices port on firefly or other similar platforms.It can support RK3288 now. 
Like GPIO, PWM, SPI and so on.

**NOTE**: fireflyP is still in development. if you find something wrong, please let me know, and if you fix bugs, it is nice to give me 'Pull requests'


##Install
fetch source code:

    $ git clone https://github.com/zhansb/pyFireflyP.git
    $ cd pyFireflyP

install python modules(python can be python2 or python3):

    $ sudo python setup.py install


##Usage
GPIO and PWM control regs directly by devmem in fireflyP, and independent of kernel space.

The devmem source is modifed from [pydevmem](https://github.com/kylemanna/pydevmem) (Thanks to Kyle).

You need root privilege to execute it!

###Gpio
####Interface:
    init()
        Init GPIO function
        implement it before using Gpio
    get_level(self)
        Returns the level of the pin for input direction
        or return setting of the DR register for output gpios.
    
    set_dir(self, dir)
        set GPIO direction
        :dir: refer to GpioDir
    
    set_drv(self, drv)
        set GPIO drv
        :drv: refer to GpioDrv
    
    set_level(self, level)
        set GPIO output signal
        :level: refer to GpioLevel
    
    set_mux(self, mux)
        set GPIO mux
        :mux: refer to GpioMux
    
    set_pull(self, pull)
        set GPIO pull
        :pull: refer to GpioPull

####Example for turn on/off the yellow led on firefly-rk3288:
    $sudo python
    >>> from fireflyP import Gpio
    >>> Gpio.init()
    >>> LED_YELLOW="GPIO8A2"
    >>> led_yellow=Gpio(LED_YELLOW)
    >>> led_yellow.set_dir(Gpio.OUTPUT) #set_dir have contained set_mux(GpioMux.MUX_GPIO)
    >>> led_yellow.set_level(Gpio.LOW)  #turn on the yellow led
    >>> led_yellow.set_level(Gpio.HIGH) #turn off the yellow led

or you can refer to demo/gpio_test.py


###Pwm
####Interface:
    init()
        Init PWM function
        implement it before using Pwm
    get_counter(self)
        Get PWM counter
    
    set_config(self, period, duty, config=10)
        set PWM period and duty.
        :period: ns 
        :duty: ns 
        :config: set PWMx_CTRL value except PWMx_CTRL.scale
    
    set_counter(self, counter)
        set PWM counter
    
    start(self)
        Start PWM
    
    stop(self)
        Stop PWM


####Example for config pwm1(freq=1MHz,duty=50%):
    $sudo python
    >>> from fireflyP import Gpio
    >>> from fireflyP import Pwm
    >>> Gpio.init()
    >>> g7a1=Gpio('GPIO7A1')
    >>> g7a1.set_mux(1)         #set GPIO7A1 mux to pwm1
    >>> Pwm.init()
    >>> pwm=Pwm('PWM1')
    >>> pwm.set_config(1000,500) 
    >>> pwm.start() 
    >>> pwm.stop()

or you can refer to demo/pwm_test.py


###Spi
Spi in fireflyP is depend on spidev,make sure your kernel support spidev(like this [patch](https://bitbucket.org/T-Firefly/firenow-lollipop/commits/65e51b30c5d453dc9d46de6a10283e7e374b8c79?at=Firefly-RK3288)) or you can down the ready-made firmware([Google drive](https://drive.google.com/open?id=0B7HO8lbGgAqAU0NRa1NHWHgweVE),[Baidu](http://pan.baidu.com/s/1gfJisZD)).

The Spi source is modifed from [python-spi](https://github.com/tomstokes/python-spi) (Thanks to Thomas).

####Interface:
    read(self, length, speed=0, bits_per_word=0, delay=0)
        Perform half-duplex Spi read as a binary string
        
        Args:
            length: Integer count of words to read
            speed: Optional temporary bitrate override in Hz. 0 (default)
                uses existing spidev speed setting.
            bits_per_word: Optional temporary bits_per_word override. 0
                (default) will use the current bits_per_word setting.
            delay: Optional delay in usecs between sending the last bit and
                deselecting the chip select line. 0 (default) for no delay.
        
        Returns:
            List of words read from device
    
    transfer(self, data, speed=0, bits_per_word=0, delay=0)
        Perform full-duplex Spi transfer
        
        Args:
            data: List of words to transmit
            speed: Optional temporary bitrate override in Hz. 0 (default)
                uses existing spidev speed setting.
            bits_per_word: Optional temporary bits_per_word override. 0
                (default) will use the current bits_per_word setting.
            delay: Optional delay in usecs between sending the last bit and
                deselecting the chip select line. 0 (default) for no delay.
        
        Returns:
            List of words read from Spi bus during transfer
    
    write(self, data, speed=0, bits_per_word=0, delay=0)
        Perform half-duplex Spi write.
        
        Args:
            data: List of words to write
            speed: Optional temporary bitrate override in Hz. 0 (default)
                uses existing spidev speed setting.
            bits_per_word: Optional temporary bits_per_word override. 0
                (default) will use the current bits_per_word setting.
            delay: Optional delay in usecs between sending the last bit and
                deselecting the chip select line. 0 (default) for no delay.
    
####Example for config spi0:
    $sudo python
    >>> from fireflyP import Spi
    >>> spi = Spi('/dev/spidev0.0')
    >>> spi.mode = Spi.MODE_3
    >>> spi.bits_per_word = 8
    >>> spi.speed = 1000*1000
    >>> received = spi.transfer([0x11, 0x22, 0xFF])
    >>> spi.write([0x12, 0x34, 0xAB, 0xCD])
    >>> received = spi.read(10)
 
or you can refer to demo/spi_test.py, it is a example of lighting up a oled.
