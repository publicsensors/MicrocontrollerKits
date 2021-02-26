# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'setup_dir':'SetUp',
        'user_param_file':'user_params.py',
        'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':1,
                       'GPS':1},
        'sensor_dirs':{'distance':'Acoustic',
                       'temperature':'Temperature',
                       'light':'Light',
                       'GPS':'GPS'},
        'sensor_func_suffices':{'distance':'dist',
                       'temperature':'temp',
                       'light':'light',
                        'GPS':'GPS'},
        'sensor_log_flags':{ 'distance':0,
                       'temperature':0,
                            'light':0,
                            'GPS':0},
        'sensor_log_prefixes':{'distance':'dist',
                       'temperature':'temp',
                       'light':'light',
                        'GPS':'GPS'},
        'sensor_log_headers':{'samplenum':'SampleNum',
                       'time':'Time',
                       'distance':{'default':'Dist'},
                       'temperature':{'default':'Temp'},
                       'light':{'lux':'lux','full':'full','ir':'ir'},
                              'GPS':{'default':'GPS'}},
        'sensor_log_formats':{'samplenum':'%d',
                       'time':'%4d-%02d-%02dT%02d-%02d-%02d',
                       'distance':'dist',
                       'temperature':{'default':'%f'},
                       'light':{'lux':'%f','full':'%d','ir':'%d'},
                        'GPS':'GPS'},
        'sensor_objs':{},
        'active_sensors':[],
        'auto_logging':False,
        'timestamp_format':'%4d-%02d-%02dT%02d-%02d-%02d',
        'sample_max':1000,
        'sample_interval':60
}

