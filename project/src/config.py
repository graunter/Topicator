import yaml
from pathlib import Path

from constants import CONFIG_FILE

class MyConfig:

    def __init__(self, CfgFile = CONFIG_FILE) -> None:
        
        p = Path(__file__).with_name(CfgFile)

        with p.open("r") as f:
            CfgData = yaml.safe_load(f)

        self.host = CfgData["broker"]["host"]
        self.port = CfgData["broker"]["port"]
        self.topics = {}
        for item in CfgData["topics"]:
            self.topics[item["In"]] = item["Out"]