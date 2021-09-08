# This script prints light readings from TSL2561 and Tsl2591 sensors

from Light.tsl25x1 import tsl25x1_sensor 
from time import sleep_ms
from os import sync
from platform_defs import p_DS18B20, p_pwr1

global full, ir, lux

# -------------------------------------------------------------------------------
# Set up pins for the light sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_light:

    def __init__(self,lcd=False,i2c=None,rtc=None):
        p_pwr1.value(1)
        sleep_ms(250)           # Sleep for 250 ms
        self.i2c=i2c
        self.lcd=lcd
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
        if self.lcd is not False:
            try:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr(str(round(lux,1))+' lux\n('+str(full)+','+str(ir)+')')
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
            
