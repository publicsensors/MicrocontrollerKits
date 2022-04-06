# Initialize microcontroller for PublicSensors/SensoresPublicos sensor activities
from SetUp.platform_defs import *
global params
global sensor_func  # attempt to fix global/local issues with eval of functions
global sensor_obj, sensor_module

# Set initial verbosity. Settings in default_params and
# user_params replace this value when imported.
from SetUp.verbosity import vrb_print,vrb_setlevel
vrb_level = 13
#vrb_level = 4
vrb_setlevel(vrb_level)

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

#vrb_print('main: params = ',params)

# Initialize Real Time Clock
rtc=RTC()
params.update({'rtc':rtc}) # dictionary item is a valid RTC object

# Link timers to params
params.update({'check_timer':check_timer}) # dictionary item is either a valid I2C object or False
params.update({'LCDtimer':LCDtimer}) # dictionary item is either a valid I2C object or False
params.update({'SMPLtimer':SMPLtimer}) # dictionary item is either a valid I2C object or False
params.update({'AQtimer':AQtimer}) # dictionary item is either a valid I2C object or False


# Initialize I2C interface
vrb_print('Initializing I2C interface...')
try:
    #i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
    vrb_print('Success: I2C initialized; scan = ',i2c.scan())
except Exception as e:
    print_exception(e)
    vrb_print('Error: Unable to initalize I2C')
    i2c=False
params.update({'i2c':i2c}) # dictionary item is either a valid I2C object or False

## SMBus initialization is disabled until the 5V vs 3.3V issue is solved
## Initialize SMBus interface
vrb_print('Initializing SMBus interface...')
try:
    if p_I2Csda_lbl is None or p_I2Cscl_lbl is None:
        smbus = SMBus(i2c_num)
    else:
        smbus = SMBus(i2c_num,scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
    #smbus = None
    vrb_print('Success: SMBus initialized')
except Exception as e:
    print_exception(e)
    vrb_print('Error: Unable to initalize SMBus')
    smbus=False
params.update({'smbus':smbus}) # dictionary item is either a valid I2C object or False

# Test for presence of LCD, and initialize if present 
vrb_print('Detecting/initializing LCD interface...')
try:
    lcd = lcd_init(i2c)
except Exception as e:
    print_exception(e)
params.update({'lcd':lcd}) # dictionary item is either a valid LCD object or False


# Instantiate a Sampler object
sampler=Sampler(params)
#sampler=Sampler(params,button=button)

#vrb_print('Launching single sample')
#sampler.sample()
          
# Launch sampling cycle
#sampler.sample_loop()
# A non-blocking alternative
sampler.sample_loop_timer()


# To halt SMPL timer, use
#sampler.SMPLtimer.deinit()


