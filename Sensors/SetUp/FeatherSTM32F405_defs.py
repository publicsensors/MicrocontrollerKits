#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: STM32f405 Feather

print('Loading definitions for STM32F405 Feather')
from pyb import UART # Use pyb UART bc machine.UART clashes with DS18B20s
from machine import Pin, I2C

board='STM32feather'
p_pwr1 = Pin('D9', Pin.OUT,value=1)  # Pin 9 is power supplied to the DS18B20, V+
p_DS18B20 = Pin('D10', Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
uartGPS = UART(6, 9600)
#uartAQ= UART(3, 9600)
#uartAQ.init(9600, bits=8, parity=None, stop=1)
uartAQ= UART(3, 9600, bits=8, parity=None, stop=1)
button = Pin('D13', Pin.IN, Pin.PULL_UP)
# Define default I2C pins
p_I2Cscl_lbl='SCL'
p_I2Csda_lbl='SDA'
# I2C without an ID currently reverts to SoftI2C; use hardware I2C(1)
# instead, which has the specified pinouts
#i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
i2c = I2C(1)
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 'D12'
p_hcsr_echo = 'D11'
#pin definitions to automatically enable sampling loop (1=loop, 0=wait for button press)
p_smpl_loop_lbl='MISO'
#p_smpl_trigger_lbl='SCK'
p_smpl_trigger_lbl='D13'

# Define timers for non-blocking sampling, logging and display
check_timer = Timer()
LCDtimer=Timer()
SMPLtimer=Timer()
AQtimer = Timer()

