# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/

import os
from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from uf2conv import upload_app

def dev_create_asm(target, source, env):
    py = join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2", "pad_checksum")
    dir = join(env["BUILD_DIR"], env["PROGNAME"])
    env.Execute("python " + py + " -s 0xffffffff " + dir + ".bin " + dir + ".S") 
    pass
                
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
        PROGNAME = "boot2" 
    )
    env.cortex = ["-mcpu=cortex-m0plus", "-mthumb"]

def dev_init(env, platform):
    print( "RASPBERRYPI PI PICO RP2040 BOOT STAGE 2")    
    dev_compiler(env)
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")

    env.Append(
        ASFLAGS=[ env.cortex, "-x", "assembler-with-cpp" ],        
        CPPDEFINES = [ "PICO_FLASH_SPI_CLKDIV=2"],        
        CPPPATH = [ 
            join(env.framework_dir, "common"),    
            join(env.framework_dir, "pico-sdk", "src", "rp2040", "hardware_regs", "include"),  
            join(env.framework_dir, "pico-sdk", "src", "rp2040", "hardware_structs", "include"),  
            join(env.framework_dir, "pico-sdk", "src", "common", "pico_base", "include"),          
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "pico_platform", "include"),
            join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2", "asminclude"),
        ],        
        CFLAGS = [
            env.cortex,
            "-Os",                                                       
            "-fdata-sections",      
            "-ffunction-sections",                                                            
            "-Wall", 
            "-Wfatal-errors",
            "-Wstrict-prototypes",                  
        ],     
        CXXFLAGS = [], 
        CCFLAGS = [],                      
        LINKFLAGS = [ 
            env.cortex,
            "-Os",    
            "-nostartfiles",   
            "-nostdlib",
            "-Wall", 
            "-Wfatal-errors",                                                     
            "--entry=_stage2_boot"                    
        ],
        LIBSOURCE_DIRS=[],
        LDSCRIPT_PATH = join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2", "boot_stage2.ld"),
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
        UPLOADCMD = dev_create_asm
    )

    libs = []     
    env.Append(LIBS = libs)   

# Select file, Clean, Upload, Get boot2.S from build folder

    env.BuildSources(join("$BUILD_DIR", "BOOT2"), join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2"), src_filter="-<*> +<boot2_w25q080.S>") # is default
    #env.BuildSources(join("$BUILD_DIR", "BOOT2"), join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2"), src_filter="-<*> +<boot2_w25x10cl.S>")
    #env.BuildSources(join("$BUILD_DIR", "BOOT2"), join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2"), src_filter="-<*> +<boot2_is25lp080.S>")
    #env.BuildSources(join("$BUILD_DIR", "BOOT2"), join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2"), src_filter="-<*> +<boot2_generic_03h.S>")
    #env.BuildSources(join("$BUILD_DIR", "BOOT2"), join(env.framework_dir, "pico-sdk", "src", "rp2_common", "boot_stage2"), src_filter="-<*> +<boot2_usb_blinky.S>")    