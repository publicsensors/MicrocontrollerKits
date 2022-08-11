# Default parameters for PublicSensors/SensoresPublicos kit and instrument activities
#
# This script sets default parameters. User-specified parameters are set (by default) in user_params.py.
#
params={'setup_dir':'SetUp',
        'user_param_file':'user_params.py',
        'sensor_list':{'distance':1,
                       'temperature':1,
                       'light':1,
                       'UIV':0,
                       'color':0,
                       'humidity':0,
                       'GPS_alt':0,
                       'GPS_vel':0,
                       'AQI':0,
                       'CO2':0,
                       'voltage':0,
                       'pressure':0,
                       'exttime':1},
        'sensor_dirs':{'distance':'Acoustic',
                       'temperature':'Temperature',
                       'light':'Light',
                       'UIV':'UIV',
                       'color':'Color',
                       'humidity':'Humidity',
                       'GPS_alt':'GPS',
                       'GPS_vel':'GPS',
                       'AQI':'AirQuality',
                       'CO2':'CO2',
                       'voltage':'Voltage',
                       'pressure':'Pressure',
                       'exttime':'ExtTime'},
        'sensor_func_suffices':{'distance':'dist',
                       'temperature':'temp',
                       'light':'light',
                       'UIV':'UIV',
                       'color':'color',
                       'humidity':'humidity',
                        'GPS_alt':'GPSalt',
                        'GPS_vel':'GPSvel',
                        'AQI':'AQI',
                        'CO2':'CO2',
                        'voltage':'volt',
                        'pressure':'press',
                        'exttime':'exttime'},
        'sensor_log_flags':{ 'distance':0,
                       'temperature':0,
                            'light':0,
                            'UIV':0,
                            'color':0,
                            'humidity':0,
                            'GPS_alt':0,
                            'GPS_vel':0,
                            'AQI':0,
                            'CO2':0,
                            'voltage':0,
                            'pressure':0,
                            'exttime':0},
        'sensor_log_prefixes':{'distance':'dist',
                       'temperature':'temp',
                       'color':'color',
                       'humidity':'humidity',
                       'light':'light',
                       'UIV':'UIV',
                        'GPS_alt':'GPSalt',
                        'GPS_vel':'GPSvel',
                        'AQI':'AQI',
                        'CO2':'CO2',
                        'voltage':'volt',
                        'pressure':'press',
                        'exttime':'exttime'},
        'sensor_log_headers':{'samplenum':'SampleNum',
                       'time':'Time',
                       'distance':{'dist':'Dist'},
                       'temperature':{'T':'Temp','sensor_id':'ROM_ID'},
                       'light':{'lux':'lux','full':'full','ir':'ir'},
                       'UIV':{'uv':'uv','ir':'ir','vis':'vis'},
                       'color':{'R':'R','G':'G','B':'B','full':'full'},
                        'humidity':{'humid':'Humid','temp':'Temp'},
                        'GPS_alt':{'GPStime':'GPStime','dec_lat':'dec_lat','dec_long':'dec_long','altitude':'altitude'},
                        'GPS_vel':{'GPStime':'GPStime','dec_lat':'dec_lat','dec_long':'dec_long',
                               'mps':'mps','course':'course'},
                        'AQI':{'PM25':'PM25','PM10':'PM10'},
                        'CO2':{'ppm':'ppm','temp':'temp'},
                        'voltage':{'volt0':'volt0','volt1':'volt1','volt2':'volt2','volt3':'volt3'},
                        'pressure':{'temp':'Temp','press':'Press','humid':'Humid'},
                        'exttime':{'year':'Year','month':'Month','day':'Day','hour':'Hour','minute':'Minute','second':'Second'}},
        'sensor_log_formats':{'samplenum':'%d',
                       'time':'%4d-%02d-%02d %02d:%02d:%02d',
                       'distance':{'dist':'%f'},
                       'temperature':{'T':'%f','sensor_id':'%s'},
                       'light':{'lux':'%f','full':'%d','ir':'%d'},
                       'UIV':{'uv':'%f','ir':'%d','vis':'%d'},
                       'color':{'R':'%d','G':'%d','B':'%d','full':'%d'},
                        'humidity':{'temp':'%f','humid':'%f'},
                        'GPS_alt':{'GPStime':'%4d-%02d-%02dT%02d-%02d-%02d','dec_lat':'%f','dec_long':'%f','altitude':'%f'},
                        'GPS_vel':{'GPStime':'%4d-%02d-%02dT%02d-%02d-%02d','dec_lat':'%f','dec_long':'%f',
                               'mps':'%f','course':'%f'},
                        'AQI':{'PM25':'%f','PM10':'%f'},
                        'CO2':{'ppm':'%f','temp':'%f'},
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
        'sample_interval':10,
        'display_interval':0,
        'output_level':'base', # Output options: 'base', 'low','med', 'high', or number 1-15
        'bt_send':0,
        'bt_rec':0,
        'bt_log':1,
        'bt_log_prefix':'BTtelem',
        'bt_rec_interval':250,
        'bt_start_str':'|||>',
        'bt_end_str':'<|||',
        'IDchars':4,
        'instr_name':None
}

