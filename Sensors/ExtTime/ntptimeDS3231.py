try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct
from SetUp.verbosity import vrb_print

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "pool.ntp.org"

def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime():
    t = time()
    import machine
    import utime
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    vrb_print(utime.localtime(),level='med')


def settimeDS3231(sclPin=5, sdaPin=4):
    t = time()
    import urtc
    from machine import I2C, Pin
    import utime
    tm = utime.localtime(t)
    #tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    i2c = I2C(scl=Pin(sclPin), sda=Pin(sdaPin))
    rtc = urtc.DS1307(i2c)
    #machine.RTC().datetime(tm)
    datetime = urtc.datetime_tuple(year=tm[0], month=tm[1], day=tm[2],hour=tm[3],minute=tm[4],second=tm[5])
    vrb_print('setting urtc datetime to: ',datetime,level='low')
    rtc.datetime(datetime)
    #rtc.datetime(tm)
    datetime = rtc.datetime()
    vrb_print('Verifying datetime: ',datetime,level='high')
