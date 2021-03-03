# This script prints temperature readings from a DS18B20 sensor

# Import platform-specific definitions
#from platform_defs import *
from platform_defs import p_DS18B20
#from machine import Pin, I2C
#from SetUp.esp8266_i2c_lcd import I2cLcd
from onewire import OneWire
from Temperature.ds18x20 import DS18X20
from time import sleep_ms
from os import sync

global T

# -------------------------------------------------------------------------------
# Set up pins for the DS18B20
# -------------------------------------------------------------------------------
class read_temp:

    def __init__(self,lcd=False,i2c=None,rtc=None):
        #p_pwr1.value(1)
        self.i2c=i2c
        self.lcd=lcd
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        ow = OneWire(p_DS18B20)   # Pin 13 is the data pin for the DS18B20
        self.ds = DS18X20(ow)        # Initialize a ds18b20 object
        self.roms = self.ds.scan()   # Find all the DS18B20 sensors that are attached (we only have one)

    # -------------------------------------------------------------------------------
    # Test the temperature sensor
    # -------------------------------------------------------------------------------
    def test_temp(self):
        if not self.roms: # Check to see if there is a DS18B20 attached/found
            print('Error: No temperature sensor address found')#
            return 0
        else:
            print('DS18B20 address: ',str(self.roms))
            try: # Try to take a measurement, return 1 if successful, 0 if not
                self.ds.convert_temp()       # Obtain temp readings from each of those sensors
                sleep_ms(750)           # Sleep for 750 ms, to give the sensors enough time to report their temperature readings
                self.ds.read_temp(self.roms[0])
                return 1
            except:
                return 0

    # -------------------------------------------------------------------------------
    # Progression for obtaining temperature readings from the sensor
    # -------------------------------------------------------------------------------
    def print_temp(self):
        global T
        self.ds.convert_temp()       # Obtain temp readings from each of those sensors
        sleep_ms(750)           # Sleep for 750 ms, to give the sensors enough time to report their temperature readings
        T = self.ds.read_temp(self.roms[0])
        print("Temp: ",T, ' C')
        if self.lcd is not False:
            self.lcd.clear()      # Sleep for 1 sec
            self.lcd.putstr("Temp: "+str(round(T,2))+" C")
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
            print('data = ',data)
            print('self.log_format=',self.log_format)
            log_line=self.log_format % tuple(data)
            print('log_line = ',log_line)
            print('logging to filename: ',self.logfilename)
            logfile=open(self.logfilename,'a')
            logfile.write(log_line)
            logfile.close()
            sync()
            sleep_ms(250)

