import platform
import os

def print_system_info():
    print("=" * 45)
    print("             SYSTEM INFORMATION              ")
    print("=" * 45)
    
    # Fetch OS Information
    print(f"Operating System : {platform.system()} {platform.release()}")
    print(f"OS Version       : {platform.version()}")
    print(f"Machine Type     : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Architecture     : {platform.architecture()[0]}")
    
    print("-" * 45)
    
    # Fetch Python Information
    print(f"Python Version   : {platform.python_version()}")
    print(f"Python Compiler  : {platform.python_compiler()}")
    
    print("-" * 45)
    
    # Fetch Environment Details
    try:
        # getlogin() can sometimes fail depending on the environment
        current_user = os.getlogin()
    except Exception:
        current_user = "Unknown"
        
    print(f"Current User     : {current_user}")
    print(f"Current Directory: {os.getcwd()}")
    
    print("=" * 45)

if __name__ == "__main__":
    print_system_info()
