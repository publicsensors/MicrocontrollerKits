#  Definitions of platform-specific pins and commands.
#
#  Currently supported boards are: STM32f405 Feather, ESP8266 Huzzah Feather/Breakout Board, Pyboard v1.1

# Detect platform via uos command
from uos import uname
sys_info = uname()
print(sys_info)
platform=sys_info[4]


if platform.find('Feather STM32F405 with STM32F405RG')>-1:  # Board-specific definitions: STM32f405 Feather

    print('Loading definitions for STM32 Feather')
    from machine import Pin, UART

    board='STM32feather'
    p_pwr1 = Pin('D9', Pin.OUT,value=1)  # Pin 12 is power supplied to the DS18B20, V+
    p_DS18B20 = Pin('D10', Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
    uartGPS = UART(6, 9600)
    #uartAQ= UART(3, 9600)
    #uartAQ.init(9600, bits=8, parity=None, stop=1)
    uartAQ= UART(3, 9600, bits=8, parity=None, stop=1)
    button = Pin('D13', Pin.IN, Pin.PULL_UP)
    # Define default I2C pins
    p_I2Cscl_lbl='SCL'
    p_I2Csda_lbl='SDA'
    #pin definitions for hcsr04/jsn sensors
    p_hcsr_trig = 'D12'
    p_hcsr_echo = 'D11'
    #pin definitions to automatically enable sampling loop (0=loop, 1= wait for button press)
    # the labeling above seems to be backwards -- should be 1=loop, 0=wait for button press)
    p_smpl_loop_lbl='MISO'
    #p_smpl_trigger_lbl='SCK'
    p_smpl_trigger_lbl='D13'

elif platform.find('ESP module with ESP8266')>-1:  # Board-specific definitions: ESP8266 Huzzah Feather/Breakout Board
    print('Loading definitions for ESP8266')

    from machine import Pin, UART
    from esp import osdebug # stop annoying WiFi messages
    osdebug(None)
    from uos import dupterm
    dupterm(UART(0, 115200), 1) # echo UART to terminal
    # Uncomment to automatically start webrepl
    #import webrepl
    #webrepl.start()
    import gc
    gc.collect()

    board='esp8266'
    p_pwr1 = Pin(13, Pin.OUT)  # Pin 12 is power supplied to the DS18B20, V+
    p_DS18B20 = Pin(12, Pin.IN)  # Pin D10 is the data pin for DS18B20 temperature sensors
    button = Pin(14, Pin.IN, Pin.PULL_UP)
    # Define default I2C pins
    p_I2Cscl_lbl=5
    p_I2Csda_lbl=4
    #pin definitions for hcsr04/jsn sensors
    p_hcsr_trig = 12
    p_hcsr_echo = 14
    

elif platform.find('PYBv1.1 with STM32F405RG')>-1:  # Board-specific definitions: Pyboard v1.1

    print('Loading definitions for PYBv1.1')
    from machine import Pin, UART
    from pyb import Switch #, UART

    board='PBDv1.1'
    # Initalize power pins off; they are turned on by read_XXX classes if called
    p_pwr1 = Pin('X19', Pin.OUT,value=1)  # Pin X19 is power supplied to the DS18B20, V+
    p_pwr2 = Pin('X18', Pin.OUT,value=0)  # Pin X18 is power supplied to the GPS, V+
    p_pwr3 = Pin('X3', Pin.OUT,value=0)  # Pin X3 is power supplied to the GPS, V+
    p_pwr4 = Pin('X4', Pin.OUT,value=0)  # Pin X4 is power supplied to the GPS, V+
    p_DS18B20 = Pin('X20', Pin.IN)  # Pin X20 is the data pin for DS18B20 temperature sensors
    uartGPS= UART(4, 9600)
    uartAQ= UART(3, 9600)
    uartAQ.init(9600, bits=8, parity=None, stop=1)
    button = Switch()  # use onboard USR button
    #p_batt=14
    #p_sens=4
    # Define default I2C pins
    p_I2Cscl_lbl='X9'
    p_I2Csda_lbl='X10'
    #pin definitions for hcsr04/jsn sensors
    p_hcsr_trig = 'D12'
    p_hcsr_echo = 'D11'
    #pin definitions to automatically enable sampling loop (0=loop, 1= wait for button press)
    p_smpl_loop_lbl='Y4'
    p_smpl_trigger_lbl='Y3'


'''
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13-53-gc20075929-dirty on 2020-09-21', machine='Adafruit Feather STM32F405 with STM32F405RG')
(sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.9.4-701-g10bddc5c2 on 2019-01-17', machine='ESP module with ESP8266')
(sysname='pyboard', nodename='pyboard', release='1.13.0', version='v1.13 on 2020-09-02', machine='PYBv1.1 with STM32F405RG')
'''
