# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':0,
                       'color':1,
                       'GPS':0,
                       'AQI':0,
                       'voltage':1,
                       'pressure':0,
                       'exttime':1},
        'sensor_log_directory':'Data',
        'sensor_log_flags':{ 'distance':1,
                       'temperature':1,
                            'light':1,
                            'color':1,
                             'GPS':1,
                             'AQI':1,
                             'voltage':1,
                             'pressure':1,
                             'exttime':1},
        'auto_logging':True,
        'default_sample_looping':True,
        'sample_max':4,
        'sample_interval':120,
        'display_wait':5
}

