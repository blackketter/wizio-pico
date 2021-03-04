import os, shutil
from os.path import join, normpath, basename
from shutil import copyfile

def do_mkdir(path, name):
    dir = join(path, name)
    if False == os.path.isdir( dir ):
        try:
            os.mkdir(dir)
        except OSError:
            print ("[ERROR] Creation of the directory %s failed" % dir)
            exit(1) 
        else: 
            #print ("[MK]  %s" % dir)
            pass
    else:
        #print ("[EXIST]  %s" % dir)        
        pass 
    return dir  

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
                pass
            except: pass
        else:
            try:
                shutil.copy2(s, d)    
                pass            
            except: pass

def copy_hardware(path, dst):
    for root, dirs, files in os.walk(path):
        src = os.path.basename(root)
        if 'hardware_' in src:
            for f in files:
                if '.c' in f or '.S' in f:
                    if False == os.path.isfile( join(dst, f) ): 
                        copyfile( join(root, f), join(dst, f) )

def copytree_h(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        if '.txt' in item: continue
        if '.md' in item: continue
        if '.c' in item: continue
        if '.S' in item: continue
        if '.ld' in item: continue
        if '.in' in item: continue
        if 'boards' in item: continue # TODO
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
                pass
            except: pass
        else:
            try:
                shutil.copy2(s, d)    
                pass            
            except: pass

def copy_include(path, dst):
    for root, dirs, files in os.walk(path):
        src = os.path.basename(root)
        if 'asminclude' in root: continue
        if 'boot_stage2' in root: continue
        if 'include' not in root: continue
        name = root[root.index('include') + 8:]
        #print ( name )
        do_mkdir(join(path, dst), name)
        for f in files:
            if '.h' in f or '.S' in f:
                file = join(dst, name, f)
                if False == os.path.isfile( file ): 
                    #print ( file )
                    copyfile( join(root, f), file )        

def copy_pico(path, dst):
    for root, dirs, files in os.walk(path):
        src = os.path.basename(root)
        if 'include' in root: continue
        if 'asminclude' in root: continue
        if 'boot_stage2' in root: continue
        if 'pico_' not in root: continue
        name = root[root.index('pico_'):]
        do_mkdir(join(path, dst), name)
        for f in files:
            if '.c' in f or '.S' in f or '.ld' in f:
                file = join(dst, name, f)
                if False == os.path.isfile( file ): 
                    copyfile( join(root, f), file )

def sanitize(path):
    for root, dirs, files in os.walk(path):
        if not os.listdir(root) :
            shutil.rmtree(root)
       
def main(): # TODO arg

    path = "C:/Users/1124/Desktop/SDK/"
    src = "pico-sdk"
    dst = "SDK"

    #try: shutil.rmtree( "C:/Users/1124/Desktop/SDK/SDK" )
    #except: pass

    do_mkdir(path, dst)
    do_mkdir(join(path, dst), 'boot')
    do_mkdir(join(path, dst), 'include')
    do_mkdir(join(path, dst), 'hardware')
    do_mkdir(join(path, dst), 'pico')
    do_mkdir(join(path, dst), 'boot_stage2')

    copy_hardware(join(path, src), join(path, dst, 'hardware'))
    copy_include( join(path, src), join(path, dst, 'include') )
    copy_pico( join(path, src), join(path, dst, 'pico') )
    copytree( join(path, src, 'rp2_common', 'boot_stage2'), join(path, dst, 'boot_stage2') )

    sanitize( join(path, dst) )
    print ( 'DONE' )

if __name__ == "__main__":
    main()
