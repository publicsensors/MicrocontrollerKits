#
#    tsl25x1.py: combined drivers for Adafruit tsl2561 and tsl2591 light sensors, for PublicSensors/SensoresPublicos
#    microcontroller kits and instruments.
#
#    Derived with minimal modifications from https://github.com/jfischer/micropython-tsl2591,
#    https://github.com/adafruit/micropython-adafruit-tsl2561
#
#    A wrapper function, read_tsl25x1, returns lux, full spectrum and IR light readings
#    from either or both tsl2561 and tsl2591 sensors attached to the I2C bus specified
#    in platform_defs.py for the relevant microcontroller board.
#
#    Modified 20210225 by DG to accept an externally generated I2C object

from time import sleep, sleep_ms
from struct import pack, unpack
from machine import Pin
from gc import collect
collect()


# tsl2591 lux sensor interface

VISIBLE = 2
INFRARED = 1
FULLSPECTRUM = 0

ADDR = 0x29
READBIT = 0x01
COMMAND_BIT = 0xA0
CLEAR_BIT = 0x40
WORD_BIT = 0x20
BLOCK_BIT = 0x10
ENABLE_POWERON = 0x01
ENABLE_POWEROFF = 0x00
ENABLE_AEN = 0x02
ENABLE_AIEN = 0x10
CONTROL_RESET = 0x80
LUX_DF = 408.0
LUX_COEFB = 1.64
LUX_COEFC = 0.59
LUX_COEFD = 0.86

REGISTER_ENABLE = 0x00
REGISTER_CONTROL = 0x01
REGISTER_THRESHHOLDL_LOW = 0x02
REGISTER_THRESHHOLDL_HIGH = 0x03
REGISTER_THRESHHOLDH_LOW = 0x04
REGISTER_THRESHHOLDH_HIGH = 0x05
REGISTER_INTERRUPT = 0x06
REGISTER_CRC = 0x08
REGISTER_ID = 0x0A
REGISTER_CHAN0_LOW = 0x14
REGISTER_CHAN0_HIGH = 0x15
REGISTER_CHAN1_LOW = 0x16
REGISTER_CHAN1_HIGH = 0x17
INTEGRATIONTIME_100MS = 0x00
INTEGRATIONTIME_200MS = 0x01
INTEGRATIONTIME_300MS = 0x02
INTEGRATIONTIME_400MS = 0x03
INTEGRATIONTIME_500MS = 0x04
INTEGRATIONTIME_600MS = 0x05

GAIN_LOW = 0x00
GAIN_MED = 0x10
GAIN_HIGH = 0x20
GAIN_MAX = 0x30

def _bytes_to_int(data):
    return data[0] + (data[1]<<8)

#from machine import I2C, Pin
class SMBusEmulator:
    __slots__ = ('i2c',)
    def __init__(self, i2c=None):
        self.i2c = i2c

    def write_byte_data(self, addr, cmd, val):
        buf = bytes([cmd, val])
        self.i2c.writeto(addr, buf)

    def read_word_data(self, addr, cmd):
        assert cmd < 256
        buf = bytes([cmd])
        self.i2c.writeto(addr, buf)
        data = self.i2c.readfrom(addr, 4)
        return _bytes_to_int(data)
    
SENSOR_ADDRESS=0x29

class Tsl2591:
    def __init__(
                 self,
                 sensor_id=None,
                 integration=INTEGRATIONTIME_100MS,
                 gain=GAIN_LOW,
                 i2c=None):
        self.i2c=i2c
        self.sensor_id = sensor_id
        self.bus = SMBusEmulator(i2c=self.i2c)
        #self.bus = SMBusEmulator()
        self.integration_time = integration
        self.gain = gain
        self.set_timing(self.integration_time)
        self.set_gain(self.gain)
        self.disable()

    def set_timing(self, integration):
        self.enable()
        self.integration_time = integration
        self.bus.write_byte_data(
                    SENSOR_ADDRESS,
                    COMMAND_BIT | REGISTER_CONTROL,
                    self.integration_time | self.gain
                    )
        self.disable()

    def set_gain(self, gain):
        self.enable()
        self.gain = gain
        self.bus.write_byte_data(
                    SENSOR_ADDRESS,
                    COMMAND_BIT | REGISTER_CONTROL,
                    self.integration_time | self.gain
                    )
        self.disable()

    def calculate_lux(self, full, ir):
        if (full == 0xFFFF) | (ir == 0xFFFF):
            return 0
            
        case_integ = {
            INTEGRATIONTIME_100MS: 100.,
            INTEGRATIONTIME_200MS: 200.,
            INTEGRATIONTIME_300MS: 300.,
            INTEGRATIONTIME_400MS: 400.,
            INTEGRATIONTIME_500MS: 500.,
            INTEGRATIONTIME_600MS: 600.,
            }
        if self.integration_time in case_integ.keys():
            atime = case_integ[self.integration_time]
        else:
            atime = 100.

        case_gain = {
            GAIN_LOW: 1.,
            GAIN_MED: 25.,
            GAIN_HIGH: 428.,
            GAIN_MAX: 9876.,
            }

        if self.gain in case_gain.keys():
            again = case_gain[self.gain]
        else:
            again = 1.

        cpl = (atime * again) / LUX_DF
        lux1 = (full - (LUX_COEFB * ir)) / cpl

        lux2 = ((LUX_COEFC * full) - (LUX_COEFD * ir)) / cpl

        return max([lux1, lux2])

    def enable(self):
        self.bus.write_byte_data(
                    SENSOR_ADDRESS,
                    COMMAND_BIT | REGISTER_ENABLE,
                    ENABLE_POWERON | ENABLE_AEN | ENABLE_AIEN
                    )

    def disable(self):
        self.bus.write_byte_data(
                    SENSOR_ADDRESS,
                    COMMAND_BIT | REGISTER_ENABLE,
                    ENABLE_POWEROFF
                    )

    def get_full_luminosity(self):
        self.enable()
        sleep(0.120*self.integration_time+1)
        #time.sleep(0.120*self.integration_time+1)
        full = self.bus.read_word_data(
                    SENSOR_ADDRESS, COMMAND_BIT | REGISTER_CHAN0_LOW
                    )
        ir = self.bus.read_word_data(
                    SENSOR_ADDRESS, COMMAND_BIT | REGISTER_CHAN1_LOW
                    )                    
        self.disable()
        return full, ir

    def get_luminosity(self, channel):
        full, ir = self.get_full_luminosity()
        if channel == FULLSPECTRUM:
            return full
        elif channel == INFRARED:
            return ir
        elif channel == VISIBLE:
            return full - ir
        else:
            return 0

    def sample(self):
        full, ir = self.get_full_luminosity()
        return self.calculate_lux(full, ir)

# tsl2561 lux sensor interface
_COMMAND_BIT = const(0x80)
_WORD_BIT = const(0x20)

_REGISTER_CONTROL = const(0x00)
_REGISTER_TIMING = const(0x01)
_REGISTER_THRESHHOLD_MIN = const(0x02)
_REGISTER_THRESHHOLD_MAX = const(0x04)
_REGISTER_INTERRUPT = const(0x06)
_REGISTER_ID = const(0x0A)
_REGISTER_CHANNEL0 = const(0x0C)
_REGISTER_CHANNEL1 = const(0x0E)

_CONTROL_POWERON = const(0x03)
_CONTROL_POWEROFF = const(0x00)

_INTERRUPT_NONE = const(0x00)
_INTERRUPT_LEVEL = const(0x10)

_INTEGRATION_TIME = {
#  time     hex     wait    clip    min     max     scale
    13:     (0x00,  15,     4900,   100,    4850,   0x7517),
    101:    (0x01,  120,    37000,  200,    36000,  0x0FE7),
    402:    (0x02,  450,    65000,  500,    63000,  1 << 10),
    0:      (0x03,  0,      0,      0,      0,      0),
}


class TSL2561:
    _LUX_SCALE = (
    #       K       B       M
        (0x0040, 0x01f2, 0x01be),
        (0x0080, 0x0214, 0x02d1),
        (0x00c0, 0x023f, 0x037b),
        (0x0100, 0x0270, 0x03fe),
        (0x0138, 0x016f, 0x01fc),
        (0x019a, 0x00d2, 0x00fb),
        (0x029a, 0x0018, 0x0012),
    )

    def __init__(self, i2c, address=0x39):
        self.i2c = i2c
        self.address = address
        sensor_id = self.sensor_id()
        if not sensor_id & 0x10:
            raise RuntimeError("bad sensor id 0x{:x}".format(sensor_id))
        self._active = False
        self._gain = 1
        self._integration_time = 13
        self._update_gain_and_time()

    def _register16(self, register, value=None):
        register |= _COMMAND_BIT | _WORD_BIT
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return unpack('<H', data)[0]
        data = pack('<H', value)
        self.i2c.writeto_mem(self.address, register, data)

    def _register8(self, register, value=None):
        register |= _COMMAND_BIT
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        data = pack('<B', value)
        self.i2c.writeto_mem(self.address, register, data)

    def active(self, value=None):
        if value is None:
            return self._active
        value = bool(value)
        if value != self._active:
            self._active = value
            self._register8(_REGISTER_CONTROL,
                _CONTROL_POWERON if value else _CONTROL_POWEROFF)

    def gain(self, value=None):
        if value is None:
            return self._gain
        if value not in (1, 16):
            raise ValueError("gain must be either 1x or 16x")
        self._gain = value
        self._update_gain_and_time()

    def integration_time(self, value=None):
        if value is None:
            return self._integration_time
        if value not in _INTEGRATION_TIME:
            raise ValueError("integration time must be 0, 13ms, 101ms or 402ms")
        self._integration_time = value
        self._update_gain_and_time()

    def _update_gain_and_time(self):
        was_active = self.active()
        self.active(True)
        self._register8(_REGISTER_TIMING,
            _INTEGRATION_TIME[self._integration_time][0] |
            {1: 0x00, 16: 0x10}[self._gain]);
        self.active(was_active)

    def sensor_id(self):
        return self._register8(_REGISTER_ID)

    def _read(self):
        was_active = self.active()
        self.active(True)
        if not was_active:
            # if the sensor was off, wait for measurement
            sleep_ms(_INTEGRATION_TIME[self._integration_time][1])
        broadband = self._register16(_REGISTER_CHANNEL0)
        ir = self._register16(_REGISTER_CHANNEL1)
        self.active(was_active)
        return broadband, ir

    def _lux(self, channels):
        if self._integration_time == 0:
            raise ValueError(
                "can't calculate lux with manual integration time")
        broadband, ir = channels
        clip = _INTEGRATION_TIME[self._integration_time][2]
        if broadband > clip or ir > clip:
            raise ValueError("sensor saturated")
        scale = _INTEGRATION_TIME[self._integration_time][5] / self._gain
        channel0 = (broadband * scale) / 1024
        channel1 = (ir * scale) / 1024
        ratio = (((channel1 * 1024) / channel0 if channel0 else 0) + 1) / 2
        for k, b, m in self._LUX_SCALE:
            if ratio <= k:
                break
        else:
            b = 0
            m = 0
        return (max(0, channel0 * b - channel1 * m) + 8192) / 16384

    def read(self, autogain=False, raw=False):
        broadband, ir = self._read()
        if autogain:
            if self._integration_time == 0:
                raise ValueError(
                    "can't do autogain with manual integration time")
            new_gain = self._gain
            if broadband < _INTEGRATION_TIME[self._integration_time][3]:
                new_gain = 16
            elif broadband > _INTEGRATION_TIME[self._integration_time][4]:
                new_gain = 1
            if new_gain != self._gain:
                self.gain(new_gain)
                broadband, ir = self._read()
        if raw:
            return broadband, ir
        return self._lux((broadband, ir))

    def threshold(self, cycles=None, min_value=None, max_value=None):
        if min_value is None and max_value is None and cycles is None:
            min_value = self._register16(_REGISTER_THRESHHOLD_MIN)
            max_value = self._register16(_REGISTER_THRESHHOLD_MAX)
            cycles = self._register8(_REGISTER_INTERRUPT)
            if not cycles & _INTERRUPT_LEVEL:
                cycles = -1
            else:
                cycles &= 0x0f
            return cycles, min_value, max_value
        was_active = self.active()
        self.active(True)
        if min_value is not None:
            self._register16(_REGISTER_THRESHHOLD_MIN, int(min_value))
        if max_value is not None:
            self._register16(_REGISTER_THRESHHOLD_MAX, int(max_value))
        if cycles is not None:
            if cycles == -1:
                self._register8(_REGISTER_INTERRUPT, _INTERRUPT_NONE)
            else:
                self._register8(_REGISTER_INTERRUPT,
                    min(15, max(0, int(cycles))) | _INTERRUPT_LEVEL)
        self.active(was_active)

    def interrupt(self, value):
        if value or value is None:
            raise ValueError("can only clear the interrupt")
        self.i2c.writeto(self.address, b'\x40')


# Those packages are identical.
TSL2561T = TSL2561
TSL2561FN = TSL2561
TSL2561CL = TSL2561


class TSL2561CS(TSL2561):
    # This package has different lux scale.
    _LUX_SCALE = (
    #       K       B       M
        (0x0043, 0x0204, 0x01ad),
        (0x0085, 0x0228, 0x02c1),
        (0x00c8, 0x0253, 0x0363),
        (0x010a, 0x0282, 0x03df),
        (0x014d, 0x0177, 0x01dd),
        (0x019a, 0x0101, 0x0127),
        (0x029a, 0x0037, 0x002b),
    )


class tsl25x1_sensor:

    def __init__(self,sensor_type=None,i2c=None):
        self.type=None
        if sensor_type==None or sensor_type=='tsl2591' or sensor_type=='TSL2591':
            try:
                self.sensor = Tsl2591(i2c=i2c)  # initialize tsl2591 sensor
                self.type='tsl2591'
                print('tsl2591 sensor initialized')
            except:
                pass
        if self.type==None or sensor_type=='tsl2561' or sensor_type=='TSL2561':
            try:
                self.sensor = TSL2561(i2c)
                self.type='tsl2561'
                print('tsl2561 sensor initialized')
            except:
                pass

    def light(self):
        if self.type=='tsl2591':
            full, ir = self.sensor.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
            lux = self.sensor.calculate_lux(full, ir)  # convert raw values to lux
            #print('tsl2591 full, ir, lux:', full, ir, lux)
            return full, ir, lux
        elif self.type=='tsl2561':
            full, ir = self.sensor.read(raw=True)
            lux=self.sensor._lux((full,ir))
            #print('tsl2561 full, ir, lux:', full, ir, lux)
            return full, ir, lux

    
