# This script prints light readings from TSL2561 and Tsl2591 sensors

from Light.tsl25x1 import tsl25x1_sensor 
from time import sleep_ms
try:
    from os import sync
except:
    pass
from platform_defs import p_pwr1

global full, ir, lux

# -------------------------------------------------------------------------------
# Set up pins for the light sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_light:

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

        # Wrapper function to synonymize calls to TSL2561 and TSL2591 light sensors
        self.sensor = tsl25x1_sensor(i2c=self.i2c)

    # -------------------------------------------------------------------------------
    # Test the light sensor
    # -------------------------------------------------------------------------------
    def test_light(self):
        global full,ir,lux
        try: # Try to take a measurement, return 1 if successful, 0 if not
            full, ir, lux = self.sensor.light()
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining light readings from the sensor
    # -------------------------------------------------------------------------------

    def print_light(self):
        global full,ir,lux
        full, ir, lux = self.sensor.light()
        print('full: ',str(full),' ir: ',str(ir))

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
        
        display_str_list = [str(round(lux,1))+' lux\n('+str(full)+','+str(ir)+')']
        return data_list,display_str_list
