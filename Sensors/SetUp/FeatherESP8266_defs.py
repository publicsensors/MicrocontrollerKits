#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: ESP8266 Huzzah Feather/Breakout Board

print('Loading definitions for ESP8266')

from machine import Pin, UART
from esp import osdebug # stop annoying WiFi messages
osdebug(None)
from uos import dupterm
dupterm(UART(0, 115200), 1) # echo UART to terminal
# Uncomment to automatically start webrepl
#import webrepl
#webrepl.start()
import gc
gc.collect()

board='esp8266'
p_pwr1 = Pin(13, Pin.OUT)  # Pin 12 is power supplied to the DS18B20, V+
p_DS18B20 = Pin(12, Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
button = Pin(14, Pin.IN, Pin.PULL_UP)
# Define default I2C pins
p_I2Cscl_lbl=5
p_I2Csda_lbl=4
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 12
p_hcsr_echo = 14

