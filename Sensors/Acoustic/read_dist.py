# This script prints temperature readings from a DS18B20 sensor

# Import platform-specific definitions
from platform_defs import *

from machine import Pin, I2C
from esp8266_i2c_lcd import I2cLcd
from Acoustic import hcsr04
from time import sleep_ms

# -------------------------------------------------------------------------------
# Set up pins for the DS18B20
# -------------------------------------------------------------------------------
class read_dist:

    def __init__(self,lcd=False,i2c=None):
        p_pwr1.value(1)
        self.i2c=i2c
        self.lcd=lcd

        self.sensor = hcsr04.HCSR04(trigger_pin = p_hcsr_trig, echo_pin = p_hcsr_echo, c = hcsr_c)

    # -------------------------------------------------------------------------------
    # Test the distance sensor
    # -------------------------------------------------------------------------------
    def test_dist(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            dist = self.sensor.distance()
            if dist == -0.1:
                return 0
            else:
                return 1
        except:
            return 0

    # -------------------------------------------------------------------------------
    # Progression for obtaining distance readings from the sensor
    # -------------------------------------------------------------------------------

    def print_dist(self):
        dist = self.sensor.distance()
        print(str(dist)+" cm")
        if self.lcd is not False:
            self.lcd.clear()      # Sleep for 1 sec
            self.lcd.putstr(str(dist)+" cm")

    # -------------------------------------------------------------------------------
    # Get continuous distance measurements
    # -------------------------------------------------------------------------------
    def print_dist_start(self,samp_max=1000,interval=5):
        sleep_microsec=int(1000*interval)
        pause_microsec=1000
        sample_num=1            # Start sample number at 0 so we can count the number of samples we take
        while sample_num <= samp_max:            # This will repeat in a loop, until we terminate with a ctrl-c
            dist = self.sensor.distance()   # Obtain a distance reading
            sleep_ms(pause_microsec)      # Sleep for 1 sec
            print("Sample: ",sample_num, ',', str(dist)+" cm") # print the sample number and distance
            print("\n")         # Print a line of space between temp readings so it is easier to read
            if self.lcd is not False:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr("Sample: "+str(sample_num)+"\nDist: "+str(dist)+" cm")
            sleep_ms(max(sleep_microsec-pause_microsec,0))      # Wait 5 sec, before repeating the loop and taking another reading
            sample_num+=1       # Increment the sample number for each reading
        if self.lcd is not False:
            self.lcd.clear()
            self.lcd.putstr("Done!")
            sleep_ms(2000)
            self.lcd.clear()
