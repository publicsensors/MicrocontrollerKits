#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: Pyboard v1.1

print('Loading definitions for PYBv1.1')
from machine import Pin, UART, I2C
from pyb import Switch #, UART

board='PBDv1.1'
# Initalize power pins off; they are turned on by read_XXX classes if called
p_pwr1 = Pin('X19', Pin.OUT,value=1)  # Pin X19 is power supplied to the DS18B20, V+
p_pwr2 = Pin('X18', Pin.OUT,value=0)  # Pin X18 is power supplied to the GPS, V+
p_pwr3 = Pin('X3', Pin.OUT,value=0)  # Pin X3 is power supplied to the GPS, V+
p_pwr4 = Pin('X4', Pin.OUT,value=0)  # Pin X4 is power supplied to the GPS, V+
p_DS18B20 = Pin('X20', Pin.IN)  # Pin X20 is the data pin for DS18B20 temperature sensors
uartGPS= UART(4, 9600)
uartAQ= UART(3, 9600)
uartAQ.init(9600, bits=8, parity=None, stop=1)
button = Switch()  # use onboard USR button
#p_batt=14
#p_sens=4
# Define default I2C pins
p_I2Cscl_lbl='X9'
p_I2Csda_lbl='X10'
i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 'D12'
p_hcsr_echo = 'D11'
#pin definitions to automatically enable sampling loop (0=loop, 1= wait for button press)
p_smpl_loop_lbl='Y4'
p_smpl_trigger_lbl='Y3'

