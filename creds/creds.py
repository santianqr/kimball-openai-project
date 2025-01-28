import yaml

class Creds:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_database_creds(self):
        return self.config.get('database', {})
    
    def get_openai_creds(self):
        return self.config.get('openai', {})