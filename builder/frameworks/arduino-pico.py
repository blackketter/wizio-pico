# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

import os
from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from common import *

def dev_init(env, platform):
    env.platform = platform
    print( "RASPBERRYPI PI PICO RP2040 PICO-ARDUINO")    
    dev_compiler(env, 'ARDUINO')
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    core = env.BoardConfig().get("build.core")
    variant= env.BoardConfig().get("build.variant")  
    add_flags(env, optimization = '-Os', heap_size = '65536') # TODO
    include_common(env)
    env.Append(
        CPPDEFINES = [ 
            platform.upper() + "=200",
            #"PICO_FLOAT_SUPPORT_ROM_V1",  # TODO
            #"PICO_DOUBLE_SUPPORT_ROM_V1", # TODO               
        ],
        CPPPATH = [            
            join(env.framework_dir, platform, platform),
            join(env.framework_dir, platform, "cores", core),
            join(env.framework_dir, platform, "variants", variant), 
        ]
    )
# LIBRARIES
    env.libs = libs = []   
#ARDUINO  
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_" + platform),  join(env.framework_dir, platform, platform) ) )     
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_core"),         join(env.framework_dir, platform, "cores", core) ) )    
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_variant"),      join(env.framework_dir, platform, "variants", variant) ) )  
# SDK 
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "common"),     join(env.framework_dir, "pico-sdk", "src", "common") ))
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "rp2_common"), join(env.framework_dir, "pico-sdk", "src", "rp2_common"),
        src_filter=[ "+<*>", 
            "-<boot_stage2>", 
            "-<pico_standard_link>",
            "-<pico_malloc",
            "-<pico_printf>",
            "-<pico_stdio>",
            "-<pico_stdio_uart>",
            "-<pico_stdio_usb>",
            "-<pico_stdio_semihosting>",
            "-<pico_fix>",    #
            "-<pico_float>",  # TODO: enable
            "-<pico_double>", # TODO: enable
        ]
    ))   
# PROJECT-LIB     
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "src", "_project"), join("$PROJECT_DIR", "lib") ) ) 
    add_boot(env)
    add_usb(env)
# LIBS    
    add_freeRTOS(env)    
    
    env.Append(LIBS = libs)  
    set_bynary_type(env)

    #print( env.get("CPPDEFINES") ) 