#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: ESP8266 Huzzah Feather/Breakout Board
from SetUp.verbosity import vrb_print
vrb_print('Loading definitions for ESP8266',level='low')

from machine import Pin, UART, I2C
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
#button = Pin(14, Pin.IN, Pin.PULL_UP)
# Define default I2C pins
p_I2Cscl_lbl=5
p_I2Csda_lbl=4
i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 12
p_hcsr_echo = 14
#pin definitions to automatically enable sampling loop (1=loop, = wait for button press)
p_smpl_loop_lbl='MISO'
#p_smpl_trigger_lbl='SCK'
p_smpl_trigger_lbl='D14'

# Define timers for non-blocking sampling, logging and display
check_timer = Timer()
LCDtimer=Timer()
SMPLtimer=Timer()
AQtimer = Timer()

