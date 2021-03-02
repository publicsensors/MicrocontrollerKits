# Utility functions for PublicSensors/SensoresPublicos sensor activities

from sys import print_exception
from time import sleep, sleep_ms
from os import sync
from machine import Pin, Timer

from pyb import ExtInt

import micropython
micropython.alloc_emergency_exception_buf(100)

global sample_trigger # flag to trigger one sample in sample_loop
sample_trigger=0
global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
sample_cycle_flag=0

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


# Callback for irq attached to button or timer to trigger a sample
def trigger_sample(p):
    global sample_trigger # flag to trigger one sample in sample_loop
    global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
    print('irq ',p)
    # Check the source of the irq:
    # change this to use the __name__ field...
    if str(type(p)).find('Timer')>-1:
        print('Timer irq')
        if sample_cycle_flag>0:
            sample_trigger=1
    elif str(type(p)).find('Pin')>-1:
        print('Pin irq')
        sample_trigger=1    

        
# Callback to switch flag turning cyclic sampling on/off
def set_cycle_flag(p):
    global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
    print('set_cycle ',p)
    sample_cycle_flag=p.value()


class Sampler:
    """ A class to handle sampling from sensors, data logging and user interfaces.
    """
    def __init__(self,pars,button=None,p_sample_loop=None,select_sensors=True):
        self.pars=pars
        self.button=button
        self.p_sample_loop=p_sample_loop
        self.rtc=self.pars['rtc']
        self.i2c=pars['i2c']
        self.lcd=pars['lcd']

        if select_sensors:
            self.sensor_select()

        if self.pars['auto_logging']:
            print('opening files for autologging...')
            self.start_log_files()
        
        # Button on Pin 13 gives lots of bounces
        # set up irq for sampling on button-press
        #self.button_sample(setting=True)
       # set up/clear an irq for button-press controlled sampling
        #self.button.irq(handler=self.button_sample,trigger=Pin.IRQ_RISING)

        self.loop_flag=0  # flag turning loop sampling off/on

        self.timer=Timer()
        self.timer.init(mode=self.timer.PERIODIC,period=1000*pars['sample_interval'],callback=trigger_sample)

        pSCK=Pin('SCK',mode=Pin.IN,pull=Pin.PULL_UP)
        pSCK.irq(trigger=Pin.IRQ_FALLING,handler=trigger_sample)

        pMISO=Pin('MISO',mode=Pin.IN,pull=Pin.PULL_UP)
        pMISO.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING,handler=set_cycle_flag)
                
    def sample(self):
        """ A method callable from an irq, e.g ALARM0 for interval sampling and button-press 
            controlled sampling
        """
        global sensor_obj, sensor_module
        for i in range(len(self.pars['active_sensors'])):
                sensr=self.pars['active_sensors'][i]
                sensor_obj=self.pars['sensor_objs'][sensr]
                cmd='sensor_obj.print_'+self.pars['sensor_func_suffices'][sensr]+'()'
                print('taking sensor reading with: ',cmd)
                exec(cmd)
                                  
    def sample_loop(self):
        global sample_trigger #sensor_obj, sensor_module
        print('Starting sample_loop')
        while True:
            if sample_trigger==1:
                print('sample triggered...')
                sample_trigger=0
                self.sample()
                                   
    def sample_cycle(self):
        global sample_trigger #sensor_obj, sensor_module
        print('Starting cycle with ',self.pars['sample_max'],' samples')
        for sample_count in range(self.pars['sample_max']):
            print('sample_count = ',sample_count)
            self.sample()
            sleep(self.pars['sample_interval'])

    def sensor_select(self):
        """A function to detect, initialize and test alternative sensors for 
           PublicSensors/SensoresPublicos activities

           Sensor drivers that successfully import and pass testing are entered into the active_sensors
           list in the pars dictionary
        """
        #global sensor # use a global variable to fix global vs. local namespace issues
        global sensor_func
        global sensor_obj, sensor_module

        print('Detecting/initializing sensor drivers...')

        i2c=self.pars['i2c']
        lcd=self.pars['lcd']
        rtc=self.pars['rtc']

        # Update list & dictionary in parameter dictionary to contain loaded and tested sensor drivers
        new_pars={'sensor_objs':{},
                  'active_sensors':[]}

        # Create a list of sensors flagged for use
        requestedSensors = [s for s in list(self.pars['sensor_list'].keys()) if self.pars['sensor_list'][s]>0]
        print('requestedSensors = ',requestedSensors)

        # Import driver functions and test requested sensors
        for sensr in requestedSensors:
            try:
                module_name=self.pars['sensor_dirs'][sensr]+'.read_'+self.pars['sensor_func_suffices'][sensr]
                print('importing module_name = ',module_name)
                sensor_module=__import__(module_name) # import module, defining a class to support sensor ops
                cmd='sensor_module.read_'+self.pars['sensor_func_suffices'][sensr]+'.read_'+ \
                    self.pars['sensor_func_suffices'][sensr]+'(lcd=lcd,i2c=i2c,rtc=rtc)'
                sensor_obj=eval(cmd)                     # instantiate an object of that class
                print('success: queuing sensor driver ',self.pars['sensor_func_suffices'][sensr])
                cmd='sensor_obj.test_'+self.pars['sensor_func_suffices'][sensr]+'()'
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
        print('Updating pars with: ',new_pars)
        self.pars.update(new_pars)
    

            

    def start_log_files(self):
        #global sensor_obj, sensor_module

        for sensr in self.pars['active_sensors']:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            timestamp_str=self.pars['timestamp_format'] % timestamp
            logfilename=self.pars['sensor_log_directory']+'/'+timestamp_str+'_'+self.pars['sensor_log_prefixes'][sensr]+'.csv'
            #logfilename=timestamp_str+'_'+self.pars['sensor_log_prefixes'][sensr]+'.csv'
            print('creating log file: ',logfilename)
            logfile=open(logfilename,'w')
            sensor_log_format=self.pars['sensor_log_formats'][sensr]
            fmt_keys=list(sensor_log_format.keys())
            header=''
            for s in ['samplenum','time']:
                header+=self.pars['sensor_log_headers'][s]+','
            for s in fmt_keys:
                header+=self.pars['sensor_log_headers'][sensr][s]+','
            header=header[:-1]+'\n' # drop the trailing comma, add a <cr>
            logfile.write(header)
            logfile.close()
            sleep_ms(250)
            sync()

            # update fields in sensor object
            self.pars['sensor_objs'][sensr].logging=True
            self.pars['sensor_objs'][sensr].logfilename=logfilename
            self.pars['sensor_objs'][sensr].sample_num=0
            self.pars['sensor_objs'][sensr].fmt_keys=fmt_keys

            # construct formats for log data lines
            log_format=''
            for s in ['samplenum','time']:
                log_format+=self.pars['sensor_log_formats'][s]+','
            for s in fmt_keys:
                log_format+=self.pars['sensor_log_formats'][sensr][s]+','
            log_format=log_format[:-1]+'\n' # drop the trailing comma, add a <cr>
            self.pars['sensor_objs'][sensr].log_format=log_format
        


            
