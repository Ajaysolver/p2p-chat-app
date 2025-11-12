import json
import os
from typing import Dict, Any

class ConfigLoader:
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found, using defaults")
            return ConfigLoader.get_default_config()
        except json.JSONDecodeError:
            print(f"Invalid config file {config_path}, using defaults")
            return ConfigLoader.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "network": {
                "timeout": 30,
                "max_peers": 50,
                "bootstrap_nodes": ["localhost:8000"]
            },
            "security": {
                "key_size": 2048,
                "encryption_algorithm": "AES",
                "hash_algorithm": "SHA256"
            },
            "logging": {
                "level": "INFO",
                "max_file_size": 10485760,
                "backup_count": 5
            }
        }
