#  Definitions of platform-specific pins and commands.
#
#  Currently supported boards are: STM32f405 Feather, ESP32 Huzzah Feather, Pyboard v1.1

# Detect platform via uos command
from uos import uname
sys_info = uname()
print(sys_info)
platform=sys_info[4]

# Default values (may be altered for specific platforms)
uartBT = False # This is the uart for HC05 bluetooth module, by default off

# Platform-specific definitions
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


