#
# A minimalist set of codes to regulate output verbosity for publicsensors sampling codes
#
# Use vrb_setlevel to set the global parameter "verbosity_level". Thereafter, arguments
# of vrb_print will be printed to the REPL iff the parameter "level"<=verbosity_level.
#
# verbosity _level is set in default_params and user_params in public_sensors code; change
# those settings to modulate terminal output.
#
# verbosity_dict is a dictionary than enables descriptive in addition to numerical settings.

global verbosity_level, verbosity_dict
verbosity_level=5
verbosity_dict={'base':2,'low':5,'med':10,'high':15}

def vrb_setlevel(*args):
    # Called with no arguments, returns verbosity level
    # Called with one argument, sets it as the verbosity level
    global verbosity_level
    if len(args)==0:
        print('Verbosity level: ',verbosity_level)
    else:
        if isinstance(args[0],int) or isinstance(args[0],float):
            verbosity_level=args[0]
        elif isinstance(args[0],str):
            try:
                verbosity_level=verbosity_dict[args[0]]
            except:
                print('Verbosity error: verbosity_level in vrb_print must be a number or in ',list(verbosity_dict.keys()))
                verbosity_level = verbosity_dict['base']
    
        
def vrb_print(*args,level='med'):
    global verbosity_level
    if isinstance(level,int) or isinstance(level,float):
        plevel=level
    elif isinstance(level,str):
        try:
            plevel=verbosity_dict[level]
        except:
            print('Verbosity error: level in vrb_print must be a number or in ',list(verbosity_dict.keys()))
            plevel = verbosity_dict['base']
    if plevel<=verbosity_level:
        for a in args:
            print(a)
    
