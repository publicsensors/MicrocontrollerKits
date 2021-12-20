# This script prints UV, IR and visible light reading in lux from a SI1132 sensor
# The driver for this sensor, derived from https://github.com/ControlEverythingCommunity/SI1132,
# uses an SMBus interface rather than I2C.

from UV_IR_Visible.si1132 import SI1132 
from time import sleep_ms
from os import sync
from platform_defs import p_pwr1

global uv, ir, vis

# -------------------------------------------------------------------------------
# Set up pins for the UIV sensor; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_UIV:

    def __init__(self,lcd=False,i2c=None,rtc=None,smbus=None):
        p_pwr1.value(1)
        sleep_ms(250)           # Sleep for 250 ms
        #self.i2c=i2c
        self.smbus=smbus
        self.lcd=lcd
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

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
        if self.lcd is not False:
            try:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr(str(round(uv,1))+' uv\n('+str(ir)+','+str(vis)+')')
            except:
                pass
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
            sleep_ms(500)
            
