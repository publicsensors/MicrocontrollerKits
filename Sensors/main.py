# Initialize microcontroller for PublicSensors/SensoresPublicos sensor activities

from SetUp.platform_defs import *
global params
global sensor_func  # attempt to fix global/local issues with eval of functions
global sensor_obj, sensor_module
global sample_trigger

params={}


from sys import print_exception
from machine import I2C, RTC
from time import sleep
from esp8266_i2c_lcd import I2cLcd

from SetUp.sensor_utils import sample_params, Sampler, trigger_sample
from SetUp.lcd_setup import lcd_init

# Load default and user-specified parameters
new_pars=sample_params()
params.update(new_pars)

params.update({'p_smpl_trigger_lbl':p_smpl_trigger_lbl,'p_smpl_loop_lbl':p_smpl_loop_lbl})

#print('main: params = ',params)

# Initialize Real Time Clock
rtc=RTC()
params.update({'rtc':rtc}) # dictionary item is a valid RTC object

# Initialize I2C interface
print('Initializing I2C interface...')
try:
    i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
    print('Success: I2C initialized')
except Exception as e:
    print_exception(e)
    print('Error: Unable to initalize I2C')
    i2c=False
params.update({'i2c':i2c}) # dictionary item is either a valid I2C object or False

# Test for presence of LCD, and initialize if present 
print('Detecting/initializing LCD interface...')
try:
    lcd = lcd_init(i2c)
    assert(lcd != False)
except Exception as e:
    print_exception(e)
params.update({'lcd':lcd}) # dictionary item is either a valid LCD object or False


# Instantiate a Sampler object
sampler=Sampler(params,button=button)

#print('Launching single sample')
#sampler.sample()
          
# Launch sampling cycle
sampler.sample_loop()

#print('Launching sampling cycle with sample_loop = ',sample_loop)
#sampler.sample_cycle()

# To halt timer, use
#sampler.timer.deinit()


