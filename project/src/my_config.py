import yaml
from pathlib import Path
from component import CComponent

from constants import CONFIG_FILE

class MyConfig:

    def __init__(self, CfgFile = CONFIG_FILE) -> None:
        
        p = Path(__file__).with_name(CfgFile)

        with p.open("r") as f:
            self.CfgData = yaml.safe_load(f)

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
            