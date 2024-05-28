import yaml
from pathlib import Path
from component import CComponent

from constants import *

from threading import Lock, Thread
import logging
import os

class MySingletone(type):

    _instances = {}
    _lock: Lock = Lock()
  
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
    
class MyConfig(metaclass=MySingletone):

    def __init__(self, CfgFile = CONFIG_FILE) -> None:
        
        logging.debug("Load of configuration" )
        
        golden_p = Path(__file__).with_name(CfgFile)
        system_p = Path( SYSTEM_PATH + COMMON_PATH )/CfgFile
        user_p = Path.home()/COMMON_PATH/CfgFile

        logging.debug('golden file: ' + str(golden_p))
        logging.debug('system file: ' + str(system_p))
        logging.debug('user file: ' + str(user_p))


        if os.path.isfile(golden_p):
            with golden_p.open("r") as golden_f:
                g_CfgData = yaml.safe_load(golden_f)
                self.CfgData = g_CfgData

        if os.path.isfile(system_p):
            with system_p.open("r") as system_f:
                s_CfgData = yaml.safe_load(system_f)
                self.CfgData = g_CfgData | s_CfgData

        if os.path.isfile(user_p):
            with user_p.open("r") as user_f:
                u_CfgData = yaml.safe_load(user_f)
                self.CfgData = self.CfgData | u_CfgData

        self.host = self.CfgData["broker"]["host"]
        self.port = self.CfgData["broker"]["port"]
        self.topics = {}
        for item in self.CfgData["topics"]:
            self.topics[item["In"]] = item["Out"]

    def get_components(self) -> dict[str, CComponent]:
        #total = dict[str, CComponent]
        total = {}
        for item in self.CfgData["topics"]:
            Comp = CComponent(item["In"], item["Out"])
            total[ item["In"] ] = Comp
        
        return total
            