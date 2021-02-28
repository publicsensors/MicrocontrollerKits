# Utility functions for PublicSensors/SensoresPublicos sensor activities

from sys import print_exception
from time import sleep, sleep_ms
from os import sync

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
        print('user_pars.user_params.params = ',user_pars.user_params.params)
        pars.update(user_pars.user_params.params)
    except Exception as e:
        print_exception(e)
        print('Unable to import user-specified parameter file')
    print('Final parameters:')
    print(pars)
    # return a local copy of the parameters, to be assigned to the global params if appropriate
    return pars

def sensor_select(i2c,lcd,pars,rtc):
    """A function to detect, initialize and test alternative sensors for 
       PublicSensors/SensoresPublicos activities

       Sensor drivers that successfully import and pass testing are entered into the active_sensors
       list in the pars dictionary
    """
    global sensor # use a global variable to fix global vs. local namespace issues
    global sensor_func
    global sensor_obj, sensor_module
    
    # Update list & dictionary in parameter dictionary to contain loaded and tested sensor drivers
    new_pars={'sensor_objs':{},
              'active_sensors':[]}
    
    # Create a list of sensors flagged for use
    requestedSensors = [s for s in list(pars['sensor_list'].keys()) if pars['sensor_list'][s]>0]
    print('requestedSensors = ',requestedSensors)

    # Import driver functions and test requested sensors
    for sensr in requestedSensors:
        try:
            module_name=pars['sensor_dirs'][sensr]+'.read_'+pars['sensor_func_suffices'][sensr]
            print('importing module_name = ',module_name)
            sensor_module=__import__(module_name) # import module, defining a class to support sensor ops
            cmd='sensor_module.read_'+pars['sensor_func_suffices'][sensr]+'.read_'+ \
                pars['sensor_func_suffices'][sensr]+'(lcd=lcd,i2c=i2c,rtc=rtc)'
            #cmd='sensor_module.read_'+pars['sensor_func_suffices'][sensr]+'.read_'+pars['sensor_func_suffices'][sensr]+'()'
            sensor_obj=eval(cmd)                     # instantiate an object of that class
            print('success: queuing sensor driver ',pars['sensor_func_suffices'][sensr])
            #print('dir(sensor_obj) = ',dir(sensor_obj))
            cmd='sensor_obj.test_'+pars['sensor_func_suffices'][sensr]+'()'
            print('testing sensor driver with: ',cmd)
            sensor_test = eval(cmd)
            sleep(1)
            if sensor_test>0:
                new_pars['active_sensors'].append(sensr)
                new_pars['sensor_objs'].update({sensr:sensor_obj})
                print('success: queuing sensor object for ',sensr)
        except Exception as e:
            print_exception(e)
            print('Error: sensor driver for ',sensr,' was requested but failed import or test')
    print('Final list of active sensors is: ',new_pars['active_sensors'])
    print(new_pars)
    return new_pars

def sample_cycle(pars,button,sample_loop=1):
    global sensor_obj, sensor_module
    if sample_loop==1: # take sensor readings when button is pressed
        i=0
        while True:
            first = button.value()
            sleep(0.01)
            second = button.value()
            if first and not second:
                sensr=pars['active_sensors'][i]
                sensor_obj=pars['sensor_objs'][sensr]
                cmd='sensor_obj.print_'+pars['sensor_func_suffices'][sensr]+'()'
                print('printing sensor reading with: ',cmd)
                exec(cmd)
                i = (i+1) % len(pars['active_sensors'])
            elif not first and second:
                pass
    elif sample_loop==0: # launch sampling at preset intervals determined by sample_max, sample_interval in pars
        for sample_count in range(pars['sample_max']):
            for i in range(len(pars['active_sensors'])):
                sensr=pars['active_sensors'][i]
                sensor_obj=pars['sensor_objs'][sensr]
                cmd='sensor_obj.print_'+pars['sensor_func_suffices'][sensr]+'()'
                print('printing sensor reading with: ',cmd)
                exec(cmd)
            sleep(pars['sample_interval'])
                                   

def start_log_files(i2c,lcd,pars,rtc):
    global sensor_obj, sensor_module

    for sensr in pars['active_sensors']:
        timestamp=tuple([list(rtc.datetime())[d] for d in [0,1,2,4,5,6]])
        timestamp_str=pars['timestamp_format'] % timestamp
        logfilename=timestamp_str+'_'+pars['sensor_log_prefixes'][sensr]+'.csv'
        print('creating log file: ',logfilename)
        logfile=open(logfilename,'w')
        sensor_log_format=pars['sensor_log_formats'][sensr]
        fmt_keys=list(sensor_log_format.keys())
        header=''
        for s in ['samplenum','time']:
            header+=pars['sensor_log_headers'][s]+','
        for s in fmt_keys:
            header+=pars['sensor_log_headers'][sensr][s]+','
        header=header[:-1]+'\n' # drop the trailing comma, add a <cr>
        logfile.write(header)
        logfile.close()
        sleep_ms(250)
        sync()

        # update fields in sensor object
        pars['sensor_objs'][sensr].logging=True
        pars['sensor_objs'][sensr].logfilename=logfilename
        pars['sensor_objs'][sensr].sample_num=0
        pars['sensor_objs'][sensr].fmt_keys=fmt_keys

        # construct formats for log data lines
        log_format=''
        for s in ['samplenum','time']:
            log_format+=pars['sensor_log_formats'][s]+','
        for s in fmt_keys:
            log_format+=pars['sensor_log_formats'][sensr][s]+','
        log_format=log_format[:-1]+'\n' # drop the trailing comma, add a <cr>
        pars['sensor_objs'][sensr].log_format=log_format
        
        


