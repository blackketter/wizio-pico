# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

import os
from os.path import join
from shutil import copyfile
from SCons.Script import DefaultEnvironment, Builder
from common import *

def dev_create_template(env):
    D = join(env.subst("$PROJECT_DIR"), "src")
    S = join(env.PioPlatform().get_package_dir("framework-wizio-pico"), "templates", env.BoardConfig().get("build.core"))
    if False == os.path.isfile( join(D, "main.c") ) and False == os.path.isfile( join(D, "main.cpp") ):
        copyfile( join(S, "main.c"), join(D, "main.c") ) 
                
def dev_init(env, platform):
    env.platform = platform
    print( "RASPBERRYPI PI PICO RP2040 PICO-SDK")    
    dev_create_template(env)
    dev_compiler(env, 'BAREMETAL')
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    add_flags(env, optimization = '-Os') # TODO
    include_common(env)
    env.Append( 
        CPPDEFINES = [ platform.upper() ],
        CPPPATH    = [ join(env.framework_dir, "pico-sdk", "src", "boards", "include") ] 
    )   
# LIBRARIES
    env.libs = libs = []     
# SDK 
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "common"), join(env.framework_dir, "pico-sdk", "src", "common") ))
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "rp2_common"), join(env.framework_dir, "pico-sdk", "src", "rp2_common"),
        src_filter=[ "+<*>", 
            "-<boot_stage2>", 
            "-<pico_standard_link/crt0.S>"
            "-<pico_stdio_usb>",
            "-<pico_fix>",
        ]
    )) 
# PROJECT-LIB    
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "src", "_project"), join("$PROJECT_DIR", "lib") ) )    
# COMMON
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "common", "pico"), join(env.framework_dir, "common", "pico") ) )  
    add_boot(env)
    add_usb(env)
# LIBS    
    add_freeRTOS(env)

    env.Append(LIBS = libs)  
    set_bynary_type(env)