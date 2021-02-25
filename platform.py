##########################################################################
#
# Autor: WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico
# 
##########################################################################

from platform import system
from platformio.managers.platform import PlatformBase
from platformio.util import get_systype

class WiziopicoPlatform(PlatformBase):
    def configure_default_packages(self, variables, targets):       
        return PlatformBase.configure_default_packages(self, variables, targets)

''' TODO
    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get("protocols", [])
        if "tools" not in debug:
            debug["tools"] = {}  
        for link in ("picoprobe-OpenOCD", "UF2-MSD"):
            if link == "picoprobe-OpenOCD":
                debug["tools"]["picoprobe-OpenOCD"] = {}                
            debug["tools"][link]["onboard"] = link in debug.get("onboard_tools", [])
            debug["tools"][link]["default"] = link in debug.get("default_tools", [])
        board.manifest["debug"] = debug      
        return board

    def configure_debug_options(self, initial_debug_options, ide_data):
        debug_options = copy.deepcopy(initial_debug_options)
        server_executable = debug_options["server"]["executable"].lower()
        adapter_speed = initial_debug_options.get("speed")
        if adapter_speed:
            if "openocd" in server_executable:
                debug_options["server"]["arguments"].extend( ["-c", "adapter speed %s" % adapter_speed] )
        return debug_options    
'''        