from pathlib import Path
from bestconfig import Config

class ConfigReader:

    def __init__(self):
        pass

    def read_config(self, key):
        with open(str(Path(__file__).parent.parent) + '/config.yml', 'r') as config:
            data = Config(config.name)
        return(data.get(key))
