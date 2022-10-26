# This script prints temperature readings from a DS18B20 sensor
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import *

from machine import Pin, I2C
from Acoustic import hcsr04
from time import sleep_ms

from SetUp.sensor_utils import Params

#global speed_of_sound
#print('speed of sound = ',speed_of_sound)

speed_of_sound = Params('speed_of_sound')

# -------------------------------------------------------------------------------
# Set up pins for the DS18B20
# -------------------------------------------------------------------------------
class read_dist:

    def __init__(self,i2c=None,rtc=None,hcsr_c=speed_of_sound,smbus=None):
    #def __init__(self,i2c=None,rtc=None,hcsr_c=343,smbus=None):
        """ Note: hcsr_c is the speed of sound for hcsr04; default is sos in air, 343
        """
        p_pwr1.value(1)
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be logged

        self.hcsr_c = hcsr_c
        print('Using speed of sound = ',self.hcsr_c)

        self.sensor = hcsr04.HCSR04(trigger_pin = p_hcsr_trig, echo_pin = p_hcsr_echo, c = hcsr_c)

    # -------------------------------------------------------------------------------
    # Test the distance sensor
    # -------------------------------------------------------------------------------
    def test_dist(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            dist = self.sensor.distance()
            if dist == -0.1:
                return 0
            else:
                return 1
        except:
            return 0

    # -------------------------------------------------------------------------------
    # Progression for obtaining distance readings from the sensor
    # -------------------------------------------------------------------------------

    def print_dist(self):
        global dist
        dist = self.sensor.distance()
        vrb_print(str(dist)+" cm",level='low')

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            vrb_print(self.fmt_keys,level='high')
            for s in self.fmt_keys:
                vrb_print(s,level='high')
                vrb_print(eval(s),level='high')
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            data.extend([eval(s) for s in self.fmt_keys])
            self.data_list.extend([data])
            #data_list.extend([data])
            
        display_str = 'distance =\n '+str(round(dist,2))+" cm"
        self.display_str_list = [display_str]


