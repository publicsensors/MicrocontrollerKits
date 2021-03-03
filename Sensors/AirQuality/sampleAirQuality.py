#from machine import UART
from time import sleep

from SetUp.platform_defs import uartAQ
from AirQuality.sds011 import SDS011

#uart = UART(1, baudrate=9600, pins=('P21','P22'))
def sample_AQ():
    dust_sensor = SDS011(uartAQ)
    #dust_sensor = sds011.SDS011(uartAQ)
    dust_sensor.set_reporting_mode_query()
    dust_sensor.sleep()

    while True:
    #Datasheet says to wait for at least 30 seconds...
        print('Start fan for 15 seconds.')
        dust_sensor.wake()
        #sleep(15)
        sleep(65)

        #Returns NOK if no measurement found in reasonable time
        status = dust_sensor.read()
        #Returns NOK if checksum failed
        pkt_status = dust_sensor.packet_status
        
        #Stop fan
        dust_sensor.sleep()
        
        if(status == False):
            print('Measurement failed.')
        elif(pkt_status == False):
            print('Received corrupted data.')
        else:
            print('PM25: ', dust_sensor.pm25)
            print('PM10: ', dust_sensor.pm10)
            
        sleep(45)

        
#while True:
#    status = dust_sensor.read(),print(status),print('PM25: ', dust_sensor.pm25,', PM10: ', dust_sensor.pm10)
#    sleep(20)

