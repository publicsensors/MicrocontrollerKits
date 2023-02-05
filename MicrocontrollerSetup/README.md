# Microcontroller Setup

The code for this repository is based on the use of the [Feather STM32](https://www.adafruit.com/product/4382) microcontroller. The following are additional resources for working with these microcontrollers:
- [Pin Identifiers](https://github.com/micropython/micropython/blob/master/ports/stm32/boards/ADAFRUIT_F405_EXPRESS/pins.csv)
- [Using the STM32 with Micropython](https://learn.adafruit.com/adafruit-stm32f405-feather-express/micropython-setup)

All of the code for the activites uses MicroPython v1.13, available directly from [MicroPython.org](https://micropython.org/download/) and provided here as `firmware.dfu`. Instructions are provided for installing using a [DFU bootloader](https://learn.adafruit.com/adafruit-stm32f405-feather-express/dfu-bootloader-details), either using a GUI (such as [STM32CubeProg](https://www.st.com/en/development-tools/stm32cubeprog.html)) or command line ([dfu-util](http://dfu-util.sourceforge.net/)) available for Windows, Mac, and Linux.

To use dfu-util:
1. Download [dfu-util](http://dfu-util.sourceforge.net/) from sourceforge.
2. Connect your microcontroller to your computer via USB in bootloader mode. For the Feather STM32, this involves connecting the **B0** pin to either of the **3.3V** pins, then connecting to your computer via USB.
3. In a terminal/command window, navigate to the dfu-util directory.`
4. You can confirm that your microcontroller is detected by dfu-util using
```
dfu-util -l
```
5. To update the firmware on the microcontroller, you can use the following syntax (note, `firmware.dfu` should be the complete path of the file):
```
dfu-util -a 0 -D firmware.dfu
```

# Using precompiled mpy-files 

When a `.py` file is loaded, it must be compiled before it can be executed.
This compilation step requires significant amounts of microcontroller heap space, beyond the heap space required to execute the code.
On microcontrollers with limited heap space, memory errors are often encountered during compilation, even though the compiled code would fit within the available heap space.

mpy-files are a precompiled form of Python code.
Because an mpy-file is precompiled, loading it avoids using heap space for compilation.
Therefore, loading an mpy-file requires significantly less heap space than loading its `.py` file precursor.

On PublicSensors instruments, using mpy-files means a larger array of sensors can be used simultaneously within available heap space constraints compared with using the original Python files.

Against this advantage, mpy-files have two disadvantages:
- mpy-files are not easily readable and cannot be edited
- MicroPython automatically loads the files `boot.py` and `main.py` when the microcontroller is rebooted; however, the corresponding mpy-files `boot.mpy` and `main.mpy` are **not** automatically loaded.

In light of these advantages and disadvantages, the recommended configuration for PublicSensors instruments is to use a code base fully compiled into mpy-files with the exception of three files:
- `boot.py` and `main.py`, which are kept as Python scripts so they will be automatically loaded at boot time; and,
- `user_params.py`, which is kept as a Python script so that user-specified parameter settings can be easily read and edited.

#### Downloading a precompiled (mpy-file) version of PublicSensors code
Precompiled code can be downloaded from the PublicSensors website as a [zip achive](https://www.publicsensors.org/mpySensors.zip) or a [tar archive](https://www.publicsensors.org/mpySensors.tar).
Individual files can be selected for download from the indexed directory at [https://www.publicsensors.org/mpySensors/](https://www.publicsensors.org/mpySensors/).

#### Creating an mpy-file directory tree

Compiling Python scripts into mpy-files requires the MicroPython utility `mpy-cross`, available from the [MicroPython github repository](https://github.com/micropython/micropython/tree/master/mpy-cross).
`mpy-cross` is part of the `unix` port of MicroPython; see the corresponding pages for detailed instructions on installation.
It is typically installed with a path `micropython/mpy-cross/mpy-cross`, where `micropython` is the base directory for the MicroPython directory cloned from github.

For conciseness and clarity, it is recommended that an alias or symbolic link be created in the MicrocontrollerKits directory to the working copy of `mpy-cross`, e.g. with
```
ln -s ~/micropython/mpy-cross/mpy-cross
```
where `~` refers to the home directory of the user and the path is 'micropython/mpy-cross/mpy-cross'.

The utility `compile_tree.py` in the `mpy_tree` module transcribes a source directory tree into a corresponding output directory tree with Python scripts compiled into equivalent mpy-files. 
For example, in a Python session launched from the `MicrocontrollerKits` directory:
```
>>> from MicrocontrollerSetup.mpy_tree import compile_tree
compile_tree(mpy_cross='micropython/mpy-cross/mpy-cross')
```
creates (or updates) a directory of mpy-files called `mpySensors` from the source `Sensors`.

There are several optional arguments for the `compile_tree` function:
- src_dir: The source directory to be transcribed (default: 'Sensors')
- dest_dir: The destination directory for the compiled directory tree (default: 'mpySensors')
- copy_files: a list of files to be copied in original form, without being compiled (default: ['boot.py','main.py','user_params.py'])
- skip_files: a list of files to be ignored, e.g. work or temporary files (default: [])
- mpy_cross: a path to the `mpy-cross` utility, if an alias or symbolic link is not created in the `MicrocontrollerKits` directory (default: './mpy-cross')
- replace_dest: a flag specifying whether existing files should be replaced (True) or skipped (False) (default: True)

