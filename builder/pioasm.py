# 
##########################################################################
# Autor: WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico
# 
##########################################################################
from __future__ import print_function
import os, platform
from platform import system, machine
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
from time import sleep

def execute(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    lines = out.decode().split("\r\n")
    error = err.decode().split("\r\n")
    #print ('[PIO-ASM] RES', proc.returncode)
    #print ('[PIO-ASM] ERR', error)
    #print ('[PIO-ASM] OUT', lines)
    if proc.returncode == 0: 
        COLOR = Fore.GREEN
    else: 
        COLOR = Fore.RED
    for i in range( len(error) ):
        print( COLOR + error[i] )
        sleep(0.02)
    return proc.returncode

def dev_pioasm(env):
    sys_dir = system() +'_'+ machine()
    sys_dir = sys_dir.lower()
    if 'windows' in sys_dir: 
        sys_dir = 'windows'

    #print("SYSTEM", system())
    #print("MACHINE", machine())
    #print("SYS DIR", sys_dir)

    tool = env.PioPlatform().get_package_dir("tool-wizio-pico")
    if None == tool:
        print( Fore.RED + '[PIO-ASM] ERROR: The', sys_dir, 'is no supported yet...' )
        return
    
    src_name = env.BoardConfig().get("build.pio_src", "0")
    dst_name = env.BoardConfig().get("build.pio_dst", "0")
    if '0' == src_name:
        return

    if '0' == dst_name:
        dst_name = src_name + '.h'

    src = join(env.subst("$PROJECT_DIR"), src_name).replace("\\", "/")
    dst = join(env.subst("$PROJECT_DIR"), dst_name).replace("\\", "/")

    if True == os.path.isfile( dst ):
        print(Fore.GREEN + '[PIO-ASM]', dst)
        return

    if False == os.path.isfile( src ):
        print(Fore.RED + '[PIO-ASM] ERROR: Source file not exist ', src, "\n")
        exit(1)

    if False == os.path.isdir( os.path.dirname( dst )  ):
        print(Fore.RED + '[PIO-ASM] ERROR: Destination folder not exist', os.path.dirname( dst ), "\n")     
        exit(1)   

    cmd = []
    cmd.append(join(tool, sys_dir, 'pioasm') ) 
    cmd.append(join(env.subst("$PROJECT_DIR"), src))        
    cmd.append(join(env.subst("$PROJECT_DIR"), dst))  
 
    if execute(cmd) != 0:    
        exit(1) 

