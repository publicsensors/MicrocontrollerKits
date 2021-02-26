# This script prints temperature readings from a DS18B20 sensor

# Import platform-specific definitions
from platform_defs import *

from machine import Pin, I2C
from SetUp.esp8266_i2c_lcd import I2cLcd
from Light.tsl25x1 import tsl25x1_sensor #, TSL2561, Tsl2591, read_tsl25x1
from time import sleep_ms

# -------------------------------------------------------------------------------
# Set up pins for the light sensors; power from either Vbat or p_pwr1 pin (defined in platform_defs)
# -------------------------------------------------------------------------------
class read_light:

    def __init__(self,lcd=False,i2c=None):
        p_pwr1.value(1)
        self.i2c=i2c
        self.lcd=lcd

        # Wrapper function to synonymize calls to TSL2561 and TSL2591 light sensors
        self.sensor = tsl25x1_sensor(i2c=self.i2c)

    # -------------------------------------------------------------------------------
    # Test the light sensor
    # -------------------------------------------------------------------------------
    def test_light(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            full, ir, lux = self.sensor.light()
            return 1
        except:
            return 0
    # -------------------------------------------------------------------------------
    # Progression for obtaining light readings from the sensor
    # -------------------------------------------------------------------------------

    def print_light(self):
        full, ir, lux = self.sensor.light()
        print('full: ',str(full),' ir: ',str(ir))
        if self.lcd is not False:
            self.lcd.clear()      # Sleep for 1 sec
            self.lcd.putstr(str(round(lux,1))+' lux\n('+str(full)+','+str(ir)+')')

    # -------------------------------------------------------------------------------
    # Get continuous light measurements
    # -------------------------------------------------------------------------------
    def print_light_start(self,samp_max=1000,interval=5):
        sleep_microsec=int(1000*interval)
        pause_microsec=1000
        sample_num=1            # Start sample number at 0 so we can count the number of samples we take
        while sample_num <= samp_max:            # This will repeat in a loop, until we terminate with a ctrl-c
            full, ir, lux  = self.sensor.light()   # Obtain a distance reading
            sleep_ms(pause_microsec)      # Sleep for 1 sec
            print("Sample: ",sample_num, ', full: ',str(full),' ir: ',str(ir)) # print the sample number and distance
            print("\n")         # Print a line of space between temp readings so it is easier to read
            if self.lcd is not False:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr("# "+str(sample_num)+': '+str(round(lux,1))+' lux\n('+str(full)+','+str(ir)+')')
            sleep_ms(max(sleep_microsec-pause_microsec,0))      # Wait 5 sec, before repeating the loop and taking another reading
            sample_num+=1       # Increment the sample number for each reading
        if self.lcd is not False:
            self.lcd.clear()
            self.lcd.putstr("Done!")
            self.sleep_ms(2000)
            self.lcd.clear()
            
