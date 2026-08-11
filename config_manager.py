#!/usr/bin/env python3
"""
Configuration Manager
Handles application configuration with file-based persistence
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        default_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "app_db"
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                return {**default_config, **file_config}
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load config file, using defaults")
                return default_config
        else:
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get all configuration values for a section."""
        return self.config.get(section, {})

if __name__ == "__main__":
    # Test the configuration manager
    config = ConfigManager()
    
    # Get database host
    db_host = config.get('database.host')
    print(f"Database host: {db_host}")
    
    # Get server port
    server_port = config.get('server.port')
    print(f"Server port: {server_port}")
    
    # Set a new value
    config.set('server.debug', True)
    
    # Verify the change
    debug_status = config.get('server.debug')
    print(f"Debug status: {debug_status}")