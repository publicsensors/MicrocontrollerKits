# This script prints temperature readings from a DS18B20 sensor

# Import platform-specific definitions
from SetUp.platform_defs import p_DS18B20, p_pwr1
from onewire import OneWire
from Temperature.ds18x20 import DS18X20
from time import sleep_ms
from os import sync

global T

# -------------------------------------------------------------------------------
# Set up pins for the DS18B20
# -------------------------------------------------------------------------------
class read_temp:

    def __init__(self,i2c=None,rtc=None,smbus=None):
        p_pwr1.value(1)
        sleep_ms(250)           # Sleep for 250 ms
        self.i2c=i2c
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
                print('test temp = ')
                print(self.ds.read_temp(self.roms[0]))
                return 1
            except:
                return 0

    # -------------------------------------------------------------------------------
    # Progression for obtaining temperature readings from the sensor
    # -------------------------------------------------------------------------------
    def print_temp(self):
        global T
        self.ds.convert_temp()       # Obtain temp readings from each of those sensors
        sleep_ms(750)           # Sleep for 750 ms, to give the sensors enough time to
                                # report their temperature readings
        T = self.ds.read_temp(self.roms[0])
        print("Temp: ",T, ' C')

        data_list = []
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
            data_list.extend([data])
            
        display_str = "Temp: "+str(round(T,2))+" C"
        return data_list,display_str
