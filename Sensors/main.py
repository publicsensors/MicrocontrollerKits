# Initialize microcontroller for PublicSensors/SensoresPublicos sensor activities
# Set initial verbosity. Examples:
# 2 or 'base'--> minimal output
# 4 or 'med'--> moderate ouput
# 13 or 'high' --> verbose output
# Settings in default_params and user_params replace this value when imported.
from SetUp.verbosity import vrb_print,vrb_setlevel as output_setlevel
output_level = 1
output_setlevel(output_level)
# Use e.g. "output_setlevel(2)" or "output_setlevel('med') in the terminal to 
# change output level during sampling

print('\n\nLaunching PublicSensors environmental sensors...\n\n')

from SetUp.platform_defs import *
global params
global sensor_func  # attempt to fix global/local issues with eval of functions
global sensor_obj, sensor_module


params={}

from sys import print_exception
from machine import RTC
#from machine import I2C, RTC
from SetUp.usmbus import SMBus
from time import sleep

from SetUp.sensor_utils import sample_params, Sampler, trigger_sample
from SetUp.lcd_setup import lcd_init

from gc import collect
collect()

# Load default and user-specified parameters
new_pars=sample_params()
params.update(new_pars)

params.update({'p_smpl_trigger_lbl':p_smpl_trigger_lbl,'p_smpl_loop_lbl':p_smpl_loop_lbl})

# Initialize Real Time Clock
rtc=RTC()
params.update({'rtc':rtc}) # dictionary item is a valid RTC object

# Link timers to params
params.update({'check_timer':check_timer}) # dictionary item is either a valid I2C object or False
params.update({'LCDtimer':LCDtimer}) # add LCD timer
params.update({'SMPLtimer':SMPLtimer}) # add sample timer
params.update({'AQtimer':AQtimer}) # add AQI sensor timer
params.update({'BTtimer':BTtimer}) # add bluetooth listener timer


# Initialize I2C interface
vrb_print('Initializing I2C interface...',level='high')
try:
    vrb_print('Success: I2C initialized; scan = ',i2c.scan(),level='high')
except Exception as e:
    print_exception(e)
    vrb_print('Error: Unable to initalize I2C',level='low')
    i2c=False
params.update({'i2c':i2c}) # dictionary item is either a valid I2C object or False

## Initialize SMBus interface
vrb_print('Initializing SMBus interface...',level='high')
try:
    if p_I2Csda_lbl is None or p_I2Cscl_lbl is None:
        smbus = SMBus(i2c_num)
    else:
        smbus = SMBus(i2c_num,scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
    vrb_print('Success: SMBus initialized',level='high')
except Exception as e:
    print_exception(e)
    vrb_print('Error: Unable to initalize SMBus',level='low')
    smbus=False
params.update({'smbus':smbus}) # dictionary item is either a valid I2C object or False

# Test for presence of LCD, and initialize if present 
vrb_print('Detecting/initializing LCD interface...',level='low')
try:
    lcd = lcd_init(i2c)
    vrb_print('Success initializing LCD interface...',level='low')
except Exception as e:
    print_exception(e)
    vrb_print('Error: failed to initialize LCD interface...',level='low')
params.update({'lcd':lcd}) # dictionary item is either a valid LCD object or False


# Instantiate a Sampler object
sampler=Sampler(params)

          
# Launch sampling cycle
sampler.sample_loop_timer()

# To take a sample at any time, execute
#sampler.sample()

# To halt automatic (loop) sampling, execute
#sampler.stop()
# Reboot with ctrl-d to restart automatic sampling

