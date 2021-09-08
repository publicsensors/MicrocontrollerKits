# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'setup_dir':'SetUp',
        'user_param_file':'user_params.py',
        'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':1,
                       'color':1,
                       'GPS':1,
                       'AQI':1,
                       'voltage':1,
                       'pressure':1,
                       'exttime':1},
        'sensor_dirs':{'distance':'Acoustic',
                       'temperature':'Temperature',
                       'light':'Light',
                       'color':'Color',
                       'GPS':'GPS',
                       'AQI':'AirQuality',
                       'voltage':'Voltage',
                       'pressure':'Pressure',
                       'exttime':'ExtTime'},
        'sensor_func_suffices':{'distance':'dist',
                       'temperature':'temp',
                       'light':'light',
                       'color':'color',
                        'GPS':'GPS',
                        'AQI':'AQI',
                        'voltage':'volt',
                        'pressure':'press',
                        'exttime':'exttime'},
        'sensor_log_flags':{ 'distance':0,
                       'temperature':0,
                            'light':0,
                            'color':0,
                            'GPS':0,
                            'AQI':0,
                            'voltage':0,
                            'pressure':0,
                            'exttime':0},
        'sensor_log_prefixes':{'distance':'dist',
                       'temperature':'temp',
                       'color':'color',
                       'light':'light',
                        'GPS':'GPS',
                        'AQI':'AQI',
                        'voltage':'volt',
                        'pressure':'press',
                        'exttime':'exttime'},
        'sensor_log_headers':{'samplenum':'SampleNum',
                       'time':'Time',
                       'distance':{'dist':'Dist'},
                       'temperature':{'T':'Temp'},
                       'light':{'lux':'lux','full':'full','ir':'ir'},
                       'color':{'R':'R','G':'G','B':'B','full':'full'},
                        'GPS':{'GPStime':'GPStime','dec_lat':'dec_lat','dec_long':'dec_long'},
                        'AQI':{'PM25':'PM25','PM10':'PM10'},
                        'voltage':{'volt0':'volt0','volt1':'volt1','volt2':'volt2','volt3':'volt3'},
                        'pressure':{'temp':'Temp','press':'Press','humid':'Humid'},
                        'exttime':{'year':'Year','month':'Month','day':'Day','hour':'Hour','minute':'Minute','second':'Second'}},
        'sensor_log_formats':{'samplenum':'%d',
                       'time':'%4d-%02d-%02d %02d:%02d:%02d',
                       'distance':{'dist':'%f'},
                       'temperature':{'T':'%f'},
                       'light':{'lux':'%f','full':'%d','ir':'%d'},
                       'color':{'R':'%d','G':'%d','B':'%d','full':'%d'},
                        'GPS':{'GPStime':'%4d-%02d-%02dT%02d-%02d-%02d','dec_lat':'%f','dec_long':'%f'},
                        'AQI':{'PM25':'%f','PM10':'%f'},
                        'voltage':{'volt0':'%f','volt1':'%f','volt2':'%f','volt3':'%f'},
                        'pressure':{'temp':'%f','press':'%f','humid':'%f'},
                        'exttime':{'year':'%d','month':'%d','day':'%d','hour':'%d','minute':'%d','second':'%d'}},
        'sensor_log_directory':'Data',
        'sensor_objs':{},
        'active_sensors':[],
        'auto_logging':False,
        'default_sample_looping':True,
        'timestamp_format':'%4d-%02d-%02dT%02d-%02d-%02d',
        'sample_max':10,
        'sample_interval':10
}

