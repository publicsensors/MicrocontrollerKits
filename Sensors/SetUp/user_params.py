# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets user-specified parameters. Default parameters are set in default_params.py.
#
params={'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':1,
                       'UIV':0,
                       'color':0,
                       'humidity':0,
                       'GPS':0,
                       'AQI':0,
                       'CO2':0,
                       'voltage':0,
                       'pressure':0,
                       'exttime':1},
        'sensor_log_directory':'Data',
        'sensor_log_flags':{ 'distance':0,
                       'temperature':0,
                            'light':0,
                            'UIV':0,
                            'color':0,
                            'humidity':0,
                             'GPS':0,
                             'AQI':0,
                             'CO2':0,
                             'voltage':0,
                             'pressure':0,
                             'exttime':0},
        'auto_logging':True,
        'default_sample_looping':True,
        'sample_max':4,
        'sample_interval':10*60,
        'display_interval':8,
        'output_level':'base', # Output options: 'base', 'low','med', 'high', or number 1-15
        'bt_send':0,
        'bt_rec':0
}

