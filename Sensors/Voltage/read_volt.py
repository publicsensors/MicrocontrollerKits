# This script prints temperature readings from a DS18B20 sensor

# Use driver by roberthh from https://github.com/robert-hh/ads1x15
from Voltage.ads1x15 import ADS1115
from time import sleep_ms
from os import sync

global raw0, raw1, raw2, raw3
global volt0, volt1, volt2, volt3
# -------------------------------------------------------------------------------
# Set up pins for the light sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_volt:

    def __init__(self,i2c=None,rtc=None,addr=72,gain=4,rate=0,smbus=None):
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.addr=addr
        self.gain=gain   # previous value gain=2
        self.rate=rate   # previous value rate=4


        # Wrapper function to call ADS1115 I2C voltage sensor
        self.sensor = ADS1115(i2c, self.addr, self.gain)

    # -------------------------------------------------------------------------------
    # Test the light sensor
    # -------------------------------------------------------------------------------
    def test_volt(self):
        global raw0, raw1, raw2, raw3
        global volt0, volt1, volt2, volt3

        try: # Try to take a measurement, return 1 if successful, 0 if not
            raw0=self.sensor.read(self.rate,0)
            volt0=self.sensor.raw_to_v(raw0)
            print('test: volt0 = ',volt0)
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining voltage 0-3 readings from the sensor
    # -------------------------------------------------------------------------------
    def print_volt(self):
        global raw0, raw1, raw2, raw3
        global volt0, volt1, volt2, volt3

        raw0=self.sensor.read(self.rate,0)
        volt0=self.sensor.raw_to_v(raw0)
        raw1=self.sensor.read(self.rate,1)
        volt1=self.sensor.raw_to_v(raw1)
        raw2=self.sensor.read(self.rate,2)
        volt2=self.sensor.raw_to_v(raw2)
        raw3=self.sensor.read(self.rate,3)
        volt3=self.sensor.raw_to_v(raw3)

        print('volt0: ',str(volt0),'volt1: ',str(volt1),'volt2: ',str(volt2),'volt3: ',str(volt3))

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
            
        display_str = 'volts: '+str(round(volt0,3))+',\n'+str(round(volt1,3))+','+str(round(volt2,3))+','+str(round(volt3,3))
        return display_str
            
