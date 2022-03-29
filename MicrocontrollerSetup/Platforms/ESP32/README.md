Copy onto the `/` directory of flash on the ESP32 running MicroPython v1.18 or later, with the filename `boot.py` (that is, replace the pre-existing `boot.py` with this file).

On boot-up, the microcontroller will mount an SD card (sck=Pin(5), mosi=Pin(18), miso=Pin(19), cs = Pin(21)) if it is present.

`main.py` will then be loaded from the SD card, imitating the behavior of STM32 boards such as the pyboard and STM32F405 Feather. Data log files will also be directed to the `/sd/Data` directory.
