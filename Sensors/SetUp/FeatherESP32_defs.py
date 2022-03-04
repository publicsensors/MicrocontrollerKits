#  Definitions of platform-specific pins and commands.
#
# Board-specific definitions: ESP32 Feather

print('Loading definitions for ESP32 Feather')
from machine import Pin, UART, SoftI2C, Timer

board='esp32'
p_pwr1 = Pin(15, Pin.OUT)  # Pin 12 is power supplied to the DS18B20, V+
p_DS18B20 = Pin(33, Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
#button = Pin(13, Pin.IN, Pin.PULL_UP)
# Define default I2C pins
p_I2Cscl_lbl=22
p_I2Csda_lbl=23
i2c = SoftI2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
#i2c = I2C(0,scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
#pin definitions for hcsr04/jsn sensors
p_hcsr_trig = 12
p_hcsr_echo = 27
#pin definitions to automatically enable sampling loop (1=loop, 0=wait for button press)
p_smpl_loop_lbl=19
#p_smpl_trigger_lbl='SCK'
#p_smpl_trigger_lbl=13
p_smpl_trigger_lbl=5

# Define timers for non-blocking sampling, logging and display
check_timer = Timer(0)
LCDtimer=Timer(1)
SMPLtimer=Timer(2)
AQtimer = Timer(3)
