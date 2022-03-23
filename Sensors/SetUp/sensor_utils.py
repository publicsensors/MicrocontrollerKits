# Utility functions for PublicSensors/SensoresPublicos sensor activities

from sys import print_exception
from time import sleep, sleep_ms
try: # The ESP32 build seems to lack sync, so skip if unavailable
    from os import sync
except:
    pass
from os import listdir
from machine import Pin, Timer

from SetUp.verbosity import vrb_print,vrb_setlevel

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

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
        vrb_print('loading default parameters from the default_param_file',level=5)
        module_name = default_param_file[:-3]
        vrb_print('importing ',module_name,level=5)
        def_pars=__import__(module_name)
        vrb_print(dir(def_pars.default_params),5)
        pars.update(def_pars.default_params.params)
    vrb_setlevel(pars['verbosity'])
    vrb_print('Default parameters:',level=20)
    vrb_print(pars,level=20)
    if user_param_file is None:
        user_param_file=pars['user_param_file']
        vrb_print('loading user-specfied parameters from '+user_param_file+' in subdirectory ',pars['setup_dir'])
    try:
        module_name = '%s.%s' % (pars['setup_dir'],user_param_file[:-3])
        vrb_print('importing ',module_name)
        user_pars=__import__(module_name)
        vrb_print(dir(user_pars.user_params))
        vrb_print('user_pars.user_params.params = ',user_pars.user_params.params)
        pars.update(user_pars.user_params.params)
        vrb_setlevel(pars['verbosity'])
    except Exception as e:
        vrb_print_exception(e)
        vrb_print('Unable to import user-specified parameter file')
    vrb_print('Final parameters:')
    vrb_print(pars)
    # return a local copy of the parameters, to be assigned to the global params if appropriate
    return pars


# Callback for irq attached to button or timer to trigger a sample
def trigger_sample(p):
    global sample_trigger # flag to trigger one sample in sample_loop
    global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
    vrb_print('irq ',p)
    # Check the source of the irq:
    # change this to use the __name__ field...
    if str(type(p)).find('Timer')>-1:
        vrb_print('Timer irq')
        if sample_cycle_flag>0:
            sample_trigger=1
    elif str(type(p)).find('Pin')>-1:
        vrb_print('Pin irq')
        sample_trigger=1    

        
# Callback to switch flag turning cyclic sampling on/off
def set_cycle_flag(p):
    global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
    #global sample_trigger # flag to trigger one sample in sample_loop
    vrb_print('Looping flag (set_cycle: {}) set to {}'.format(p,p.value()),level=4)
    sample_cycle_flag=p.value()

class Sampler:
    """ A class to handle sampling from sensors, data logging and user interfaces.
    """
    def __init__(self,pars,button=None,select_sensors=True):
        global sample_cycle_flag # flag to turn on/off cyclic sampling at preset intervals
        global sample_trigger # flag to trigger one sample in sample_loop
        global check_loop_state, state, p_smpl_loop

        self.pars=pars
        self.button=button
        self.rtc=self.pars['rtc']
        self.i2c=pars['i2c']
        self.lcd=pars['lcd']
        self.display_list = []

        # Set up initial sampling if looping is turned on
        # The two options below use the either the setting or the
        # initial position of the loop flag switch.
        if pars['default_sample_looping']:
        #if self.p_smpl_loop.value()==1:
            sample_cycle_flag=1  # flag to trigger loop sampling
            sample_trigger=1     # flag to trigger first sample
        else:
            sample_cycle_flag=0  # flag to trigger loop sampling
            sample_trigger=0     # flag to trigger first sample

        if select_sensors:
            self.sensor_select()

        if self.pars['auto_logging']:
            vrb_print('opening files for autologging...')
            self.start_log_files()
        
        self.loop_flag=0  # flag turning loop sampling off/on

        # Virtual timer for LCD display
        self.LCDtimer=self.pars['LCDtimer']
        if self.lcd:
            self.LCDtimer.init(mode=self.LCDtimer.PERIODIC,period=1000*pars['display_interval'],
                           callback=self.sample_display)
        
        # Timer for sample looping
        self.SMPLtimer=self.pars['SMPLtimer']
        self.SMPLtimer.init(mode=self.SMPLtimer.PERIODIC,period=1000*pars['sample_interval'],
                            callback=trigger_sample)
        
        # Timer for AQI is added here, so it can be deinited when requested
        self.AQtimer=self.pars['AQtimer']

        # Interrupt for sampling on button press
        self.p_smpl_trigger=Pin(self.pars['p_smpl_trigger_lbl'], Pin.IN,pull=Pin.PULL_DOWN)
        self.p_smpl_trigger.irq(trigger=Pin.IRQ_RISING,handler=trigger_sample)
        #self.p_smpl_trigger=Pin(self.pars['p_smpl_trigger_lbl'], Pin.IN,pull=Pin.PULL_UP)
        #self.p_smpl_trigger.irq(trigger=Pin.IRQ_FALLING,handler=trigger_sample)
        
        # The parameter pars['default_sample_looping'] determines the default sample looping behavior.
        # If True, the pin is pulled up and looping occurs unless there is a connection to GND.
        # If False, the pin is pulled down and looping occurs only when the pin is connected to V+.
        if pars['default_sample_looping']:
            try:
                self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN,pull=Pin.PULL_UP)
                vrb_print('set pull-up for p_smpl_loop: enable auto-looping')
            except:
                vrb_print('unable to set pull-up for p_smpl_loop')
                self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN)
        else:
            try:
                self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN,pull=Pin.PULL_DOWN)
                vrb_print('set pull-down for p_smpl_loop: disable auto-looping')
            except:
                vrb_print('unable to set pull-down for p_smpl_loop')
                self.p_smpl_loop=Pin(self.pars['p_smpl_loop_lbl'], Pin.IN)                
        self.p_smpl_loop.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING,handler=set_cycle_flag)
        
        if self.lcd:
            self.lcd.clear()
            self.lcd.putstr('Ready to sample!')

    def stop(self):
        """A method to stop sampling and IRQ calls by deinitializing the
           timers activating non-blocking sampling, display and logging.
        """
        vrb_print('>>> User requested stop: Deinitializing timers...')
        self.check_timer.deinit()
        self.LCDtimer.deinit()
        self.SMPLtimer.deinit()
        self.AQtimer.deinit()
                
    def pause(self):
        """An EXPERIMENTAL method to pause sampling (both loop and button-
           driven) in a recoverable way
        """
        vrb_print('>>> User requested pause: Disabling IRQs...')
        from machine import disable_irq
        self.irq_state=disable_irq()

    def resume(self):
        """A, EXPERIMENTAL method to resume sampling disabled by the
           pause() method.
        """
        vrb_print('>>> User requested resume: Enabling IRQs...')
        from machine import enable_irq
        self.irq_state=enable_irq(self.irq_state)

    def sample(self):
        """ A method callable from an irq, e.g ALARM0 for interval sampling and button-press 
            controlled sampling
        """
        global sensor_obj, sensor_module
        global sample_trigger,sample_cycle_flag
        vrb_print('A; sample_trigger,sample_cycle_flag =',sample_trigger,sample_cycle_flag)
        sample_trigger=0
        for i in range(len(self.pars['active_sensors'])):
            sensr=self.pars['active_sensors'][i]
            sensor_obj=self.pars['sensor_objs'][sensr]
            cmd='sensor_obj.print_'+self.pars['sensor_func_suffices'][sensr]+'()'
            vrb_print('\ntaking sensor reading with: ',cmd)
            exec(cmd)
                                                                     
    def sample_display(self,t):
        # A method to display output strings in sequence, callable
        # by a timer irq (t). Display strings come from the
        # display_str_list field of each read_X sensor driver.
        #vrb_print('irq ',t)
        #vrb_print('Entering sample_display...')
        for i in range(len(self.pars['active_sensors'])):
            sensr=self.pars['active_sensors'][i]
            sensor_obj=self.pars['sensor_objs'][sensr]
            for i in range(len(sensor_obj.display_str_list)):
                vrb_print('sensor_obj.display_str_list[i] = ',sensor_obj.display_str_list[i])
                vrb_print('3) sample_display: self.display_list = ',self.display_list)
                self.display_list.extend([sensor_obj.display_str_list[i]])
                vrb_print('4) sample_display: self.display_list = ',self.display_list)
            sensor_obj.display_str_list=[]
            #while len(sensor_obj.display_str_list)>0:
            #    self.display_list.extend(sensor_obj.display_str_list.pop(0))
            # This worked in sample:
            #self.display_list.extend(sensor_obj.display_str_list)
        if len(self.display_list) > 0:
            vrb_print('1) sample_display: self.display_list = ',self.display_list)
            display_str = self.display_list.pop(0)
            vrb_print("display_str = ",display_str)
            vrb_print('2) sample_display: self.display_list = ',self.display_list)
            self.lcd.clear()
            self.lcd.putstr(display_str)
        else:
            self.lcd.clear()
            wait_str = 'Waiting for data...'
            self.lcd.putstr(wait_str)
            
                                   
    def sample_check(self,t):
        # Performs one check whether a sample has been requested,
        # intended to be called by a timer (t)
        global sample_trigger 
        #vrb_print('sample_check...')
        if sample_trigger==1:
            vrb_print('sample triggered...')
            sample_trigger=0
            self.sample()
        # Write to logs in sequence. Log strings come from the 
        # the data_list field of the sensor object,
        # with the corresponding output format.
        #vrb_print('Entering sample_log...')
        for i in range(len(self.pars['active_sensors'])):
            sensr=self.pars['active_sensors'][i]
            sensor_obj=self.pars['sensor_objs'][sensr]
            if len(sensor_obj.data_list)>0: # check if data waits to be logged
                logfile=open(sensor_obj.logfilename,'a')
                while len(sensor_obj.data_list)>0: # cycle through data lines
                    data=sensor_obj.data_list.pop()
                    vrb_print('data = ',data)
                    vrb_print('self.log_format=',sensor_obj.log_format)
                    log_line=sensor_obj.log_format % tuple(data)
                    vrb_print('log_line = ',log_line)
                    vrb_print('logging to filename: ',sensor_obj.logfilename)
                    logfile.write(log_line)
                logfile.close()
                try:
                    sync()
                except:
                    pass
                                   
    def sample_loop_timer(self):
        # Method to initiate a timer that calls sample_check (a non-blocking
        # alternative to sampler_loop. sample_check also executes a non-
        # blocking logger.
        tmr_period = 50
        self.check_timer=self.pars['check_timer']
        self.check_timer.init(mode=Timer.PERIODIC,period=tmr_period,callback=self.sample_check)

    def sample_loop(self):
        global sample_trigger 
        vrb_print('Starting sample_loop')
        while True:
            if sample_trigger==1:
                vrb_print('sample triggered...')
                sample_trigger=0
                self.sample()
                                   
    def sample_cycle(self):
        global sample_trigger 
        vrb_print('Starting cycle with ',self.pars['sample_max'],' samples')
        for sample_count in range(self.pars['sample_max']):
            vrb_print('sample_count = ',sample_count)
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

        vrb_print('Detecting/initializing sensor drivers...')

        i2c=self.pars['i2c']
        smbus=self.pars['smbus']
        lcd=self.pars['lcd']
        rtc=self.pars['rtc']

        # Update list & dictionary in parameter dictionary to contain loaded and tested sensor drivers
        new_pars={'sensor_objs':{},
                  'active_sensors':[]}

        # Create a list of sensors flagged for use
        requestedSensors = [s for s in list(self.pars['sensor_list'].keys()) if self.pars['sensor_list'][s]>0]
        #requestedSensors.reverse()
        #vrb_print('requestedSensors = ',requestedSensors)

        # Import driver functions and test requested sensors
        for sensr in requestedSensors:
            try:
                module_name=self.pars['sensor_dirs'][sensr]+'.read_'+self.pars['sensor_func_suffices'][sensr]
                vrb_print('importing module_name = ',module_name)
                sensor_module=__import__(module_name) # import module, defining a class to support sensor ops
                cmd='sensor_module.read_'+self.pars['sensor_func_suffices'][sensr]+'.read_'+ \
                    self.pars['sensor_func_suffices'][sensr]+'(i2c=i2c,rtc=rtc,smbus=smbus)'
                    #self.pars['sensor_func_suffices'][sensr]+'(lcd=lcd,i2c=i2c,rtc=rtc,smbus=smbus)'
                sensor_obj=eval(cmd)                     # instantiate an object of that class
                vrb_print('success: queuing sensor driver ',self.pars['sensor_func_suffices'][sensr])
                cmd='sensor_obj.test_'+self.pars['sensor_func_suffices'][sensr]+'()'
                vrb_print('testing sensor driver with: ',cmd)
                sensor_test = eval(cmd)
                sleep(1)
                if sensor_test>0:
                    new_pars['active_sensors'].append(sensr)
                    new_pars['sensor_objs'].update({sensr:sensor_obj})
                    vrb_print('success: queuing sensor object for ',sensr)
            except Exception as e:
                print_exception(e)
                vrb_print('Error: sensor driver for ',sensr,' was requested but failed import or test')
        vrb_print('Final list of active sensors is: ',new_pars['active_sensors'])
        vrb_print('Updating pars with: ',new_pars)
        self.pars.update(new_pars)
    

            

    def start_log_files(self):
        # A method to initialize data log files
        # Log file names begin with a timestamp, followed by the name
        # of the sensor.
        #
        # If the RTC has been initialized, no data files can be overwritten with
        # this convention. However, if the RTC has its uninitialized value, log
        # files names would have the same names. To prevent that, an additional suffix
        # is added with the number of existing files with a .csv suffix.
        nfile=len([f for f in listdir(self.pars['sensor_log_directory']) if f.endswith('.csv')])

        # Open requested log files
        for sensr in self.pars['active_sensors']:
            nfile+=1
            timestamp=tuple([list(self.rtc.datetime())[d] for d in [0,1,2,4,5,6]])
            timestamp_str=self.pars['timestamp_format'] % timestamp
            logfilename=self.pars['sensor_log_directory']+'/'+timestamp_str+'_'+ \
                str(nfile) + '_' + self.pars['sensor_log_prefixes'][sensr]+'.csv'
            #logfilename=self.pars['sensor_log_directory']+'/'+timestamp_str+'_'+self.pars['sensor_log_prefixes'][sensr]+'.csv'
            vrb_print('creating log file: ',logfilename)
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
        


            
