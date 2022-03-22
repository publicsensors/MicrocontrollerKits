# Sensors
This directory contains [MicroPython](https://micropython.org/)-based code for [PublicSensors](https://www.publicsensors.org) environmental sensor microcontroller kits.
This software is used for beginner and intermediate activities.
Activities and circuit layouts for microcontrollers and sensors using these codes are documented on the PublicSensors website.

The code in this directory will operate for the following types of microcontrollers running Micropython:
- [**Adafruit Feather STM32F405**](https://www.adafruit.com/product/4382), which is used for all sensor kit activites on [PublicSensors](https://www.publicsensors.org)
- **ESP32-based microcontrollers** (with some limitations, but with WiFi -- see below)
  - [Feather HUZZAH](https://www.adafruit.com/product/2821)
- **ESP8266-based microcontrollers** (with substantial limitations -- see below)
<!--   - [HUZZAH Breakout](https://www.adafruit.com/product/2471) -->
  - [Feather HUZZAH](https://www.adafruit.com/product/2821)
- [**MicroPython pyboard v1.1**](https://www.adafruit.com/product/2390)

The software and circuit layouts are designed to accommodate "drop-in" swapping between listed microcontroller types with Adafruit's Feather form factor, without changing the circuit layout.
Pin definitions, UART initialization and other platform-specific selections are specified via calls from the Python script `platform_defs.py` in the `SetUp` directory.
The code automatically detects the microcontroller type, and imports the corresponding definitions.



To use this code, make sure your microcontroller is running MicroPython version 1.18 or later.
MicroPython firmware is a [free download](https://micropython.org/download/) from the MicroPython website, or from the PublicSensors [Microcontroller Setup page](https://github.com/publicsensors/MicrocontrollerKits/tree/main/MicrocontrollerSetup).

Then, download or clone a copy of the [MicrocontrollerKits](https://github.com/publicsensors/MicrocontrollerKits) repository onto your local machine.

If your microcontroller supports reading and writing files from a microSD card (Adafruit Feather STM32F405, pyboard, microSD reader-equipped ESP32 or ESP8266), copy the **contents** of the Sensor directory (not the folder itself) onto a microSD card.

Otherwise, copy the contents of the Sensor directory onto the microcontroller's flash memory.

The complete code set includes drivers for many types of environmental sensors, organized in separate directories (Temperature, Light, GPS, etc.).
If space is limiting (e.g. on the flash memory of some microcontrollers) you can copy over only the directories for sensors you will be using.
If you want to use an additional sensor later, simply copy over the corresponding driver directory. The driver for that sensor will be available after the next microcontroller reboot.

The **essential** files and directories to run [PublicSensors](https://www.publicsensors.org) activities are:
- `boot.py`
- `main.py`
- the `SetUp` directory
- the `Data` directory
- one or more directories corresponding to the sensors you intend to use (Temperature, Light, etc.)

All data files produced when logging output from environmental sensors are placed into the **Data** subdirectory or folder.
For notes on accessing these files, see below.

## Basic operation of PublicSensors MicrocontrollerKits instruments
[PublicSensors](https://www.publicsensors.org) environmental sensor instruments can run either with or without being attached to a computer:
- In operation without a computer, instruments display sensor data and other output through an attached LCD screen.
- In operation with a computer, the instruments can be operated via commands from the computer, and will additionally display sensor data to an LCD if one is attached.

Instruments can operate with specific sensors set in **logging** or **non-logging mode**:
- In logging mode, all samples are both displayed via the LCD and/or computer interface and logged to a timestamped data file in the Data directory.
- In non-logging mode, samples are displayed but a data file is not created.

Instruments can be set to sample only when a button is pressed, or to automatically sample at regular intervals (and also when the sampling button is pressed).

**Logging/non-logging, looping/non-looping and other behaviors are determined by parameters in the file `user_params.py` in the SetUp directory, along with two optional buttons for triggering an individual sample and toggling between looping and non-looping.**

Communicating with a PublicSensors microcontroller requires a serial communication program running on a desktop or laptop.
Good tools for this include (depending on the type of microcontroller):
- [thonny](https://thonny.org/)
- [BeagleTerm](https://chrome.google.com/webstore/detail/beagle-term/gkdofhllgfohlddimiiildbgoggdpoea) (via the Chrome browser)
- [rshell](https://github.com/dhylands/rshell)
- [mpfshell](https://github.com/wendlers/mpfshell)
- [WebREPL](https://github.com/micropython/webrepl)

The PublicSensors MicrocontrollerKits code is designed to start automatically when the microcontroller boots up.
The initialization process produces some output through the LCD, if one is attached, with additional information provided through the computer interface.

**Note: After boot-up, a computer interface (if one is attached) will show the standard MicroPython REPL prompt, ">>>".
The sampling process, either triggered by button presses or automatic sampling at intervals, is still operating.**

The PublicSensors MicrocontrollerKits code is designed to be non-blocking, which means that it runs essentially in the background.
This is to enable a user to do other tasks during sampling, such as setting the onboard Real Time Clock, copying or transferring files, etc.

### Stopping automatic sampling at intervals
Sampling operations are executed by `sampler`, which is an instance of the Sampler class object defined in the Python script `sensor_utils.py` (in the `SetUp` directory).

When the instrument is set to automatically sample at intervals (see below), sampling can be **terminated** by invoking the `stop()` method,
```python
>>>sampler.stop()
```
This will halt the current series of environmental samples.
To start a new set of samples (with a new set of data files, if they are being recorded), reboot the microcontroller with `ctrl-d` from a computer interface, or press the `RST` button on the microcontroller.

If a looping static switch is present, sampling can be **paused** by moving that switch to the `off` position.
Pressing the sampling button, or moving the looping static switch to the `on` position, will **resume** sampling (using the already-existing data files if they are being recorded).

## Setting up sampling parameters
The settings that users most frequently want to modify are specified in the form of a dictionary, called `params`, in `user_params.py` in the `SetUp` directory:
```python
# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets user-specified parameters. Default parameters are set in default_params.py.
#
params={'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':0,
                       'UIV':1,
                       'color':1,
                       'GPS':0,
                       'AQI':0,
                       'voltage':1,
                       'pressure':1,
                       'exttime':1},
        'sensor_log_flags':{ 'distance':1,
                       'temperature':1,
                            'light':1,
                            'UIV':1,
                            'color':1,
                             'GPS':1,
                             'AQI':1,
                             'voltage':1,
                             'pressure':1,
                             'exttime':1},
        'auto_logging':True,
        'default_sample_looping':True,
        'sample_max':4,
        'sample_interval':60,
        'display_interval':3,
        'verbosity':14
}
```
The interpretation of these entries is:
- `sensor_list`:

1 indicates sampling is requested (e.g., `'temperature':1`); 0 indicates sampling is not requested (e.g. 'light':0).

At boot-up, each requested sensor will be tested; if functional, it will be added to the sampling schedule and its results displayed and logged.
If a sensor is requested but not present and functional, then it will be left off the sampling schedule.

This means there is generally no harm in leaving sensors set to 1 in the `sensor_list`, even if they are not present. However, there are two situations in which it may be undesirable to set sensors to 1 when they are not being used.

One is when there is a conflict in I2C addressing. For example, the Light sensor and the Color sensor use the same I2C address, so that only one may be used on a given I2C bus.
It is best to avoid attempting to query incompatible sensors (even though the initialization testing process at boot-up may handle it gracefully).

The other is when testing a sensor requires significant amount of time, e.g. an Air Quality Index sensor that must run its fan for 30 seconds to a minute before a valid sample can be obtained.
This can slow down testing during boot-up to an annoying extent.

- `sensor_log_flags`:

1 indicates data should be logged to a data file (if the sensor is queried); 0 indicated data should not be logged. In general, there is little reason not to record data files, so leaving these as 1 is usually fine.

- `auto_logging`:

This is a switch to easily turn logging on and off: `True` means data will automatically be logged for sensors flagged in `sensor_log_flags`; `False` turns off all data file logging.

- 'default_sample_looping':

Determines initial sampling behavior at boot-up: `True` means looping will automatically be started, so that samples are taken at intervals. `False` means that sample looping will not be automatically started.

This initial behavior can be over-ridden (after boot-up) by changing the position of the looping static switch, if there is one.

- `sample_max`:

Not currently used.

- `sample_interval`:

This is the time interval, in seconds, at which samples will be obtained during sample looping.

This should be longer than the longest sensor reading, which is usually an issue only for a few specific sensors (like Air Quality Index) for which each reading takes a significant amount of time.

- `display_interval`:

In sampling, queries to each requested sensor are done in rapid succession to make data as nearly contemporaneous as possible.

To make the LCD display readable, data are presented sequentially, with each sensor's output remaining on the LCD for the number of seconds specified in `display_interval`

- `verbosity`

This parameter regulates a simple verbosity scheme, implemented in `SetUp/verbosity.py`. In calls to the function `vrb_print`, output is printed to a computer interface if the associated `vrb_level` is less than or equal to the verbosity parameter.
The default level of `vrb_level` is 10, if it is not otherwise specified in the call to `vrb_print`.

Additional settings (ones that typical users rarely need to change) are specified in in `default_params.py` in the `SetUp` directory.

## Sensor drivers
PublicSensors code is designed to make it easy to add or modify drivers for environmental sensors.
Code for each distinct type of sensor is in an informatively named directory.
For example, sampling with TSL25X1 light sensors is executed using code in the `Light` directory; sampling with acoustic distance sensors uses code in the `Acoustic` directory, etc.

Sampling for each sensor type is accomplished using an object defined in a short, informatively named module.
These modules have stereotyped naming conventions and internal structures.

For example, light level samples are handled by `read_light` objects defined in `Light/read_light.py`; pressure samples from BME280 or BMP280 sensors are handled by `read_press` objects defined in `read_press.py`, etc.

The `read_X` classes each have:
- a `test_X` method (`test_light`, `test_press`, etc.) which is used to assess at boot-up whether a sensor is present and functioning; and
- a `print_X` method (`print_light`, `print_press`, etc.) which obtains sensor readings during regular sampling, and stages it for LCD display and logging.

Most parameters for sensor operations are specified in `SetUp/default_params`, including directory names, variables and formats for output, log file headers, etc.

The easiest way to add additional sensors is to copy an existing sensor directory, adding required low-level drivers, modifying the variable names and formats as necessary, and adding the corresponding entries in the `params` dictionary in `user_params.py` and `default_params.py`.

## Data log file formats
Data log files from PublicSensors instruments appear in the `Data` directory (a parameter that can be changed in `default_params.py`).

For each sample, the corresponding data files are opened, a new data line appended, then the file is immediately closed.
This means that, almost always, data files can be copied or downloaded intact even while the sampling loop is ongoing.

Log files have the following standardized naming convention (e.g. `2022-03-21T17-25-32_10_temp.csv`) to facilitate tracking large datasets and automated processing:
- A timestamp (`2022-03-21T17-25-32`), with format specified in `default_params.py`, reflecting the creation time of the file;
- An index number (`_10_`), reflecting the number of files in the `Data` directory at initialization.
The index number prevents data log files from being overwritten if the Real Time Clock is not set (which results in duplicate timestamps).
- An indicator of the sensor being logged (`temp`).
- A `.csv` suffix.

The contents of PublicSensors data log files have stereotyped formats similar to:
```python
SampleNum,Time,ROM_ID,Temp
1,2022-03-21 17:25:34,28543a6d09000056,21.250000
1,2022-03-21 17:25:34,28ae4815060000ee,20.625000
2,2022-03-21 17:26:34,28543a6d09000056,21.187501
2,2022-03-21 17:26:34,28ae4815060000ee,20.562501
3,2022-03-21 17:27:34,28543a6d09000056,21.187501
3,2022-03-21 17:27:34,28ae4815060000ee,20.437500
4,2022-03-21 17:28:34,28543a6d09000056,21.187501
4,2022-03-21 17:28:34,28ae4815060000ee,20.500000
5,2022-03-21 17:29:34,28543a6d09000056,21.250000
5,2022-03-21 17:29:34,28ae4815060000ee,20.500000
6,2022-03-21 17:30:34,28543a6d09000056,21.250000
6,2022-03-21 17:30:34,28ae4815060000ee,20.500000
7,2022-03-21 17:31:34,28543a6d09000056,21.250000
7,2022-03-21 17:31:34,28ae4815060000ee,20.500000
8,2022-03-21 17:32:34,28543a6d09000056,21.250000
8,2022-03-21 17:32:34,28ae4815060000ee,20.500000
9,2022-03-21 17:33:34,28543a6d09000056,21.250000
9,2022-03-21 17:33:34,28ae4815060000ee,20.437500
10,2022-03-21 17:34:34,28543a6d09000056,21.250000
10,2022-03-21 17:34:34,28ae4815060000ee,20.437500
11,2022-03-21 17:35:34,28543a6d09000056,21.250000
11,2022-03-21 17:35:34,28ae4815060000ee,20.437500
12,2022-03-21 17:36:34,28543a6d09000056,21.250000
12,2022-03-21 17:36:34,28ae4815060000ee,20.437500
13,2022-03-21 17:37:34,28543a6d09000056,21.312501
13,2022-03-21 17:37:34,28ae4815060000ee,20.375001
14,2022-03-21 17:38:34,28543a6d09000056,21.312501
14,2022-03-21 17:38:34,28ae4815060000ee,20.437500
15,2022-03-21 17:39:34,28543a6d09000056,21.437500
15,2022-03-21 17:39:34,28ae4815060000ee,20.500000
16,2022-03-21 17:40:34,28543a6d09000056,21.500001
16,2022-03-21 17:40:34,28ae4815060000ee,20.562501
```
In these files, the header entries and the formats for environmental variables are parameters dictionaries defined in `default_params.py`, and can be modified without changing the underlying code set.
For this example, those entries are, respectively:
```python
'temperature':{'T':'Temp','sensor_id':'ROM_ID'},
```
and
```python
'temperature':{'T':'%f','sensor_id':'%s'}
```
This example, using `DS18B20` temperature sensors, illustrates special case:
Two sensors are connected, and readings from each are logged in separate lines.

Data columns are:
- the sample number, within the current sampling series;
- the timestamp corresponding to the sample;
- the unique ROM ID of the `DS18B20` sensor;
- the recorded temperature value

Another special case is illustrated in data from an acoustic distance sensor:
```python
SampleNum,Time,Dist
1,2022-03-21 17:25:33,21.400001
2,2022-03-21 17:26:33,21.400001
3,2022-03-21 17:27:33,21.400001
4,2022-03-21 17:28:33,24.800000
5,2022-03-21 17:29:33,-0.100000
6,2022-03-21 17:30:33,-0.100000
7,2022-03-21 17:31:33,-0.100000
8,2022-03-21 17:32:33,121.599996
9,2022-03-21 17:33:33,101.199996
10,2022-03-21 17:34:33,25.200002
11,2022-03-21 17:35:33,-0.100000
12,2022-03-21 17:36:33,-0.100000
13,2022-03-21 17:37:33,25.600002
14,2022-03-21 17:38:33,18.600000
15,2022-03-21 17:39:33,-0.100000
16,2022-03-21 17:40:33,-0.100000
```
In this example, the distance (rightmost column) is specified in the driver to be `-0.1` if the sensor reading has failed (e.g. because the target is less than the minimum distance from the sensor).

**Data file formats are designed such that data can be plotted simply by opening the `.csv` file in a spreadsheet, selecting the data series columns corresponding to timestamps and measurements, and creating an XY chart.**

Data file formats are designed to make it straightforward to isolate specific sensors or exclude invalid data using basic spreadsheet functions (e.g. the temperature and distance timeseries examples above).
