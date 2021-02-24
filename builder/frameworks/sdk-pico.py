# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/

import os
from os.path import join
from shutil import copyfile
from SCons.Script import DefaultEnvironment, Builder
from uf2conv import upload_app

def dev_uploader(target, source, env):
    drive = env.get("UPLOAD_PORT")
    if None == drive:
        drive = env.get("BUILD_DIR") + '/'
    return upload_app(join(env.get("BUILD_DIR"), env.get("PROGNAME")) + '.bin', drive, env.address)

def dev_create_template(env):
    D = join(env.subst("$PROJECT_DIR"), "src")
    S = join(env.PioPlatform().get_package_dir("framework-wizio-pico"), "templates", env.BoardConfig().get("build.core"))
    if False == os.path.isfile( join(D, "main.c") ) and False == os.path.isfile( join(D, "main.cpp") ):
        copyfile( join(S, "main.c"), join(D, "main.c") ) 
                
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
        PROGNAME = "BAREMETAL" 
    )
    env.cortex = ["-mcpu=cortex-m0plus", "-mthumb"]

def dev_init(env, platform):
    print( "RASPBERRYPI PI PICO RP2040 PICO-SDK")    
    dev_create_template(env)
    dev_compiler(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    tinyusb_dir = join(framework_dir, "pico-sdk", "lib", "tinyusb")    

    use_usb = env.BoardConfig().get("build.use_usb", "0")       # compile tiniusb
    heap = env.BoardConfig().get("build.heap", "2048")          # default heap size in platform_defs.h
    boot = env.BoardConfig().get("build.boot", "w25q080")       # get boot
    linker = env.BoardConfig().get("build.linker", "-")         # get linker srcipt
    env.address = env.BoardConfig().get("build.address", "-")   # get appstartaddr

    disable_nano = env.BoardConfig().get("build.disable_nano", "by defaut nano is enabled") 
    if disable_nano == "true":
        nano = ["-specs=nano.specs", "-u", "_printf_float", "-u", "_scanf_float" ]
    else: 
        nano = []

    print('  HEAP SIZE:', heap)

    env.Append(
        ASFLAGS=[ env.cortex, "-x", "assembler-with-cpp" ],        
        CPPDEFINES = [                         
            platform.upper(), 
            "PICO_STDIO_UART",
            "PICO_ON_DEVICE=1",
            "PICO_HEAP_SIZE=" + heap,
            "CFG_TUSB_MCU=OPT_MCU_RP2040"
        ],        
        CPPPATH = [    
            join(framework_dir, "common"),        
            join(framework_dir, "pico-sdk", "src", "boards", "include"), 
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
            join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_fix", "rp2040_usb_device_enumeration", "include"),

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

            join(framework_dir, "pico-sdk", "src", "rp2_common", "tinyusb"),
            join(tinyusb_dir, "src"),
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
            "-Wstrict-prototypes",
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
        LIBSOURCE_DIRS=[ join(framework_dir, "library") ],
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
# SDK 
    libs.append( env.BuildLibrary( 
        join("$BUILD_DIR", '_' + platform, "common"),      
        join(framework_dir, "pico-sdk", "src", "common") 
    ))
    libs.append( env.BuildLibrary( 
        join("$BUILD_DIR", '_' + platform, "rp2_common"),        
        join(framework_dir, "pico-sdk", "src", "rp2_common"),
        src_filter=[ "+<*>", 
            "-<boot_stage2>", 
            "-<pico_standard_link/crt0.S>"
        ]
    )) 
# PROJECT    
    libs.append( env.BuildLibrary( join("$BUILD_DIR", "_custom"), join("$PROJECT_DIR", "lib") ) )  
# BOOT2
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "boot2"), join(framework_dir, "common", "boot2", boot) ) )
# Missing
    libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "std"), join(framework_dir, "common", "pico") ) )  
# USB
    if '0' != use_usb:
        print('  TINYUSB: in use')
        libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + platform, "tinyusb"), join(tinyusb_dir) ))

    env.Append(LIBS = libs)  

    bynary_type = env.BoardConfig().get("build.bynary_type", 'default')
    print('  BINARY TYPE:', bynary_type)
    if 'copy_to_ram' == bynary_type:
        if '-' == env.address: env.address = '0x10000000'               
        if '-' == linker: linker = 'memmap_copy_to_ram.ld'          
        env.Append(
            LDSCRIPT_PATH = join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
            CPPDEFINES = ['PICO_COPY_TO_RAM']
        )  
    elif 'no_flash' == bynary_type:
        if '-' == env.address: env.address = '0x20000000'               
        if '-' == linker: linker = 'memmap_no_flash.ld'          
        env.Append(
            LDSCRIPT_PATH = join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
            CPPDEFINES = ['PICO_NO_FLASH']
        )          
        pass
    #elif 'blocked_ram' == bynary_type: # ?????????   
    else: #default  
        if '-' == env.address: env.address = '0x10000000'               
        if '-' == linker: linker = 'memmap_default.ld'        
        env.Append(
            LDSCRIPT_PATH = join(framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
        )        
    print('  LINKER:', linker)
    print('  ADDRESS:', env.address)
    print('  BOOT:', boot)
