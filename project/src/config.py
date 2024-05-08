import yaml
from pathlib import Path

from constants import CONFIG_FILE

class MyConfig:

    def __init__(self, CfgFile = CONFIG_FILE) -> None:
        
        p = Path(__file__).with_name(CfgFile)

        with p.open("r") as f:
            CfgData = yaml.safe_load(f)

        self.broker = CfgData["broker"]
        self.topics = CfgData["topics"]