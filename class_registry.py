from typing import Dict, Type, Any

class PluginRegistry(type):
    """
    A metaclass that automatically registers any class that uses it.
    This is useful for creating plugin architectures.
    """
    registry: Dict[str, Type] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: Dict[str, Any]):
        # Create the new class
        new_class = super().__new__(mcs, name, bases, namespace)
        
        # We might not want to register the base class itself if it's meant to be abstract
        if name != "BasePlugin":
            mcs.registry[name] = new_class
            print(f"Registered plugin: {name}")
            
        return new_class

class BasePlugin(metaclass=PluginRegistry):
    """Base class for all plugins."""
    def execute(self) -> str:
        raise NotImplementedError("Plugins must implement the execute method.")

# --- Plugin Implementations ---

class DataExportPlugin(BasePlugin):
    def execute(self) -> str:
        return "Exporting data to CSV..."

class ImageProcessingPlugin(BasePlugin):
    def execute(self) -> str:
        return "Applying filters to image..."

class AuthenticationPlugin(BasePlugin):
    def execute(self) -> str:
        return "Authenticating user via OAuth2..."

if __name__ == "__main__":
    print("\n--- Available Plugins ---")
    for name, plugin_cls in PluginRegistry.registry.items():
        print(f"Instantiating {name}...")
        plugin_instance = plugin_cls()
        print(f"Result: {plugin_instance.execute()}")
