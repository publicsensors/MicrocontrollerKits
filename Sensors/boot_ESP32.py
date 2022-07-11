# This file is executed on every boot (including wake-boot from deepsleep)

# code block from original boot.py on STM32 Micropython v1.13
#import machine
#import pyb
#pyb.country('US') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU
##pyb.main('main.py') # main script to run after this one
##pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
##pyb.usb_mode('VCP+HID') # act as a serial device and a mouse
# Import platform-specific definitions

# LCD initialization now moved to lcd_setup.py, and called from main.py

# If sd card is mounted, change directories to read and write files there:
try:
    from SetUp.sdcard import SDCard
    from machine import SoftSPI, Pin
    spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(5), mosi=Pin(18), miso=Pin(19))
    sd = SDCard(spi, Pin(21))
    from os import mount,listdir,chdir
    mount(sd, '/sd')
    chdir('/sd')
    print('SD card mounted -- using /sd as base directory...')
    listdir()
except:
    print('No SD card mounted -- using / as base directory...')



'''
from platform_defs import *

from machine import Pin, I2C
from esp8266_i2c_lcd import I2cLcd
from time import sleep


try:
    i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
    lcd = I2cLcd(i2c, 0x27,2,16)
    exclam_u = bytearray([0x00,0x04,0x00,0x00,0x04,0x04,0x04,0x04])
    lcd.custom_char(0,exclam_u)
    lcd.putstr('Hello\n'+chr(0)+'Hola!')
    sleep(5)
except:
    pass
'''
