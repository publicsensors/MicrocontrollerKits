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
global sensor_func  # fix global/local issues with eval of functions
global sensor_obj, sensor_module

global speed_of_sound
speed_of_sound = 343.2

params={}

from sys import print_exception
from machine import RTC
#from machine import I2C, RTC
from SetUp.usmbus import SMBus
from time import sleep

from SetUp.sensor_utils import sample_params, Sampler, Params, SampleLoop
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

# Link file-writing indicator LED to params
params.update({'fileLED':fileLED}) # add file-writing LED pin to dictionary


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

## declare global driver parameters, so they may be easily changed from the terminal
#speed_of_sound = params['speed_of_sound']

# Initialize the Params convenience function
shared_params={'speed_of_sound':params['speed_of_sound']}
Params(shared_params)


# Instantiate a Sampler object
sampler=Sampler(params)

# Define functions to call sensors directly from the command line
def Sample(N=1,interval=5):
    for n in range(N):
        sampler.sample()
        sleep(interval)
def SampleTemp(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['temperature'])
        sleep(interval)
def SampleLight(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['light'])
        sleep(interval)
def SampleDist(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['distance'])
        sleep(interval)
def SampleUIV(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['UIV'])
        sleep(interval)
def SampleColor(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['color'])
        sleep(interval)
def SampleCO2(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['CO2'])
        sleep(interval)
def SampleVolt(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['voltage'])
        sleep(interval)
def SampleGPSalt(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['GPS_alt'])
        sleep(interval)
def SampleGPSvel(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['GPS_vel'])
        sleep(interval)
def SampleHumidity(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['humidity'])
        sleep(interval)
def SamplePress(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['pressure'])
        sleep(interval)
def SampleAQI(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['AQI'])
        sleep(interval)
def SampleAQI5003(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['AQI5003'])
        sleep(interval)
def SampleAQI7003(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['AQI7003'])
        sleep(interval)
def SampleTime(N=1,interval=5):
    for n in range(N):
        sampler.sample(sensor_select=['exttime'])
        sleep(interval)
        

          
# Launch sampling cycle
sampler.sample_loop_timer()

# To take a sample at any time, execute
#sampler.sample()

# To halt automatic (loop) sampling, execute
#sampler.stop()
# Reboot with ctrl-d to restart automatic sampling

