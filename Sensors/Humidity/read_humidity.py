# This script prints humidity & temperature from a HDC1080 sensor
from SetUp.verbosity import vrb_print

# Use modification of driver by @rubenmoral from
# https://github.com/digidotcom/xbee-micropython/blob/master/lib/sensor/hdc1080/hdc1080.py
from Humidity.hdc1080 import HDC1080
from time import sleep_ms

global values
global temp, humid
# -------------------------------------------------------------------------------

class read_humidity:

    def __init__(self,i2c=None,rtc=None,smbus=None):
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

        # Wrapper function to call BME280 or BMP280 I2C pressure/temperature[/humidity] sensor
        self.sensor = HDC1080(i2c)

    # -------------------------------------------------------------------------------
    # Test the humidity sensor
    # -------------------------------------------------------------------------------
    def test_humidity(self):
        global values
        global temp, humid

        try: # Try to take a measurement, return 1 if successful, 0 if not
            #values=self.sensor.read_compensated_data()
            values=self.sensor.read_humid_temp()
            vrb_print('test: values = ',values)
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining humidity readings and other values from the sensor
    # -------------------------------------------------------------------------------
    def print_humidity(self):
        global values
        global temp, humid

        (humid,temp)=self.sensor.read_humid_temp()

        vrb_print('humid: ',str(humid),'temp: ',str(temp))

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            vrb_print(self.fmt_keys)
            for s in self.fmt_keys:
                vrb_print(s)
                vrb_print(eval(s))
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            vrb_print([s for s in self.fmt_keys])
            vrb_print([eval(s) for s in self.fmt_keys])
            data.extend([eval(s) for s in self.fmt_keys])
            self.data_list.extend([data])
            #data_list.extend([data])
            
        display_str = 'h/t: '+str(humid)+',\n'+str(temp)
        self.display_str_list = [display_str]
