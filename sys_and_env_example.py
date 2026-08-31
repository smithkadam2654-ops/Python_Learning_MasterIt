import sys
import os

def explore_system_and_environment():
    print("--- 1. The 'sys' Module ---")
    
    # sys.version gives you the exact Python version you are running
    print(f"Python Version: {sys.version.split()[0]}")
    
    # sys.platform tells you the platform (e.g., 'win32', 'linux', 'darwin')
    print(f"Platform: {sys.platform}")
    
    # sys.path is a list of directories Python searches when you 'import' a module
    print("\nPython Module Search Path (first 3 locations):")
    for path in sys.path[:3]:
        print(f"- {path}")
        
    print("\n--- 2. Environment Variables (os.environ) ---")
    # Environment variables are stored by your Operating System. 
    # They are standard for securely passing secrets (like API keys) to your code.
    
    # Let's set a fake environment variable just for this script's memory
    os.environ['MY_APP_MODE'] = 'development'
    
    # Now let's retrieve it (using .get() prevents crashing if it doesn't exist)
    app_mode = os.environ.get('MY_APP_MODE', 'production (default)')
    secret_key = os.environ.get('API_KEY', 'NOT_FOUND')
    
    print(f"App Mode: {app_mode}")
    print(f"API Key: {secret_key}")
    
    print("\n--- 3. Exiting a Script ---")
    print("This script will now exit with a success code (0).")
    
    # sys.exit(0) signals to the OS that the program finished successfully.
    # Non-zero numbers (like sys.exit(1)) signal an error occurred.
    sys.exit(0)
    
    # Because we exited above, this line will NEVER execute!
    print("You will never see this.")

if __name__ == "__main__":
    explore_system_and_environment()
