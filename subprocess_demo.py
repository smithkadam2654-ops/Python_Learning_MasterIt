import subprocess
import sys

def demonstrate_subprocess():
    """Demonstrate how to run system commands from Python."""
    
    print("--- Running a simple command ---")
    # Determine the correct command to list directory based on OS
    list_cmd = ["dir"] if sys.platform == "win32" else ["ls", "-la"]
    
    try:
        # run() is the recommended way to invoke subprocesses
        result = subprocess.run(
            list_cmd, 
            capture_output=True, # Capture stdout and stderr
            text=True,           # Return strings instead of bytes
            shell=True if sys.platform == "win32" else False # shell=True needed for 'dir' on Windows
        )
        
        if result.returncode == 0:
            print("Command succeeded! First 150 chars of output:")
            print(result.stdout[:150] + "...")
        else:
            print(f"Command failed with error:\n{result.stderr}")
            
    except Exception as e:
        print(f"An error occurred while running the subprocess: {e}")

if __name__ == "__main__":
    demonstrate_subprocess()
