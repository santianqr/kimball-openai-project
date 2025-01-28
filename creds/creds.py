import yaml

class creds:
    @classmethod
    def db_creds(cls, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('database', {})
    
    @classmethod
    def openai_config(cls, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('openai', {})
