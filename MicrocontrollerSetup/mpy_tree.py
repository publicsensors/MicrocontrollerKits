#
# A utility to create a parallel directory from a source directory, with a matching
# directory tree but with python (.py) files compiled into bytecode (.mpy) files.
# Files with suffices other than .py are ignored.
# Files with suffices other than .py can be specified for compilation if they are
# python scripts, and arbitrary suffices can be specified for copying.
# skip_files and copy_files are, respectively, lists of files to ignore and to
# copy intact.
#
#  D. Grunbaum 2023011720618 publicsensors.org/sensorespublicos.org
#
import os
import shutil

def compile_tree(src_dir='Sensors',
                 dest_dir='mpySensors',
                 compile_suffices=['py'],
                 copy_suffices=['mpy'],
                 skip_files=[],
                 copy_files=[],
                 mpy_cross='/home/dg/Micropython/micropython/mpy-cross/mpy-cross',
                 replace_dest=True):
    '''A method to record the elements of a directory tree comprising subdirectories or
       files with specified suffices (expected to be python files). 
           compile_suffices: a list of suffices for files to be compiled
           copy_suffices: a list of suffices for files to be copied without compiling
           mpy_cross: full path to a working copy of mpy-cross
           replace_dest: a flag indicating whether to replace or skip existing destination files
    '''
    if not os.path.isdir(dest_dir): # create destination dir, if not present
        os.mkdir(dest_dir)
    for dir_name, subdir_list, file_list in os.walk(src_dir):
        print('Found directory: %s' % dir_name)
        new_dir = dest_dir + dir_name.rsplit(src_dir)[1]
        print('New directory is ',new_dir)
        if not os.path.isdir(new_dir): # create destination subdir, if not present
            os.mkdir(new_dir)
        for fname in file_list:
            if fname in skip_files:
                print('Skipping file ',fname)
            # Copy files as directed:
            elif fname.rsplit('.')[-1] in copy_suffices or fname in copy_files:
                print('\t copying file %s' % fname)
                new_file = os.path.join(new_dir,fname)
                print('\t New file is %s' % new_file)
                if (os.path.isfile(new_file)) and replace_dest: # copy file
                    print('\t overwriting file %s' % new_file)
                    os.remove(new_file)
                    shutil.copyfile(os.path.join(dir_name,fname), new_file)
                elif (os.path.isfile(new_file)) and (not replace_dest): # skip file
                    print('\t skipping file %s' % new_file)
                elif (not os.path.isfile(new_file)) or replace_dest: # copy file
                    print('\t creating file %s' % new_file)
                    shutil.copyfile(os.path.join(dir_name,fname), new_file)
            # Compile files as directed:
            elif fname.rsplit('.')[-1] in compile_suffices:
                print('\t compiling file %s' % fname)
                src_file = os.path.join(dir_name,fname)
                new_fname = fname[:-len(fname.rsplit('.')[-1])] + 'mpy'
                new_file = os.path.join(new_dir,new_fname)
                print('\t New file is %s' % new_file)
                cmd = mpy_cross+' '+src_file+' -o '+new_file
                #cmd = mpy_cross+' -i '+src_file+' -o '+new_file
                print('Compiling with %s' % cmd)
                if (os.path.isfile(new_file)) and replace_dest: # copy file
                    print('\t overwriting file %s' % new_file)
                    os.remove(new_file)
                    os.system(cmd)
                elif (os.path.isfile(new_file)) and (not replace_dest): # skip file
                    print('\t skipping file %s' % new_file)
                elif (not os.path.isfile(new_file)) or replace_dest: # copy file
                    print('\t creating file %s' % new_file)
                    os.system(cmd)






