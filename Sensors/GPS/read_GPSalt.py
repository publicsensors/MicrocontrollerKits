# A wrapper function for read_GPS, that restricts GPS sentence types to GGA
from GPS.read_GPS import read_GPS

class read_GPSalt(read_GPS):

    def __init__(self,timeout=30,init_timeout=30,i2c=None,rtc=None,smbus=None,
                 sentence_types=["b'$GPGGA"]):
        super().__init__(self)

        self.rtc=rtc
        self.sentence_types=sentence_types
        self.timeout=timeout
        self.init_timeout=init_timeout

        self.test_GPSalt = self.test_GPS
        self.print_GPSalt = self.print_GPS

