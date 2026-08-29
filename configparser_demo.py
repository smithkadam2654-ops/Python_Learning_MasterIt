import configparser
import os

def demonstrate_configparser():
    """Demonstrate reading and writing INI configuration files."""
    config_file = 'settings.ini'
    config = configparser.ConfigParser()
    
    print("--- 1. Writing a Configuration File ---")
    # Add sections and key-value pairs
    config['DEFAULT'] = {
        'ServerAliveInterval': '45',
        'Compression': 'yes',
        'CompressionLevel': '9'
    }
    
    config['forge.example'] = {
        'User': 'hg'
    }
    
    config['topsecret.server.com'] = {
        'Port': '50022',
        'ForwardX11': 'no'
    }
    
    # Write it out to a file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print(f"Created '{config_file}' successfully.\n")
    
    print("--- 2. Reading a Configuration File ---")
    # Create a new parser instance and read the file
    reader = configparser.ConfigParser()
    reader.read(config_file)
    
    print(f"Sections found: {reader.sections()}")
    
    # Accessing values
    if 'topsecret.server.com' in reader:
        secret_server = reader['topsecret.server.com']
        print("\nTop Secret Server Settings:")
        print(f"Port: {secret_server['Port']}")
        print(f"ForwardX11: {secret_server['ForwardX11']}")
        
        # Notice that DEFAULT values cascade to other sections!
        print(f"Compression (from DEFAULT): {secret_server.get('Compression')}")
        
    # Get values with correct types (e.g., getting an integer or boolean)
    interval = reader.getint('DEFAULT', 'ServerAliveInterval')
    compression = reader.getboolean('DEFAULT', 'Compression')
    print(f"\nParsed integer: {interval} (type: {type(interval)})")
    print(f"Parsed boolean: {compression} (type: {type(compression)})")
    
    # Cleanup
    os.remove(config_file)
    print("\nCleaned up the configuration file.")

if __name__ == "__main__":
    demonstrate_configparser()
