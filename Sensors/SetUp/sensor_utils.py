# Utility functions for PublicSensors/SensoresPublicos sensor activities

from sys import print_exception
from time import sleep, sleep_ms
try: # The ESP32 build seems to lack sync, so skip if unavailable
    from os import sync
except:
    pass
    
from machine import Pin, Timer

#from pyb import ExtInt

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
    print('set_cycle ',p,p.value())
    sample_cycle_flag=p.value()

# A minimalist debouncing preprocessing step for set_cycle_flag
global bnc_inprocess,bnc_query
bnc_inprocess = False # flag to prevent multiple invocations of debounce
bnc_query = Flase

def in_process():
    global bnc_inprocess
    bnc_inprocess = True
    bnc_timer = Timer(mode=Timer.ONE_SHOT,period=200,callback=out_process())
    
def out_process():
    global bnc_inprocess
    bnc_inprocess = False
    
def set_cycle_flag_process(p):
    global bnc_inprocess
    if bnc_inprocess:
        return
    else:
        in_process()  # call function to set inprocess flag
        set_cycle_flag_debounce(p)

def set_cycle_flag_debounce(p):
    global bnc_inprocess
    global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
    if bnc_inprocess: # a debounce is already in process
        return
    bnc_delay = 20 # delay between pin value samples, in ms
    bnc_num = 16   # number of p.value samples that must agree to accept state
    bnc_max = 64 # number of sample cycles before giving up
    bnc_inprocess = True
    state = p.value()
    for i in range(bnc_max):
        sleep_ms(bnc_delay)
        state = (state<<1 | p.value()) & (~2**bnc_num)
        print('i = ',i,', state = ',state)
        if i >= bnc_num-2:
            if state == 0:
                sample_cycle_flag = 0
                break
            if state == 2**bnc_num-1:
                sample_cycle_flag = 1
                break
    # condition satisfied or timed out -- reset inprocess flag 
    print('sample_cycle_flag =', sample_cycle_flag)
    bnc_inprocess = False


class Sampler:
    """ A class to handle sampling from sensors, data logging and user interfaces.
    """
    def __init__(self,pars,button=None,select_sensors=True):
        global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
        global sample_trigger # flag to trigger one sample in sample_loop

        self.pars=pars
        self.button=button
        self.rtc=self.pars['rtc']
        self.i2c=pars['i2c']
        self.lcd=pars['lcd']
        self.display_list = []

        if select_sensors:
            self.sensor_select()

        if self.pars['auto_logging']:
            print('opening files for autologging...')
            self.start_log_files()
        
        self.loop_flag=0  # flag turning loop sampling off/on

        # Virtual timer for LCD display
        self.LCDtimer=Timer()
        self.LCDtimer.init(mode=self.LCDtimer.PERIODIC,period=1000*pars['display_interval'],
                           callback=self.sample_display)
        
        # Virtual timer for sample looping
        self.SMPLtimer=Timer()
        self.SMPLtimer.init(mode=self.SMPLtimer.PERIODIC,period=1000*pars['sample_interval'],
                            callback=trigger_sample)
        
        # Interrupt for sampling on button press
        self.p_smpl_trigger=Pin(self.pars['p_smpl_trigger_lbl'], Pin.IN,pull=Pin.PULL_UP)
        self.p_smpl_trigger.irq(trigger=Pin.IRQ_FALLING,handler=trigger_sample)
        
        # The parameter pars['default_sample_looping'] determines the default sample looping behavior.
        # If True, the pin is pulled up and looping occurs unless there is a connection to GND.
        # If False, the pin is pulled down and looping occurs only when the pin is connected to V+.
        if pars['default_sample_looping']:
            self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN,pull=Pin.PULL_UP)
        else:
            self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN,pull=Pin.PULL_DOWN)
        #self.p_smpl_loop.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING,handler=set_cycle_flag_debounce)
        self.p_smpl_loop.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING,handler=set_cycle_flag)
        
        # Set up initial sampling if looping is turned on
        if self.p_smpl_loop.value()==1:
            sample_cycle_flag=1  # flag to trigger loop sampling
            sample_trigger=1     # flag to trigger first sample
                
    def sample(self):
        """ A method callable from an irq, e.g ALARM0 for interval sampling and button-press 
            controlled sampling
        """
        global sensor_obj, sensor_module
        for i in range(len(self.pars['active_sensors'])):
            sensr=self.pars['active_sensors'][i]
            sensor_obj=self.pars['sensor_objs'][sensr]
            cmd='sensor_obj.print_'+self.pars['sensor_func_suffices'][sensr]+'()'
            print('\ntaking sensor reading with: ',cmd)
            #exec(cmd)
            data_list,display_str_list = eval(cmd)
            #display_str = eval(cmd)
            #if len(display_str) > 0:
            self.display_list.extend(display_str_list)
            #for display_str in display_str_list:
            #    print("display_str = ",display_str)
            #    self.display_list.append(display_str)
            for data in data_list:
                print('data = ',data)
                print('self.log_format=',sensor_obj.log_format)
                log_line=sensor_obj.log_format % tuple(data)
                print('log_line = ',log_line)
                print('logging to filename: ',sensor_obj.logfilename)
                logfile=open(sensor_obj.logfilename,'a')
                logfile.write(log_line)
                logfile.close()
            try:
                sync()
            except:
                pass
            sleep_ms(250)
                    
                    
                #sleep_ms(1000*self.pars['display_interval'])
                                  
    def sample_display(self,p):
        # A method to display output strings in sequence, callable
        # by a timer irq
        #print('irq ',p)
        #print('Displaying next output string:')
        if len(self.display_list) > 0:
            display_str = self.display_list.pop(0)
            print("display_str = ",display_str)
            self.lcd.clear()
            self.lcd.putstr(display_str)
                                   
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
        # use a global variable to fix global vs. local namespace issues
        global sensor_func
        global sensor_obj, sensor_module

        print('Detecting/initializing sensor drivers...')

        i2c=self.pars['i2c']
        smbus=self.pars['smbus']
        lcd=self.pars['lcd']
        rtc=self.pars['rtc']

        # Update list & dictionary in parameter dictionary to contain loaded and tested sensor drivers
        new_pars={'sensor_objs':{},
                  'active_sensors':[]}

        # Create a list of sensors flagged for use
        requestedSensors = [s for s in list(self.pars['sensor_list'].keys()) if self.pars['sensor_list'][s]>0]
        #
        #  NOTE: A bug causes onewire to crash if initialized before the GPS and AQI uarts.
        #        Reversing the order avoids this bug.
        #
        requestedSensors.reverse()
        print('requestedSensors = ',requestedSensors)

        # Import driver functions and test requested sensors
        for sensr in requestedSensors:
            try:
                module_name=self.pars['sensor_dirs'][sensr]+'.read_'+self.pars['sensor_func_suffices'][sensr]
                print('importing module_name = ',module_name)
                sensor_module=__import__(module_name) # import module, defining a class to support sensor ops
                cmd='sensor_module.read_'+self.pars['sensor_func_suffices'][sensr]+'.read_'+ \
                    self.pars['sensor_func_suffices'][sensr]+'(i2c=i2c,rtc=rtc,smbus=smbus)'
                    #self.pars['sensor_func_suffices'][sensr]+'(lcd=lcd,i2c=i2c,rtc=rtc,smbus=smbus)'
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

        for sensr in self.pars['active_sensors']:
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            timestamp_str=self.pars['timestamp_format'] % timestamp
            logfilename=self.pars['sensor_log_directory']+'/'+timestamp_str+'_'+self.pars['sensor_log_prefixes'][sensr]+'.csv'
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
            try:
                sync()
            except:
                pass

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
        


            
