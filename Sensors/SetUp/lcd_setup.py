# Initialize LCD for PublicSensors/SensoresPublicos sensor activities

from SetUp.platform_defs import *

from machine import Pin, I2C
from SetUp.esp8266_i2c_lcd import I2cLcd
from time import sleep

# Attempt to initialize the LCD. If success, return handle to LCD object.
# If failure, return False to disable further attemps to use the LCD.
def lcd_init(i2c):
    print('Initializing LCD...')
    try:
        #i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
        lcd = I2cLcd(i2c, 0x27,2,16)
        exclam_u = bytearray([0x00,0x04,0x00,0x00,0x04,0x04,0x04,0x04])
        lcd.custom_char(0,exclam_u)
        lcd.putstr('Hello\n'+chr(0)+'Hola!')
        print('Success: LCD initialized')
        sleep(5)
        return lcd
    except:
        lcd = False
        print('LCD initialization failed...proceding without LCD')
    return lcd
    











