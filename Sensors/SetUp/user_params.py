# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets user-specified parameters. Default parameters are set in default_params.py.
#
params={'sensor_list':{'distance':0,
                       'temperature':1,
                       'light':0,
                       'UIV':0,
                       'color':0,
                       'GPS':0,
                       'AQI':0,
                       'CO2':0,
                       'voltage':0,
                       'pressure':0,
                       'exttime':0},
        'sensor_log_directory':'Data',
        'sensor_log_flags':{ 'distance':1,
                       'temperature':1,
                            'light':1,
                            'UIV':1,
                            'color':1,
                             'GPS':1,
                             'AQI':1,
                             'CO2':1,
                             'voltage':1,
                             'pressure':1,
                             'exttime':1},
        'auto_logging':True,
        'default_sample_looping':True,
        'sample_max':4,
        'sample_interval':120,
        'display_interval':3,
        'verbosity':14,
        'bt_flag':1
}

