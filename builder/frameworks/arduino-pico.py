# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/

import os
from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from uf2conv import upload_app

def dev_uploader(target, source, env):
    return upload_app(join(env.get("BUILD_DIR"), env.get("PROGNAME")) + '.bin', env.get("UPLOAD_PORT"))
               
def dev_compiler(env):
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-none-eabi-ar",
        AS="arm-none-eabi-as",
        CC="arm-none-eabi-gcc",
        GDB="arm-none-eabi-gdb",
        CXX="arm-none-eabi-g++",
        OBJCOPY="arm-none-eabi-objcopy",
        RANLIB="arm-none-eabi-ranlib",
        SIZETOOL="arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".elf", 
        PROGNAME = "ROM" 
    )
    env.cortex = ["-mcpu=cortex-m0plus", "-mthumb"] # float?

def dev_init(env, platform):
    print( "RASPBERRYPI PI PICO RP2040 ARDUINO")    
    dev_compiler(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    core          = env.BoardConfig().get("build.core")  
    variant       = env.BoardConfig().get("build.variant")  
    heap          = env.BoardConfig().get("build.heap", "65536") # default heap size 
    print("Heap Size:", heap)      

    disable_nano = env.BoardConfig().get("build.disable_nano", "by defaut nano is enabled")
    if disable_nano == "true":
        nano = ["-specs=nano.specs", "-u", "_printf_float", "-u", "_scanf_float" ]
    else: 
        nano = []

    boot = env.BoardConfig().get("build.boot", "w25q080") # selecting boot

    tinyusb_dir = join(framework_dir, "pico-sdk", "lib", "tinyusb", "src")

    env.Append(
        ASFLAGS=[ env.cortex, "-x", "assembler-with-cpp" ],        
        CPPDEFINES = [                         
            platform.upper()+"=200",
            #"PICO_FLOAT_SUPPORT_ROM_V1",   # TODO: enable
            #"PICO_DOUBLE_SUPPORT_ROM_V1",  # TODO: enable           
            "PICO_ON_DEVICE=1",
            "PICO_HEAP_SIZE="+heap,
        ],        
        CPPPATH = [            
            join(framework_dir, platform, platform),
            join(framework_dir, platform, "cores", core),
            join(framework_dir, platform, "variants", variant), 

            join(framework_dir, "common"),        
            join(framework_dir, "pico-sdk", "src", "rp2040", "hardware_regs", "include"),  
            join(framework_dir, "pico-sdk", "src", "rp2040", "hardware_structs", "include"),

            join(framework_dir, "pico-sdk", "src", "common", "pico_binary_info", "include"), 
            join(framework_dir, "pico-sdk", "src", "common", "pico_base", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_stdlib", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_time", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_bit_ops", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_divider", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_sync", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "pico_util", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "boot_picoboot", "include"),
            join(framework_dir, "pico-sdk", "src", "common", "boot_uf2", "include"),

            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_bit_ops", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_bootrom", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_cxx_options", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_divider", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_double", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_fix", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_float", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_int64_ops", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_malloc", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_mem_ops", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_multicore", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_platform", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_printf", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_runtime", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio", "include"),            
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_semihosting", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_uart", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_usb", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdlib", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_unique_id", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_fix", "rp2040_usb_device_enumeration","include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "tinyusb"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_adc", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_base", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_claim", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_clocks", "include"),     
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_divider", "include"),        
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_dma", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_flash", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_gpio", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_i2c", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_interp", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_irq", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pio", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pll", "include"),            
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pwm", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_resets", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_rtc", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_spi", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_sync", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_timer", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_uart", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_vreg", "include"),            
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_watchdog", "include"),
            join(framework_dir, "pico-sdk", "src", "rp2_common", "hardware_xosc", "include"),

            join(tinyusb_dir),
            join(tinyusb_dir, "common"),
            join(tinyusb_dir, "hw"),      
        ],        
        CFLAGS = [
            env.cortex,
            "-Os",                                                       
            "-fdata-sections",      
            "-ffunction-sections",              
            "-fno-strict-aliasing",
            "-fno-zero-initialized-in-bss", 
            "-fsingle-precision-constant",                                                 
            "-Wall", 
            "-Wfatal-errors",
            "-Wno-strict-prototypes",
            "-Wno-unused-function",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-unused-value", 
            "-Wno-discarded-qualifiers",    
            "-mno-unaligned-access",                   
        ],     
        CXXFLAGS = [                               
            "-fno-rtti",
            "-fno-exceptions", 
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
            "-fno-threadsafe-statics",
        ], 
        CCFLAGS = [
            env.cortex,
            "-Os",            
            "-fdata-sections",      
            "-ffunction-sections",              
            "-fno-strict-aliasing",
            "-fno-zero-initialized-in-bss",                                                  
            "-Wall", 
            "-Wfatal-errors",
            "-Wno-unused-function",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-unused-value",
            "-mno-unaligned-access",                                                       
        ],                      
        LINKFLAGS = [ 
            env.cortex,
            "-Os",    
            "-nostartfiles",   
            "-mno-unaligned-access",
            "-Wall", 
            "-Wfatal-errors",            
            "-fno-use-cxa-atexit",     
            "-fno-zero-initialized-in-bss",                                           
            "-Xlinker", "--gc-sections",                           
            "-Wl,--gc-sections", 
            "--entry=_entry_point", 
            nano                      
        ],
        LIBSOURCE_DIRS=[ join(framework_dir, platform, "libraries") ],  #arduino libraries 
        LDSCRIPT_PATH = join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", "memmap_default.ld"),  
        LIBS = [],               
        BUILDERS = dict(
            ElfToBin = Builder(
                action = env.VerboseAction(" ".join([
                    "$OBJCOPY",
                    "-O",
                    "binary",
                    "$SOURCES",
                    "$TARGET",
                ]), "Building $TARGET"),
                suffix = ".bin"
            )      
        ), 
        UPLOADCMD = dev_uploader
    )
    
    libs = []   
#ARDUINO  
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_" + platform),  join(framework_dir, platform, platform) ) )     
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_core"),         join(framework_dir, platform, "cores", core) ) )    
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_variant"),      join(framework_dir, platform, "variants", variant) ) )  
# SDK 
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "common"), join(framework_dir, "pico-sdk", "src", "common") ))
    libs.append( env.BuildLibrary( 
        join("$BUILD_DIR", '_' + platform, "rp2_common"),        
        join(framework_dir, "pico-sdk", "src", "rp2_common"),
        src_filter=[ "+<*>", "-<boot_stage2>", "-<pico_standard_link>",
            "-<pico_malloc",
            "-<pico_printf>",
            "-<pico_stdio>",
            "-<pico_stdio_uart>",
            "-<pico_stdio_usb>",
            "-<pico_stdio_semihosting>",
            "-<pico_float>",    # TODO: enable
            "-<pico_double>",   # TODO: enable
        ]
    )) 
# PROJECT    
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_custom"), join("$PROJECT_DIR", "lib") ) )   
# BOOT2 todo: select other
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "boot2"), join(framework_dir, "common", "boot2", boot) ) )
# USB TODO
        
    env.Append(LIBS = libs)   