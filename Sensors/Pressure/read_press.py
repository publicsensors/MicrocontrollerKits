# This script prints pressure, temperature, and (if available) humidity readings from a BMe280 or BMP280 sensor

# Use driver by roberthh from https://github.com/robert-hh/BME280
from Pressure.bme280_float import BME280
from time import sleep_ms
from os import sync

global values
global temp, press, humid
# -------------------------------------------------------------------------------
# Set up pins for the light sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_press:

    def __init__(self,i2c=None,rtc=None,smbus=None):
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        # Wrapper function to call BME280 or BMP280 I2C pressure/temperature[/humidity] sensor
        self.sensor = BME280(i2c=i2c)

    # -------------------------------------------------------------------------------
    # Test the pressure sensor
    # -------------------------------------------------------------------------------
    def test_press(self):
        global values
        global temp, press, humid

        try: # Try to take a measurement, return 1 if successful, 0 if not
            #values=self.sensor.read_compensated_data()
            values=self.sensor.values
            print('test: values = ',values)
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining pressure readings and other values from the sensor
    # -------------------------------------------------------------------------------
    def print_press(self):
        global values
        global temp, press, humid

        (temp,press,humid)=self.sensor.read_compensated_data()

        print('temp: ',str(temp),'press: ',str(press),'humid: ',str(humid))

        if self.logging:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            self.sample_num+=1
            print(self.fmt_keys)
            for s in self.fmt_keys:
                print(s)
                print(eval(s))
            data=[self.sample_num]
            data.extend([t for t in timestamp])
            print([s for s in self.fmt_keys])
            print([eval(s) for s in self.fmt_keys])

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
            
        display_str = 't/p/h: '+temp+',\n'+press+','+humid
        return display_str
