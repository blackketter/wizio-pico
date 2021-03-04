import os
from os.path import join

def add_pico(array, line, filename):
    line = line.strip()
    #print(line)    
    words = line.split(" ") 
    define = words[1]
    if '_H_' in line: return
    if define not in array:
        if len(words) > 2: 
            print ( define + ',' + words[2] + ',' + filename + ',' + ',' )
        else: 
            print ( define + ',' + ',' + filename + ',' + ',' )
        array.append( define )


def list_files(startpath):
    A = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for fn in files:
            #print('{}{}'.format(subindent, fn))
            if '.h' in fn or '.c' in fn or '.S' in fn: 
                with open( join(root, fn), mode='r') as f: 
                    Lines = f.readlines()
                    for L in Lines:
                        if '#if PICO_' in L: add_pico(A, L, fn)
                        if '#ifndef PICO_' in L: add_pico(A, L, fn)
                        if '#define PICO_' in L: add_pico(A, L, fn)
                f.close()
            


if __name__ == "__main__":
    path = 'C:/Users/1124/.platformio/packages/framework-wizio-pico/SDK'
    list_files(path)         

    #https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/  