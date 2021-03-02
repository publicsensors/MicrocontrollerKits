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

from SetUp.sensor_utils import sample_params, sensor_select, sample_cycle, start_log_files, Sampler, trigger_sample
from SetUp.lcd_setup import lcd_init

# Load default and user-specified parameters
new_pars=sample_params()
params.update(new_pars)

#print('main: params = ',params)

# Initialize Real Time Clock
rtc=RTC()

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
    #print('Success: LCD initialized')
except Exception as e:
    print_exception(e)
    #print('Error: Unable to initalize LCD')    
params.update({'lcd':lcd}) # dictionary item is either a valid LCD object or False

# Detect and initialize sensor drivers
print('Detecting/initializing sensor drivers...')
new_pars=sensor_select(i2c,lcd,params,rtc)
params.update(new_pars)

# If auto-logging is enabled, initialize log files
if params['auto_logging']:
          start_log_files(i2c,lcd,params,rtc)

# Instantiate a Sampler object
sample_loop=p_sample_loop.value()
print('sample_loop = ',sample_loop)
sampler=Sampler(params,button=button,p_sample_loop=p_sample_loop)
#sampler=Sampler(params,button,sample_loop=sample_loop)
#print('Launching single sample')
#sampler.sample()
          
# Launch sampling cycle
sampler.sample_loop()
#print('Launching sampling cycle with sample_loop = ',sample_loop)
#sampler.sample_cycle()



#sample_cycle(params,button,sample_loop=sample_loop)


# To halt timer, use
#sampler.timer.deinit()


