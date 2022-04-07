# This script prints CO2 readings from an MHZ19C attached to uartAQ
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import uartAQ
from CO2.mhz19UART import mhz19

global ppm, temp, co2status
# -------------------------------------------------------------------------------
# Set up pins for power and usatAQ
# -------------------------------------------------------------------------------
class read_CO2:

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
        self.co2status=None
        self.temp=None
        self.ppm=-1
        
        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be displayed        

        self.sensor = mhz19(uartAQ)
    
    # -------------------------------------------------------------------------------
    # Test the CO2 sensor
    # -------------------------------------------------------------------------------
    def test_CO2(self):
        global ppm, temp, co2status
        try: # Try to take a measurement, return 1 if successful, 0 if not
        #if True:
            vrb_print('starting test_CO2')
            self.sensor.get_data()
            self.ppm = self.sensor.ppm
            self.co2status = self.sensor.co2status
            self.temp = self.sensor.temp
            vrb_print('CO2 sensor test: ppm = {}, temp = {}, co2status = []'.format(self.ppm,self.temp,self.co2status))
            return 1
        except:
            vrb_print('error in query to CO2 sensor...')
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining AQI readings from the sensor
    # -------------------------------------------------------------------------------

    def print_CO2(self):
        global ppm, temp, co2status
        # Complete the sampling by reading from the SDS011, and
        # displaying/logging the results. t is the timer.
        vrb_print('entering print_CO2')
        self.sensor.get_data()
        self.ppm = self.sensor.ppm
        self.co2status = self.sensor.co2status
        self.temp = self.sensor.temp
        vrb_print('CO2 sensor test: ppm = {}, temp = {}, co2status = []'.format(self.ppm,self.temp,self.co2status))
        ppm = self.ppm
        temp = self.temp
        co2status = self.co2status

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

        display_str = str(ppm)+' ppm CO2\n'+str(temp)+' deg C'
        self.display_str_list = [display_str]

