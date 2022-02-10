#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: STM32f405 Feather

print('Loading definitions for STM32F405 Feather')
from machine import Pin, UART, I2C

board='STM32feather'
p_pwr1 = Pin('D9', Pin.OUT,value=1)  # Pin 12 is power supplied to the DS18B20, V+
p_DS18B20 = Pin('D10', Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
uartGPS = UART(6, 9600)
#uartAQ= UART(3, 9600)
#uartAQ.init(9600, bits=8, parity=None, stop=1)
uartAQ= UART(3, 9600, bits=8, parity=None, stop=1)
button = Pin('D13', Pin.IN, Pin.PULL_UP)
# Define default I2C pins
p_I2Cscl_lbl='SCL'
p_I2Csda_lbl='SDA'
i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 'D12'
p_hcsr_echo = 'D11'
#pin definitions to automatically enable sampling loop (0=loop, 1= wait for button press)
# the labeling above seems to be backwards -- should be 1=loop, 0=wait for button press)
p_smpl_loop_lbl='MISO'
p_smpl_trigger_lbl='SCK'
#p_smpl_trigger_lbl='D13'

