# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from platformio.builder.tools.piolib import PlatformIOLibBuilder
from common import *
             
def dev_init(env, platform):
    env.platform = platform    
    env.libs = libs = []     
    env.sdk = sdk = env.BoardConfig().get("build.sdk", "SDK")
    print( "RASPBERRYPI PI PICO RP2040 PICO-%s" % env.sdk )    
    dev_compiler(env)
    dev_create_template(env)    
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    optimization_level = env.BoardConfig().get("build.optimization_level", "-Os")
    add_flags(env, optimization = optimization_level) 
    env.Append( 
        CPPDEFINES = [ platform.upper() ],
        CPPPATH    = [ 
            join(env.framework_dir, sdk, "include"), # SDK
            join(env.framework_dir, sdk, "boards"), # BOARDS
        ],       
    )    
# SDK           
    libs.append( env.BuildLibrary( 
        join("$BUILD_DIR", platform, sdk),   
        join(env.framework_dir, sdk),
        src_filter=[ "+<*>", "-<boot_stage2>", 
            "-<pico/pico_standard_link/crt0.S>",
            "-<pico/pico_printf>",            
            "-<pico/pico_stdio_semihosting>",
            "-<pico/pico_stdio_uart>",
            "-<pico/pico_stdio_usb>",
            "-<pico/pico_fix>",           
            "-<pico/pico_float>",  
            "-<pico/pico_double>",
        ]
    )) 
# WIZIO    
    libs.append( env.BuildLibrary(  # crt0.S  syscall.c  
        join("$BUILD_DIR", platform, "wizio", "pico"), 
        join(env.framework_dir, "wizio", "pico") ) )
# FINALIZE        
    add_common(env)
    env.Append(LIBS = libs)  
    set_bynary_type(env)
