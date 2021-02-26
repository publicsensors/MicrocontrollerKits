# Utility functions for PublicSensors/SensoresPublicos sensor activities

from SetUp.platform_defs import *
#global params

from sys import print_exception
#from machine import I2C
from time import sleep
#from esp8266_i2c_lcd import I2cLcd

def sample_params(user_param_file=None,default_param_file='SetUp.default_params.py',pars={}):
    """ A function to load default and user-specified parameters for the sample cycle.
        pars is a dictionary containing settings to be entered into the global params dictionary.
        If pars is not passed, it is created from the settings in default_param file.
        It is then modified by settings in the user_param_file, then returned
    """
    if len(pars)==0:
        print('loading default parameters from the default_param_file')
        module_name = default_param_file[:-3]
        print('importing ',module_name)
        def_pars=__import__(module_name)
        print(dir(def_pars.default_params))
        pars.update(def_pars.default_params.params)
    print('Default parameters:')
    print(pars)
    if user_param_file is None:
        user_param_file=pars['user_param_file']
        print('loading user-specfied parameters from '+user_param_file+' in subdirectory ',pars['setup_dir'])
    try:
        module_name = '%s.%s' % (pars['setup_dir'],user_param_file[:-3])
        print('importing ',module_name)
        user_pars=__import__(module_name)
        print(dir(user_pars.user_params))
        pars.update(user_pars.user_params.params)
    except Exception as e:
        print_exception(e)
        print('Unable to import user-specified parameter file')
    print('Final parameters:')
    print(pars)
    # return a local copy of the parameters, to be assigned to the global params if appropriate
    return pars

def sensor_select(i2c,lcd,pars):
    """A function to detect, initialize and test alternative sensors for 
       PublicSensors/SensoresPublicos activities 
    """
    global sensor # use a global variable to fix global vs. local namespace issues

    # recreate the sensor use flags previously in active_sensors.py
    temperature=pars['sensor_list']['temperature']
    light=pars['sensor_list']['light']
    distance=pars['sensor_list']['distance']
    GPS=pars['sensor_list']['GPS']
    
    activeNames, activeFuncs, sensors =  [[] for i in range(3)]  # Lists for when we are going to use multiple sensors
    sensorFuncs = {'light': 'light', 'distance': 'dist', 'temperature': 'temp', 'GPS': 'GPS'}
    sensorDirs = {'light': 'Light', 'distance': 'Acoustic', 'temperature': 'Temperature', 'GPS': 'GPS'}
    #for sensr in ['temperature','light','distance','GPS']: # lets try talking to all the sensors
    for sensr in ['GPS','distance','light','temperature']: # lets try talking to all the sensors
            try:
                activeName = sensr
                activeFunc = sensorFuncs[sensr]
                activeDir = sensorDirs[sensr]
                #print('from .',activeDir+' import read_'+activeFunc)
                #exec('from .',activeDir+' import read_'+activeFunc)
                print('from %s import read_%s' % (activeDir,activeFunc))
                exec('from %s import read_%s' % (activeDir,activeFunc))
                #exec('import read_'+activeFunc)
                sensor = eval('read_'+activeFunc+'.read_'+activeFunc+'()')
                sleep(1)
                print('success: queuing sensor driver ',activeFunc)
                exec('print(sensor.test_'+activeFunc+'())')
                sTest=eval('sensor.test_'+activeFunc+'()')
                exec('sTest = sensor.test_'+activeFunc+'()')
                print('got here 5')
                print(sTest)
                if sTest:
                    activeNames.append(activeName)
                    activeFuncs.append(activeFunc)
                    sensors.append(sensor)
                    print('success: able to make measurement using ',activeFunc)
                else:
                    print('Error: unable to connect to ',activeFunc, ' sensor')
            except Exception as e:
                print_exception(e)
                print('Error: sensor driver ',activeFunc,' was requested but failed to load')

    if True: #asFlag ==1:
        print('activeNames = ',activeNames)
        print('activeFuncs = ',activeFuncs)
        print('sensors = ',sensors)
        #activeList = [s for s in [item for item in dir(active_sensors) if not item.startswith("__")] if eval('active_sensors.'+s) == 1]
        activeList = [s for s in list(pars['sensor_list'].keys()) if pars['sensor_list'][s]==1]
        print('activeList = ',activeList)
        #activeNamesMeasure = [k for k in activeList if k in (activeNames and activeList)] # check which from the active list work
        activeNamesMeasure = [k for k in activeList if ((k in activeNames) and (k in activeList))]
        print('activeNamesMeasure = ',activeNamesMeasure)
        activeIndex = [activeNamesMeasure.index(k) for k in activeNames] # get the index of the active & good sensors
        #activeIndex = [activeNames.index(k) for k in activeNamesMeasure] # get the index of the active & good sensors
        print('activeIndex = ',activeIndex)
        activeFuncs = [activeFuncs[k] for k in activeIndex] # use the index to get the good and active funcs
        print('activeFuncs = ',activeFuncs)
        sensors = [sensors[k] for k in activeIndex] # get the good and active sensor objects
        print('sensors = ',sensors)
    else: # if no active_sensors, use all the sensors found and the original lists as above
        activeNamesMeasure = activeNames
    print('activeNamesMeasure = ',activeNamesMeasure)
    if lcd:
        #i2c = I2C(scl=Pin(p_I2Cscl_lbl),sda=Pin(p_I2Csda_lbl))
        #lcd = I2cLcd(i2c, 0x27,2,16)
        lcd.clear()
        lcd.scrollstr('Found the following sensors: '+', '.join(activeNames))
        lcd.clear()
        lcd.scrollstr('Preparing to measure: '+', '.join(activeNamesMeasure))
        lcd.clear()
        lcd.putstr("Ready!\n"+chr(0)+'Listo!')
    else:
        print('LCD not registered...')
    new_pars={'sensors':sensors,
              'activeFuncs':activeFuncs,
              'activeNamesMeasure':activeNamesMeasure}
    print('*********exiting sensor_select************')
    return new_pars


def sample_cycle(i2c,lcd,pars):
    sensors=pars['sensors']
    activeFuncs=pars['activeFuncs']
    activeNamesMeasure=pars['activeNamesMeasure']
    #print('activeNames = ',activeNames)
    print('activeFuncs = ',activeFuncs)
    print('sensors = ',sensors)
    print('activeNamesMeasure = ',activeNamesMeasure)
    
    i=0
    while True:
        first = button.value()
        sleep(0.01)
        second = button.value()
        if first and not second:
            sensor=sensors[i]
            exec('sensor.print_'+activeFuncs[i]+'()')
            i = (i+1) % len(activeNamesMeasure)
        elif not first and second:
            pass

