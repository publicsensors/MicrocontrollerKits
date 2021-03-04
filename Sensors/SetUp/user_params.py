# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'sensor_list':{'distance':0,
                       'temperature':1,
                       'light':1,
                       'GPS':1,
                       'AQI':1},
        'sensor_log_directory':'Data',
        'sensor_log_flags':{ 'distance':0,
                       'temperature':1,
                            'light':1,
                             'GPS':1,
                             'AQI':1},
        'auto_logging':True,
        'sample_max':4,
        'sample_interval':120
}

