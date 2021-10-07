# This script prints color readings from a TCS34725 sensor

from Color.tcs34725 import TCS34725
from time import sleep_ms
from os import sync

global R, G, B, full

# -------------------------------------------------------------------------------
# Set up pins for the color sensor; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_color:

    def __init__(self,lcd=False,i2c=None,rtc=None):
        self.i2c=i2c
        self.lcd=lcd
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        # Wrapper function to call tcs34725 sensor
        #self.sensor = tsl25x1_sensor(i2c=self.i2c)
        self.sensor = TCS34725(self.i2c)
    # -------------------------------------------------------------------------------
    # Test the color sensor
    # -------------------------------------------------------------------------------
    def test_color(self):
        global R, G, B, full
        try: # Try to take a measurement, return 1 if successful, 0 if not
            R, G, B, full = self.sensor.read(True)
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining color readings from the sensor
    # -------------------------------------------------------------------------------

    def print_color(self):
        global R, G, B, full
        R, G, B, full = self.sensor.read(True)
        print('R, G, B, full: ',str(R),', ',str(G),', ',str(B),', ',str(full))
        if self.lcd is not False:
            try:
                self.lcd.clear()      # Clear and sleep for 1 sec
                sleep_ms(1000)
                self.lcd.putstr('RGB = ('+str(R)+','+str(G)+','+str(B)+')'+'\nfull='+str(full))
                sleep_ms(1000)
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
            