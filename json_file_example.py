import json

def json_operations():
    filename = 'config.json'
    
    # 1. Writing a Python dictionary to a JSON file
    print(f"--- Writing data to {filename} ---")
    app_config = {
        "app_name": "My Awesome App",
        "version": 2.1,
        "features": {
            "dark_mode": True,
            "auto_save": False
        },
        "supported_languages": ["English", "Spanish", "French"]
    }
    
    # Save the dictionary to the file
    with open(filename, 'w') as file:
        # indent=4 formats the JSON nicely with spaces so it's readable by humans
        json.dump(app_config, file, indent=4)
        
    print("JSON file saved successfully.\n")
    
    # 2. Reading a JSON file back into a Python dictionary
    print(f"--- Reading data from {filename} ---")
    with open(filename, 'r') as file:
        loaded_config = json.load(file)
        
    print(f"Loaded App Name: {loaded_config['app_name']}")
    print(f"Is Dark Mode Enabled? {loaded_config['features']['dark_mode']}")
    print(f"First supported language: {loaded_config['supported_languages'][0]}")

if __name__ == "__main__":
    json_operations()
