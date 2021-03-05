# 
##########################################################################
# Autor: WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/
# 
##########################################################################
from __future__ import print_function
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore

env = DefaultEnvironment()
env.Replace(
    CXX="arm-none-eabi-g++",
)

print( '<<<<<<<<<<<< ' + env.BoardConfig().get("name").upper() + " 2021 Georgi Angelov >>>>>>>>>>>>" )

elf = env.BuildProgram()

src = env.ElfToBin( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg = env.Alias( "buildprog", src, [ env.VerboseAction("", "DONE") ] )
AlwaysBuild( prg )

upload = env.Alias("upload", prg, [ 
    env.VerboseAction("$UPLOADCMD", "Uploading..."),
    env.VerboseAction("", "  DONE"),
])
AlwaysBuild( upload )    

Default( prg )
