import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """
    A utility class for loading configuration settings from a YAML file.
    """

    @classmethod
    def _load_config(cls, config_file: str = 'config.yaml') -> Dict[str, Any]:
        """
        Loads the YAML configuration file.

        Args:
            config_file (str): Path to the YAML configuration file. Default is 'config.yaml'.

        Returns:
            dict: The parsed configuration data.
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"❌ Configuration file '{config_file}' not found. Please check the path.")
        
        try:
            with config_path.open('r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"⚠️ Error parsing YAML file: {e}. Please check the file format.")

    @classmethod
    def get_database_config(cls, config_file: str = 'config.yaml') -> Dict[str, Any]:
        """
        Retrieves the database configuration from the YAML file.

        Args:
            config_file (str): Path to the YAML configuration file.

        Returns:
            dict: Database configuration settings.
        """
        config = cls._load_config(config_file)
        return config.get('database', {})

    @classmethod
    def get_openai_config(cls, config_file: str = 'config.yaml') -> Dict[str, Any]:
        """
        Retrieves the OpenAI API key from the YAML file.

        Args:
            config_file (str): Path to the YAML configuration file.

        Returns:
            dict: OpenAI API key.
        """
        config = cls._load_config(config_file)
        return config.get('openai', {})
