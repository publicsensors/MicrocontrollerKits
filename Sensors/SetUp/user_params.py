# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'sensor_list':{'distance':0,
        'temperature':1,
        'light':1,
        'GPS':0},
        'sensor_log_directory':'Data',
        'sensor_log_flags':{ 'distance':0,
                       'temperature':1,
                            'light':1,
                             'GPS':0},
        'auto_logging':True,
        'sample_max':10,
        'sample_interval':10
}

