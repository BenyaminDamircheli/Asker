import os 
import yaml

class Config:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/asker")
        self.config_file = os.path.join(self.config_dir, "config.yaml")
        self.default_config = {
            "model": "OpenAI"
        }

    def load_config(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.isfile(self.config_file):
            with open(self.config_file, "w") as file:
                yaml.dump(self.default_config, file, default_flow_style=False)
        with open(self.config_file, "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config
    
    def save_config(self, config):
        with open(self.config_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False)