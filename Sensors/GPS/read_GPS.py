# This script prints GSP readings from a unit attached to uartGPS
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import uartGPS
try:
    from SetUp.platform_defs import p_pwr2
except:
    pass
try:
    from SetUp.platform_defs import p_pwr3
except:
    pass
try:
    from SetUp.platform_defs import p_pwr4
except:
    pass

from sys import print_exception
#from GPS.micropyGPS import MicropyGPS
from GPS.gps import NmeaParser
from time import sleep_ms,ticks_ms,ticks_diff

global GPStime,dec_lat,dec_long,altitude,kph,course
global hours, minutes, seconds, day, month, year

# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_GPS:

    #def __init__(self,num_sentences=3,timeout=30,init_timeout=30,i2c=None,rtc=None,smbus=None,
    #             timeout_ms=5000,sentence_types=["b'$GPGGA"]):
    def __init__(self,num_sentences=3,timeout=30,init_timeout=30,i2c=None,rtc=None,smbus=None,
                 timeout_ms=5000,sentence_types=["b'$GPGGA","b'$GPRMC"]):
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
        
        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be logged        

        self.uartGPS=uartGPS
        self.num_sentences=num_sentences
        self.timeout=timeout
        self.init_timeout=init_timeout
        #self.my_gps = MicropyGPS()  # create GPS parser object
        
        #self.parser = NmeaParser(sentence_types=sentence_types)
        self.sentence_types = sentence_types
        
    # -------------------------------------------------------------------------------
    # Define an explicitly constructed readline for the GPS UART because 
    # the built-in one returns partial lines
    # -------------------------------------------------------------------------------
    def readline(self,timeout_char=1000):
        sentence = b''
        t = ticks_ms() # Get initial time, to compare to timeout limit
        while True:
            if ticks_diff(ticks_ms(), t) >= timeout_char:
                vrb_print('readline timeout reached...')
                break
            else:
                if uartGPS.any():
                    #sentence +=self.uartGPS.read()
                    sentence +=self.uartGPS.read(1)
                    #vrb_print(sentence)
                # Look for end of line
                if sentence.find(b'\n')>-1 or sentence.find(b'\r')>-1:
                    break
        vrb_print(sentence)
        # remove duplicate partial lines
        sentence = b'$' + sentence.rsplit(b'$')[-1] 
        vrb_print(sentence)
        return sentence
        
    def test_GPS(self):
        #self.parser.data = []
        self.parser = NmeaParser(sentence_types=self.sentence_types)
        try: # Try to take a measurement, return 1 if successful, 0 if not
            vrb_print('starting test_GPS')
            self.uartGPS.read() # clear the buffer
            t = ticks_ms() # Get initial time, to compare to timeout limit
            while True:
                if ticks_diff(ticks_ms(), t) >= 1000*self.init_timeout:
                    vrb_print('no response from GPS...')
                    return 0
                else:
                    if uartGPS.any():
                        data = self.readline()
                        #data = self.uartGPS.readline()
                        vrb_print(data)
                        update_success = self.parser.update(data)
                        #try:
                        #    #self.parser.update(data)
                        #    vrb_print(self.parser.data)
                        #except:
                        #    pass
                        if self.parser.valid is True:
                        #if self.parser.valid_sentence is True:
                            #self.parser.data.append(data)
                            vrb_print('update_success: ',update_success)
                            vrb_print('received from GPS: ')
                            vrb_print(self.parser.date,self.parser.timestamp,self.parser.longitude,":",
                                    self.parser.latitude,self.parser.altitude,self.parser.speed,self.parser.course)
                            #self.parser.data=[]
                            return 1                          
        except Exception as e:
            vrb_print('error in query to GPS...')
            print_exception(e)
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining GPS readings from the sensor
    # -------------------------------------------------------------------------------

    def print_GPS(self,display=True):
        global GPStime,dec_lat,dec_long, altitude,kph,course
        # Create a loop to obtain several sentences from the GPS, to make sure
        # all relevant fields in the parser are populated with recent data
        sentence_count = 0
        self.parser = NmeaParser(sentence_types=self.sentence_types)
        #self.parser.data = []
        self.uartGPS.read() # clear the buffer
        t = ticks_ms() # Get initial time, to compare to timeout limit
        while True:
            if ticks_diff(ticks_ms(), t) >= 1000*self.timeout:
                vrb_print('GPS query breaking after time limit ',self.timeout,' s expired with ',sentence_count,' sentences')
                break
            if uartGPS.any():
                data = self.readline()
                #data = self.uartGPS.readline()
                #vrb_print(data)
                update_success = self.parser.update(data)
                if self.parser.valid is True:
                    vrb_print('update_success: ',update_success)
                    vrb_print('received from GPS: ')
                    vrb_print(self.parser.date,self.parser.timestamp,self.parser.longitude,":",
                          self.parser.latitude,self.parser.altitude,self.parser.speed,self.parser.course)

                    # calculate decimal lat and long
                    dec_lat = self.parser.latitude #self.my_gps.latitude[0]+self.my_gps.latitude[1]/60
                    #if self.my_gps.latitude[2]=="S": # correction for southern hemisphere
                    #    dec_lat=-dec_lat
                    dec_long = self.parser.longitude #self.my_gps.longitude[0]+self.my_gps.longitude[1]/60
                    #if self.my_gps.longitude[2]=="W": # correction for western hemisphere
                    #    dec_long=-dec_long
                    vrb_print(self.parser.altitude,self.parser.speed)
                    altitude = self.parser.altitude
                    try:
                        if len(self.parser.speed)==3:
                            kph = self.parser.speed[2]
                        else:
                            kph = -1
                    except:
                        kph = -1
                    course = self.parser.course
                    (day, month, year) = self.parser.date
                    (hours, minutes, seconds) = self.parser.timestamp

                    GPStime=[year,month,day,hours,minutes,seconds]
                    GPSstr='GPS: {}-{}-{} {}:{}:{} {},{},{}'.format(year,month,day,hours,minutes,seconds, \
                                                                    dec_lat,dec_long,altitude)
                    vrb_print(GPSstr)

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
                        flat_data=[]
                        for d in data:
                            if type(d).__name__=='list':
                                for dd in d:
                                    flat_data.append(dd)
                            else:
                                flat_data.append(d)
                        self.data_list.extend([flat_data])
                    break
                
        display_str = 'GPS: {},\n   {}'.format(dec_lat,dec_long)
        self.display_str_list = [display_str]
            
