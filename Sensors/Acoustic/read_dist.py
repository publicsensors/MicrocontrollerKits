# This script prints temperature readings from a DS18B20 sensor

# Import platform-specific definitions
from SetUp.platform_defs import *

from machine import Pin, I2C
from Acoustic import hcsr04
from time import sleep_ms
from os import sync

# -------------------------------------------------------------------------------
# Set up pins for the DS18B20
# -------------------------------------------------------------------------------
class read_dist:

    def __init__(self,i2c=None,rtc=None,hcsr_c=343,smbus=None):
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
        print(str(dist)+" cm")

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            print(self.fmt_keys)
            for s in self.fmt_keys:
                print(s)
                print(eval(s))
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            data.extend([eval(s) for s in self.fmt_keys])
            self.data_list.extend([data])
            #data_list.extend([data])
            
        display_str = 'distance =\n '+str(dist)+" cm"
        self.display_str_list = [display_str]


