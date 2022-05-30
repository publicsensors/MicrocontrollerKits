#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: Pyboard v1.1
from SetUp.verbosity import vrb_print
vrb_print('Loading definitions for PYBv1.1',level='low')

from machine import Pin, I2C, Timer
from pyb import Switch, UART

board='PBDv1.1'
# Initalize power pins off; they are turned on by read_XXX classes if called
p_pwr1 = Pin('X19', Pin.OUT,value=1)  # Pin X19 is power supplied to the DS18B20, V+
p_pwr2 = Pin('X18', Pin.OUT,value=0)  # Pin X18 is power supplied to the GPS, V+
p_pwr3 = Pin('X3', Pin.OUT,value=0)  # Pin X3 is power supplied to the GPS, V+
p_pwr4 = Pin('X4', Pin.OUT,value=0)  # Pin X4 is power supplied to the GPS, V+
p_DS18B20 = Pin('X20', Pin.IN)  # Pin X20 is the data pin for DS18B20 temperature sensors
uartGPS= UART(4, 9600)
uartGPS.init(9600, bits=8, parity=None, stop=1,timeout_char=5)
uartAQ= UART(3, 9600)
uartAQ.init(9600, bits=8, parity=None, stop=1)
uartBT= UART(6, 9600)
uartBT.init(9600, bits=8, parity=None, stop=1)
#p_batt=14
#p_sens=4
# Define default I2C pins
p_I2Cscl_lbl='X9'
p_I2Csda_lbl='X10'
i2c_num=1
# I2C without an ID currently reverts to SoftI2C; use hardware I2C(1)
# instead, which has the specified pinouts
#i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
i2c = I2C(1)
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 'D12'
p_hcsr_echo = 'D11'
#pin definitions to automatically enable sampling loop (1=loop, 0=wait for button press)
p_smpl_loop_lbl='Y4'
#p_smpl_trigger_lbl='Y3'
p_smpl_trigger_lbl='X17'
#button = Switch()  # use onboard USR button

# Define timers for non-blocking sampling, logging and display
check_timer = Timer()
LCDtimer=Timer()
SMPLtimer=Timer()
AQtimer = Timer()
BTtimer = Timer()
