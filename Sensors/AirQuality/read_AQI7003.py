# This script prints AQI readings from a SDS011 attached to uartAQ
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import uartAQ, AQtimer
from AirQuality.pms7003 import Pms7003

#from time import sleep_ms,sleep,ticks_ms,ticks_diff

# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_AQI7003:

    def __init__(self,i2c=None,rtc=None,smbus=None):
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.uartAQ=uartAQ

        self.PM1=-1
        self.PM25=-1
        self.PM10=-1
        
        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be displayed        

        self.pms7003 = Pms7003(uartAQ)
    
    # -------------------------------------------------------------------------------
    # Test the AQI sensor
    # -------------------------------------------------------------------------------
    def test_AQI7003(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            vrb_print('starting test_AQI7003')
            pms_data = None
            pms_data = self.pms7003.read()
            if pms_data['VERSION']>0:
                return 1
            else:
                return 0
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining AQI readings from the sensor
    # -------------------------------------------------------------------------------

    def print_AQI7003(self):
        global PM1,PM25,PM10
        pms_data = self.pms7003.read()
        # Use atmospheric environment variation of measurements, units = ug/m^3
        atmos_env=True # Compensates for non-standard air temp?
        PM1 = pms_data['PM1_0_ATM']
        PM25 = pms_data['PM2_5_ATM']
        PM10 = pms_data['PM10_0_ATM']

        # record last measurement in object
        self.PM1=PM1
        self.PM25=PM25
        self.PM10=PM10

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            vrb_print(self.fmt_keys)
            for s in self.fmt_keys:
                vrb_print(s)
                vrb_print(eval(s))
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            data.extend([eval(s) for s in self.fmt_keys])
            self.data_list.extend([data])

        display_str = str(round(PM1,1))+' PM1    '+str(round(PM25,1))+' PM25\n'+str(round(PM10,1))+' PM10'
        self.display_str_list = [display_str]

