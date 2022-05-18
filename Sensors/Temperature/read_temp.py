# This script prints temperature readings from a DS18B20 sensor
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import p_DS18B20, p_pwr1
from onewire import OneWire
from Temperature.ds18x20 import DS18X20
from time import sleep_ms
from ubinascii import hexlify

global T, sensor_id

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

        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be logged        

        ow = OneWire(p_DS18B20)   # Pin 13 is the data pin for the DS18B20
        self.ds = DS18X20(ow)        # Initialize a ds18b20 object
        self.roms = self.ds.scan()   # Find all the DS18B20 sensors that are attached (we only have one)

    # -------------------------------------------------------------------------------
    # Test the temperature sensor
    # -------------------------------------------------------------------------------
    def test_temp(self):
        if not self.roms: # Check to see if there is a DS18B20 attached/found
            vrb_print('Error: No temperature sensor address found',level='low')#
            return 0
        else:
            vrb_print('DS18B20 address: ',str(self.roms),level='med')
            try: # Try to take a measurement, return 1 if successful, 0 if not
                self.ds.convert_temp()       # Obtain temp readings from each of those sensors
                sleep_ms(750)           # Sleep for 750 ms, to give the sensors enough time to
                                        # report their temperature readings
                vrb_print('test temp = ',level='low')
                vrb_print(self.ds.read_temp(self.roms[0]),level='low')
                return 1
            except:
                return 0

    # -------------------------------------------------------------------------------
    # Progression for obtaining temperature readings from the sensor
    # -------------------------------------------------------------------------------
    def print_temp(self):
        global T, sensor_id
        self.roms = self.ds.scan()   # Rescan to find currently alive DS18B20 sensors
        self.ds.convert_temp()       # Obtain temp readings from each of those sensors
        sleep_ms(750)           # Sleep for 750 ms, to give the sensors enough time to
                                # report their temperature readings
        timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
        self.sample_num+=1
        for rom in self.roms:
            sensor_id=str(hexlify(rom))[2:-1]
            T = self.ds.read_temp(rom)
            vrb_print("Temp: ",T, ' C',level='med')
            vrb_print(self.fmt_keys,level='high')
            if self.logging:
                for s in self.fmt_keys:
                    vrb_print(s,level='high')
                    vrb_print(eval(s),level='high')
                data=[self.sample_num]
                data.extend([t for t in timestamp])
                data.extend([eval(s) for s in self.fmt_keys])
                self.data_list.extend([data])
            display_str = "Temp: "+str(round(T,2))+" C\nID: "+sensor_id[2:7]
            self.display_str_list.extend([display_str])
