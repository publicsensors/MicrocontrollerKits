#  Definitions of platform-specific pins and commands.
#
#  Currently supported boards are: STM32f405 Feather, ESP8266 Huzzah Feather/Breakout Board, Pyboard v1.1

# Detect platform via uos command
from uos import uname
sys_info = uname()
print(sys_info)
platform=sys_info[4]


if platform.find('Feather STM32F405 with STM32F405RG')>-1:  # Board-specific definitions: STM32f405 Feather
    print('Platform is STM32 Feather')
    from SetUp.FeatherSTM32F405_defs import *

elif platform.find('ESP module with ESP8266')>-1:  # Board-specific definitions: ESP8266 Huzzah Feather/Breakout Board
    print('Platform is ESP8266')
    from SetUp.FeatherESP8266_defs import *

elif platform.find('PYBv1.1 with STM32F405RG')>-1:  # Board-specific definitions: Pyboard v1.1
    print('Platform is PYBv1.1')
    from SetUp.PYB_defs import *

elif platform.find('ESP32 module with ESP32')>-1:  # Board-specific definitions: ESP32 Feather
    print('Platform is ESP32')
    from SetUp.FeatherESP32_defs import *


'''
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13-53-gc20075929-dirty on 2020-09-21', machine='Adafruit Feather STM32F405 with STM32F405RG')
(sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.9.4-701-g10bddc5c2 on 2019-01-17', machine='ESP module with ESP8266')
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13 on 2020-09-02', machine='PYBv1.1 with STM32F405RG')
(sysname='esp32', nodename='esp32', release='1.17.0', version='v1.17 on 2021-09-02', machine='ESP32 module with ESP32')
'''
