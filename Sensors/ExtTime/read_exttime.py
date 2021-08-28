# This script prints temperature readings from a DS18B20 sensor

# Use driver by roberthh from https://github.com/robert-hh/ads1x15
from ExtTime.urtc import DS3231
#from Light.tsl25x1 import tsl25x1_sensor #, TSL2561, Tsl2591, read_tsl25x1
from time import sleep_ms
from os import sync

global datetime
global year, month, day, weekday, hour, minute, second
# -------------------------------------------------------------------------------
# Set up pins for the external RTC sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_exttime:

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

        self.datetime=None

        # Wrapper function to call DS3231 I2C Real Time Clock
        self.sensor = DS3231(i2c)

    # -------------------------------------------------------------------------------
    # Test the light sensor
    # -------------------------------------------------------------------------------
    def test_exttime(self):
        global datetime
        global year, month, day, weekday, hour, minute, second

        try: # Try to take a measurement, return 1 if successful, 0 if not
            print('testing ds3231...')
            datetime=self.sensor.datetime()
            self.datetime=datetime
            print('test: datetime = ',datetime)
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining voltage 0-3 readings from the sensor
    # -------------------------------------------------------------------------------

    def print_exttime(self):
        global datetime
        global year, month, day, weekday, hour, minute, second

        datetime=self.sensor.datetime()
        self.datetime=datetime
        year=datetime.year
        month=datetime.month
        day=datetime.day
        weekday=datetime.day
        hour=datetime.hour
        minute=datetime.minute
        second=datetime.second

        print('year: ',str(year),' month: ',str(month),' day: ',str(day),' hour: ',str(hour),' minute: ',\
              str(minute),' second: ',str(second))
        if self.lcd is not False:
            try:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr('time '+str(year)+'-'+str(month)+'-'+str(day)+'\n'+str(hour)+':'+\
                                str(minute)+':'+str(second))
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
            sleep_ms(250)
            
