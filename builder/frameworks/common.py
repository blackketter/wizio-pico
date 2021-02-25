# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from SCons.Script import DefaultEnvironment, Builder, ARGUMENTS
import os, json, tempfile, shutil
from os.path import join, normpath, basename
from shutil import copyfile
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
from uf2conv import upload_app

def dev_uploader(target, source, env):
    drive = env.get("UPLOAD_PORT")
    if None == drive:
        drive = env.get("BUILD_DIR") + '/'
    return upload_app(join(env.get("BUILD_DIR"), env.get("PROGNAME")) + '.bin', drive, env.address)

def dev_compiler(env, application_name):
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
        PROGNAME = application_name 
    )
    env.cortex = ["-mcpu=cortex-m0plus", "-mthumb"]

def get_nano(env):
    disable_nano = env.BoardConfig().get("build.disable_nano", "by defaut nano is enabled") 
    nano = [] 
    if disable_nano == "true":
        nano = ["-specs=nano.specs", "-u", "_printf_float", "-u", "_scanf_float" ]       
    return nano   

def add_usb(env):
    if ('0' == env.BoardConfig().get("build.use_usb", "0")) and ("PICO_STDIO_USB" not in env.get("CPPDEFINES")): 
        return
    print('  TINYUSB: IN USE')
    tinyusb_dir = join(env.framework_dir, "pico-sdk", "lib", "tinyusb")
    env.Append(
        CPPDEFINES = [ "CFG_TUSB_MCU=OPT_MCU_RP2040" ],         
        CPPPATH = [
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "tinyusb"),
            join(tinyusb_dir, "src"),
            join(tinyusb_dir, "hw"),             
        ]
    )  
    env.libs.append( 
        env.BuildLibrary( join("$BUILD_DIR", '_' + env.platform, "tinyusb"), 
        join(tinyusb_dir) )
    )

def add_boot(env):
    boot = env.BoardConfig().get("build.boot", "w25q080") # get boot
    print('  BOOT:', boot)  
    env.libs.append( env.BuildLibrary( join("$BUILD_DIR", '_' + env.platform, "common", "boot2"), join(env.framework_dir, "common", "boot2", boot) ) )        

def add_flags(env, optimization = '-Os', heap_size = "2048"):
    print('  HEAP:', heap_size) 
    env.Append(
        ASFLAGS=[ env.cortex, "-x", "assembler-with-cpp" ],        
        CPPDEFINES = [ 
            "PICO_ON_DEVICE=1",
            "PICO_HEAP_SIZE=" + env.BoardConfig().get("build.heap", heap_size)
        ],              
        CFLAGS = [
            env.cortex,
            optimization,                                                       
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
            optimization,            
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
            optimization,    
            "-nostartfiles",   
            "-mno-unaligned-access",
            "-Wall", 
            "-Wfatal-errors",            
            "-fno-use-cxa-atexit",     
            "-fno-zero-initialized-in-bss",                                           
            "-Xlinker", "--gc-sections",                           
            "-Wl,--gc-sections", 
            "--entry=_entry_point", 
            get_nano(env)                      
        ],
        LIBSOURCE_DIRS=[ join(env.framework_dir, "library") ],
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

def set_bynary_type(env):
    env.address = env.BoardConfig().get("build.address", "-") # get uf2 start address
    linker = env.BoardConfig().get("build.linker", "-") # get linker srcipt
    bynary_type = env.BoardConfig().get("build.bynary_type", 'default')
    print('  BINARY TYPE:', bynary_type)
    if 'copy_to_ram' == bynary_type:
        if '-' == env.address: env.address = '0x10000000'               
        if '-' == linker: linker = 'memmap_copy_to_ram.ld'          
        env.Append(
            LDSCRIPT_PATH = join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
            CPPDEFINES = ['PICO_COPY_TO_RAM']
        )  
    elif 'no_flash' == bynary_type:
        if '-' == env.address: env.address = '0x20000000'               
        if '-' == linker: linker = 'memmap_no_flash.ld'          
        env.Append(
            LDSCRIPT_PATH = join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
            CPPDEFINES = ['PICO_NO_FLASH']
        )          
        pass
    #elif 'blocked_ram' == bynary_type: # ?????????   
    else: #default  
        if '-' == env.address: env.address = '0x10000000'               
        if '-' == linker: linker = 'memmap_default.ld'        
        env.Append(
            LDSCRIPT_PATH = join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", linker),
        )        
    print('  LINKER:', linker)
    print('  ADDRESS:', env.address)

def include_common(env):
    env.Append(      
        CPPPATH = [    
            join(env.framework_dir, "common"),         
            join(env.framework_dir, "pico-sdk", "src", "rp2040", "hardware_regs", "include"),  
            join(env.framework_dir, "pico-sdk", "src", "rp2040", "hardware_structs", "include"),

            join(env.framework_dir, "pico-sdk", "src", "common", "pico_binary_info", "include"), 
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_base", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_stdlib", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_time", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_bit_ops", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_divider", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_sync", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_util", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "boot_picoboot", "include"),
            join(env.framework_dir, "pico-sdk", "src", "common", "boot_uf2", "include"),

            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_bit_ops", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_bootrom", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_cxx_options", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_divider", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_double", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_fix", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_float", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_int64_ops", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_malloc", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_mem_ops", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_multicore", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_platform", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_printf", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_runtime", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_standard_link", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio", "include"),            
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_semihosting", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_uart", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdio_usb", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_stdlib", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_unique_id", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_fix", "rp2040_usb_device_enumeration", "include"),

            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_adc", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_base", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_claim", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_clocks", "include"),     
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_divider", "include"),        
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_dma", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_flash", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_gpio", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_i2c", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_interp", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_irq", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pio", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pll", "include"),            
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_pwm", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_resets", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_rtc", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_spi", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_sync", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_timer", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_uart", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_vreg", "include"),            
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_watchdog", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "hardware_xosc", "include"),
        ],                       
    )    


