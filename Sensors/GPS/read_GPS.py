# This script prints GSP readings from a unit attached to uartGPS

# Import platform-specific definitions
from platform_defs import *

from machine import Pin, I2C
from esp8266_i2c_lcd import I2cLcd
from GPS.micropyGPS import MicropyGPS
from time import sleep_ms


# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_GPS:

    def __init__(self,num_sentences=3,timeout=5):
        p_pwr2.value(1)  # turn on power to the GPS
        p_pwr3.value(1)  # the GPS requires power from multiple GPIOs
        p_pwr4.value(1)

        self.num_sentences=num_sentences
        self.timeout=timeout
        self.my_gps = MicropyGPS()  # create GPS parser object

    # -------------------------------------------------------------------------------
    # Progression for obtaining GPS readings from the sensor
    # -------------------------------------------------------------------------------

    def print_GPS(self,display=True, pr=1):
        i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
        try:
            lcd = I2cLcd(i2c, 0x27,2,16)
            lcdF = 1
        except:
            lcdF = 0
        # Create a loop to obtain several sentences from the GPS, to make sure
        # all relevant fields in the parser are populated with recent data
        sentence_count = 0
        while True:
            if uartGPS.any():
                stat = self.my_gps.update(chr(uartGPS.readchar()))
                if stat:
                    print(stat)
                    stat = None
                    sentence_count += 1

                if sentence_count == self.num_sentences: # have necessary fixes, output data and return
                    # calculate decimal lat and long
                    dec_lat=self.my_gps.latitude[0]+self.my_gps.latitude[1]/60
                    if self.my_gps.latitude[2]=="S": # correction for southern hemisphere
                        dec_lat=-dec_lat
                    dec_long=self.my_gps.longitude[0]+self.my_gps.longitude[1]/60
                    if self.my_gps.longitude[2]=="W": # correction for western hemisphere
                        dec_long=-dec_long

                    if not display: # if False, return GPS data instead of displaying it
                        return (self.my_gps.date,self.my_gps.timestamp,dec_lat,dec_long)

                    #print('UTC Timestamp:', self.my_gps.timestamp)
                    #print('Date:', self.my_gps.date_string('long'))
                    #print('Latitude:', self.my_gps.latitude_string())
                    #print('Longitude:', self.my_gps.longitude_string())
                    #print('Altitude:', self.my_gps.altitude)#_string())
                    #print('Speed:', self.my_gps.speed_string())
                    #print('Compass direction:', self.my_gps.compass_direction())
                    #print('Course:', self.my_gps.course)#_string())
                    #print('Horizontal Dilution of Precision:', self.my_gps.hdop)
                    #print()
                    GPSstr='GPS: {}-{}-{} {}:{}:{} {},{}'.format(self.my_gps.date[0],self.my_gps.date[1],self.my_gps.date[2], \
                                                        self.my_gps.timestamp[0],self.my_gps.timestamp[1],self.my_gps.timestamp[2], \
                                                                dec_lat,dec_long)
                    print(GPSstr)
                    #print('GPS: {} {} {} {}'.format(self.my_gps.timestamp,self.my_gps.date,self.my_gps.latitude,self.my_gps.longitude))
                    if lcdF == 1 & pr==1:
                        lcd.clear()      # Sleep for 1 sec
                        #GPSstr2='GPS: {}:{}:{} {},{}'.format(self.my_gps.timestamp[0],self.my_gps.timestamp[1], \
                        #                                     self.my_gps.timestamp[2],dec_lat,dec_long)
                        GPSstr2='GPS: {},\n   {}'.format(dec_lat,dec_long)
                        lcd.putstr(GPSstr2)
                        #lcd.putstr('GPS: {} {} {} {}'.format(self.my_gps.timestamp,self.my_gps.date,dec_lat,dec_long))
                    break;

    # -------------------------------------------------------------------------------
    # Get continuous GPS readings
    # -------------------------------------------------------------------------------
    def print_GPSs_start(self,samp_max=1000,interval=5):
        sleep_microsec=int(1000*interval)
        pause_microsec=1000
        i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
        try:
            lcd = I2cLcd(i2c, 0x27,2,16)
            lcdF = 1
        except:
            lcdF = 0
        sample_num=1            # Start sample number at 0 so we can count the number of samples we take
        while sample_num <= samp_max:            # This will repeat in a loop, until we terminate with a ctrl-c
            (date,timestamp,dec_lat,dec_long) = self.print_GPS(display=False)
            print("Sample: ",sample_num,', ',date,', ',timestamp,', ',dec_lat,', ',dec_long) # print the sample number and temperature
            print("\n")         # Print a line of space between temp readings so it is easier to read
            if lcdF ==1:
                lcd.clear()      # Sleep for 1 sec
                GPSstr3='#{} {},{}'.format(sample_num,dec_lat,dec_long)
                lcd.putstr(GPSstr3)
                #lcd.putstr("Sample: "+str(sample_num)+"\nTemp: "+str(round(self.ds.read_GPS(self.roms[0]),2))+" C")
            sleep_ms(max(sleep_microsec-pause_microsec,0))      # Wait 5 sec, before repeating the loop and taking another reading
            sample_num+=1       # Increment the sample number for each reading
        if lcdF == 1:
            lcd.clear()
            lcd.putstr("Done!")
            sleep_ms(2000)
            lcd.clear()
