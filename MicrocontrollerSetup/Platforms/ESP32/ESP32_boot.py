# This file is executed on every boot (including wake-boot from deepsleep)

# If sd card is mounted, change directories to read and write files there:
try:
    from SetUp.sdcard import SDCard
    from machine import SoftSPI, Pin
    spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(5), mosi=Pin(18), miso=Pin(19))
    sd = SDCard(spi, Pin(21))
    from os import mount,listdir,chdir,getcwd
    mount(sd, '/sd')
    #from sys import path
    #path.insert(0,'/sd')
    print(getcwd())
    print(listdir())
    chdir('/sd')
    print('SD card mounted -- using /sd as base directory...')
    print(getcwd())
    print(listdir())
except:
    print('No SD card mounted -- using / as base directory...')

