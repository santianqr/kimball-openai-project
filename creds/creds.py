import yaml

class Creds:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def db_creds(self):
        return self.config.get('database', {})
    
    def openai_creds(self):
        return self.config.get('openai', {})