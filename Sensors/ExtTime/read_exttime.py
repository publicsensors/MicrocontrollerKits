# This script prints temperature readings from a DS18B20 sensor
from SetUp.verbosity import vrb_print
from sys import print_exception

# Use driver by roberthh from https://github.com/robert-hh/ads1x15
from ExtTime.urtc import DS3231
from time import sleep_ms

global datetime
global year, month, day, weekday, hour, minute, second
# -------------------------------------------------------------------------------
# Set up pins for the external RTC sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_exttime:

    def __init__(self,i2c=None,rtc=None,smbus=None):
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.datetime=None

        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be displayed

        # Wrapper function to call DS3231 I2C Real Time Clock
        self.sensor = DS3231(i2c)

    # -------------------------------------------------------------------------------
    # Test the light sensor
    # -------------------------------------------------------------------------------
    def test_exttime(self):
        global datetime
        global year, month, day, weekday, hour, minute, second

        try: # Try to take a measurement, return 1 if successful, 0 if not
            vrb_print('testing ds3231...',level='med')
            datetime=self.sensor.datetime()
            self.datetime=datetime
            vrb_print('test: datetime = ',datetime,level='low')
            vrb_print('Setting onboard RTC...',level='med')
            self.rtc.datetime((self.datetime.year,self.datetime.month,self.datetime.day,0,
                               self.datetime.hour,self.datetime.minute,self.datetime.second,0))
            vrb_print('Onboard RTC set to: ',self.rtc.datetime(),level='med')
            return 1
        except Exception as e:
            print_exception(e)
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

        vrb_print('year: ',str(year),' month: ',str(month),' day: ',str(day),' hour: ',str(hour),' minute: ',\
                  str(minute),' second: ',str(second),level='med')

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            data.extend([eval(s) for s in self.fmt_keys])
            self.data_list.extend([data])
            #data_list.extend([data])

        
        display_str = 'time '+str(year)+'-'+str(month)+'-'+str(day)+',\n'+str(hour)+':'+str(minute)+':'+str(second)
        self.display_str_list = [display_str]
        vrb_print('exttime: display_str = ',display_str,level='low')
        vrb_print('exttime: self.display_str_list = ',self.display_str_list,level='med')
