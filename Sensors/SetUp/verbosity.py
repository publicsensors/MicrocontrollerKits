#
# A minimalist function to regulate output verbosity for publicsensors sampling codes
#
global verbosity_level
vrb_level=10

def vrb_setlevel(*args):
    # Called with no arguments, returns verbosity level
    # Called with one argument, sets it as the verbosity level
    global verbosity_level
    if len(args)>0:
            verbosity_level = args[0]
    print('Verbosity level: ',verbosity_level)

def vrb_print(*args,level=10):
    global verbosity_level
    if verbosity_level == 0:
        print('verbosity_level = ',verbosity_level)
    if level<=verbosity_level:
        for a in args:
            print(a)
    
