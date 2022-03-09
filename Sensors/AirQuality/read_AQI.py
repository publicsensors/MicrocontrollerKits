# This script prints AQI readings from a SDS011 attached to uartAQ
from SetUp.verbosity import vrb_print

# Import platform-specific definitions
from SetUp.platform_defs import uartAQ, AQtimer
from AirQuality.sds011 import SDS011
from machine import Timer

from time import sleep_ms,sleep,ticks_ms,ticks_diff

# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_AQI:

    def __init__(self,fan_start_sec=30,init_timeout=30,stop_fan=True,i2c=None,rtc=None,smbus=None):
        self.i2c=i2c
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.fan_start_sec=fan_start_sec
        self.stop_fan=stop_fan
        self.init_timeout=init_timeout
        
        self.AQtimer=AQtimer
        
        self.uartAQ=uartAQ
        self.status=None
        self.pkt_status=None
        self.PM25=-1
        self.PM10=-1
        
        self.data_list = [] # bucket for data to be logged        
        self.display_str_list = [] # bucket for data to be displayed        

        self.dust_sensor = SDS011(uartAQ) # create SDS11 parser object
        self.dust_sensor.set_reporting_mode_query()
        sleep(5)
        self.dust_sensor.wake()
        vrb_print('running fan for ',2,' sec')
        sleep(2)
        if self.stop_fan:
            self.dust_sensor.sleep() # stop fan
        sleep(1)
    
    # -------------------------------------------------------------------------------
    # Test the AQI sensor
    # -------------------------------------------------------------------------------
    def test_AQI(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            vrb_print('starting test_AQI')
            if self.stop_fan: #Start fan
                self.dust_sensor.wake()
                #vrb_print('running fan for ',self.fan_start_sec,' sec')
                #sleep(self.fan_start_sec)
            t = ticks_ms() # Get initial time, to compare to timeout limit
            count = 0
            while True:
                if ticks_diff(ticks_ms(), t) >= 1000*self.init_timeout:
                    vrb_print('no response from AQI within init time limit...')
                    if self.stop_fan: #Stop fan
                        self.dust_sensor.sleep()
                    #return 0
                    vrb_print('AQI testing suspended -- enabling AQI anyways...')
                    return 1
                else:
                    # Initiate a reading
                    count += 1
                    #self.status = self.dust_sensor.read()
                    #vrb_print(count,self.status)
                    #sleep(5)
                    #if self.status:
                    #    vrb_print('AQI status = OK')
                    #    if self.stop_fan: #Stop fan
                    #        self.dust_sensor.sleep()
                    #    return 1
                    self.dust_sensor.query()
                    sleep(1)
                    if self.uartAQ.any():
                        vrb_print('got characters from uartAQ -- enabling AQI sensor')
                        if self.stop_fan: #Stop fan
                            self.dust_sensor.sleep()
                        return 1
                    sleep(4)
        except:
            vrb_print('error in query to AQI sensor...')
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining AQI readings from the sensor
    # -------------------------------------------------------------------------------

    def print_AQI(self):
        global PM25,PM10
        # Turn on fan, and initiate a non-blocking process
        # to take a reading after the specified interval
        if self.stop_fan:
            self.dust_sensor.wake()
        vrb_print('running fan for ',self.fan_start_sec,' sec')
        #self.AQtimer = Timer()
        self.AQtimer.init(mode=Timer.ONE_SHOT,period=1000*self.fan_start_sec,callback=self.print_AQI_read)
        # Return empty lists -- these will be filled when reading is taken
        vrb_print('exiting print_AQI')

    def print_AQI_read(self,t):
        global PM25,PM10
        # Complete the sampling by reading from the SDS011, and
        # displaying/logging the results. t is the timer.
        vrb_print('entering print_AQI_read')
        #Returns NOK if no measurement found in reasonable time
        self.status = self.dust_sensor.read()
        #Returns NOK if checksum failed
        self.pkt_status = self.dust_sensor.packet_status
        
        #Stop fan
        if self.stop_fan:
            self.dust_sensor.sleep()

        # Easiliy recognizable dummy values if sensor fails to return data
        PM25=-1
        PM10=-1
        
        if(self.status == False):
            vrb_print('Measurement failed.')
        elif(self.pkt_status == False):
            vrb_print('Received corrupted data.')
        else:
            PM25= self.dust_sensor.pm25
            PM10= self.dust_sensor.pm10
            vrb_print('PM25: ', PM25)
            vrb_print('PM10: ', PM10)

        # record last measurement in object
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

        display_str = str(round(PM25,1))+' PM25\n'+str(round(PM10,1))+' PM10'
        self.display_str_list = [display_str]

