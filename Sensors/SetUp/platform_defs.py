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
    from Setup.FeatherSTM32F405_defs import *

elif platform.find('ESP module with ESP8266')>-1:  # Board-specific definitions: ESP8266 Huzzah Feather/Breakout Board
    print('Platform is ESP8266')
    from Setup.FeatherESP8266_defs import *

elif platform.find('PYBv1.1 with STM32F405RG')>-1:  # Board-specific definitions: Pyboard v1.1

    print('Platform is PYBv1.1')
    from Setup.PYB_defs import *



'''
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13-53-gc20075929-dirty on 2020-09-21', machine='Adafruit Feather STM32F405 with STM32F405RG')
(sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.9.4-701-g10bddc5c2 on 2019-01-17', machine='ESP module with ESP8266')
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13 on 2020-09-02', machine='PYBv1.1 with STM32F405RG')
'''
