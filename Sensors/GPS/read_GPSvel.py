# A wrapper function for read_GPS, that restricts GPS sentence types to RMC
from GPS.read_GPS import read_GPS

class read_GPSvel(read_GPS):

    def __init__(self,timeout=30,init_timeout=30,i2c=None,rtc=None,smbus=None,
                 sentence_types=["b'$GPRMC"]):
        super().__init__(self)

        self.rtc=rtc
        self.sentence_types=sentence_types
        self.timeout=timeout
        self.init_timeout=init_timeout

        self.test_GPSvel = self.test_GPS
        self.print_GPSvel = self.print_GPS
        
