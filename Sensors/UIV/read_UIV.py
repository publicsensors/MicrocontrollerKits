# This script prints UV, IR and visible light reading in lux from a SI1132 sensor
# The driver for this sensor, derived from https://github.com/ControlEverythingCommunity/SI1132,
# uses an SMBus interface rather than I2C.

from UV_IR_Visible.si1132 import SI1132 
from time import sleep_ms
from platform_defs import p_pwr1

global uv, ir, vis

# -------------------------------------------------------------------------------
class read_UIV:

    def __init__(self,i2c=None,rtc=None,smbus=None):
        p_pwr1.value(1)
        sleep_ms(250)           # Sleep for 250 ms
        self.smbus=smbus
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be logged        

        # Initialize the SI1132 object
        self.sensor = SI1132(smbus=self.smbus)

    # -------------------------------------------------------------------------------
    # Test the UIV sensor
    # -------------------------------------------------------------------------------
    def test_UIV(self):
        global uv,ir,vis
        try: # Try to take a measurement, return 1 if successful, 0 if not
            uv, ir, vis = self.sensor.read()
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining UIV readings from the sensor
    # -------------------------------------------------------------------------------

    def print_(self):
        global uv,ir,vis
        uv, ir, vis = self.sensor.read()
        print('uv: ',str(uv),' ir: ',str(ir),' vis: ',str(vis))

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
            
        display_str = str(round(uv,1))+' uv\n('+str(ir)+','+str(vis)+')'
        self.display_str_list = [display_str]
