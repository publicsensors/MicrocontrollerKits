# This script prints GSP readings from a unit attached to uartGPS

# Import platform-specific definitions
from Setup.platform_defs import uartGPS
try:
    from Setup.platform_defs import p_pwr2
except:
    pass
try:
    from Setup.platform_defs import p_pwr3
except:
    pass
try:
    from Setup.platform_defs import p_pwr4
except:
    pass

from os import sync
from GPS.micropyGPS import MicropyGPS
from time import sleep_ms,ticks_ms,ticks_diff

global GPStime,dec_lat,dec_long

# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_GPS:

    def __init__(self,num_sentences=3,timeout=5,init_timeout=15,i2c=None,rtc=None,smbus=None):
        # Turn on GPS power pins, if defined
        for p in ['p_pwr2','p_pwr3','p_pwr4']:
            if p in list(locals().keys()):
                exec(p+'.value(1)')
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0
        
        self.uartGPS=uartGPS
        self.num_sentences=num_sentences
        self.timeout=timeout
        self.init_timeout=init_timeout
        self.my_gps = MicropyGPS()  # create GPS parser object

    # -------------------------------------------------------------------------------
    # Test the GPS sensor
    # -------------------------------------------------------------------------------
    def test_GPS(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            print('starting test_GPS')
            t = ticks_ms() # Get initial time, to compare to timeout limit
            while True:
                if ticks_diff(ticks_ms(), t) >= 1000*self.init_timeout:
                    print('no response from GPS...')
                    return 0
                else:
                    if uartGPS.any():
                        stat = self.my_gps.update(chr(uartGPS.readchar()))
                        if stat:
                            print('recieved from GPS: ',stat)
                            return 1
        except:
            print('error in query to GPS...')
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining GPS readings from the sensor
    # -------------------------------------------------------------------------------

    def print_GPS(self,display=True):
        global GPStime,dec_lat,dec_long
        # Create a loop to obtain several sentences from the GPS, to make sure
        # all relevant fields in the parser are populated with recent data
        sentence_count = 0
        t = ticks_ms() # Get initial time, to compare to timeout limit
        while True:
            if ticks_diff(ticks_ms(), t) >= 1000*self.timeout:
                print('GPS query breaking after time limit ',self.timeout,' s expired with ',sentence_count,' sentences')
                break
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

                    GPStime=[self.my_gps.date[2],self.my_gps.date[1],self.my_gps.date[0], \
                                  self.my_gps.timestamp[0],self.my_gps.timestamp[1],self.my_gps.timestamp[2]]
                    GPSstr='GPS: {}-{}-{} {}:{}:{} {},{}'.format(self.my_gps.date[0],self.my_gps.date[1],self.my_gps.date[2], \
                                                        self.my_gps.timestamp[0],self.my_gps.timestamp[1],self.my_gps.timestamp[2], \
                                                                dec_lat,dec_long)
                    print(GPSstr)

                    data_list = []
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
                        flat_data=[]
                        for d in data:
                            if type(d).__name__=='list':
                                for dd in d:
                                    flat_data.append(dd)
                            else:
                                flat_data.append(d)
                        data_list.extend([flat_data])
                    break
                
        display_str = 'GPS: {},\n   {}'.format(dec_lat,dec_long)
        display_str_list = [display_str]
        return data_list,display_str_list
            
