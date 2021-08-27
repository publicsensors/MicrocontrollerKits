# This script prints AQI readings from a SDS011 attached to uartAQ

# Import platform-specific definitions
from Setup.platform_defs import uartAQ
from AirQuality.sds011 import SDS011

from os import sync
from time import sleep_ms, sleep

# -------------------------------------------------------------------------------
# Set up pins for power and usrtGPS
# -------------------------------------------------------------------------------
class read_AQI:

    def __init__(self,fan_start_sec=60,stop_fan=True,lcd=False,i2c=None,rtc=None):
        self.i2c=i2c
        self.lcd=lcd
        self.rtc=rtc
        self.logging=False
        self.logfilename=None
        self.logfile=None
        self.log_format=None
        self.fmt_keys=None
        self.sample_num=0

        self.fan_start_sec=fan_start_sec
        self.stop_fan=stop_fan
        
        self.uartAQ=uartAQ
        self.status=None
        self.pkt_status=None
        self.PM25=-1
        self.PM10=-1

        self.dust_sensor = SDS011(uartAQ) # create SDS11 parser object
        self.dust_sensor.set_reporting_mode_query()
        if self.stop_fan:
            self.dust_sensor.sleep() # stop fan
            
    
    # -------------------------------------------------------------------------------
    # Test the AQI sensor
    # -------------------------------------------------------------------------------
    def test_AQI(self):
        try: # Try to take a measurement, return 1 if successful, 0 if not
            #full, ir, lux = self.sensor.light()
            return 1
        except:
            return 0
        
    # -------------------------------------------------------------------------------
    # Progression for obtaining GPS readings from the sensor
    # -------------------------------------------------------------------------------

    def print_AQI(self,display=True, pr=1):
        global PM25,PM10
        # Create a loop to obtain several sentences from the GPS, to make sure
        # all relevant fields in the parser are populated with recent data

        if self.stop_fan:
            self.dust_sensor.wake()
            print('running fan for ',self.fan_start_sec,' sec')
            if self.lcd is not False:
                try:
                    self.lcd.clear()      # Sleep for 1 sec
                    self.lcd.putstr('AQI: running fan for '+str(self.fan_start_sec)+' sec')
                except:
                    pass
            sleep(self.fan_start_sec)

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
            print('Measurement failed.')
        elif(self.pkt_status == False):
            print('Received corrupted data.')
        else:
            PM25= self.dust_sensor.pm25
            PM10= self.dust_sensor.pm10
            print('PM25: ', PM25)
            print('PM10: ', PM10)

        # record last measurement in object
        self.PM25=PM25
        self.PM10=PM10

        if self.lcd is not False:
            try:
                self.lcd.clear()      # Sleep for 1 sec
                self.lcd.putstr(str(round(PM25,1))+' PM25\n'+str(round(PM10,1))+' PM10')
            except:
                pass
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
            sleep_ms(250)


