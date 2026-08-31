import subprocess
import platform

def run_system_commands():
    print(f"Operating System detected: {platform.system()}\n")
    
    # Decide which command to run based on the OS
    if platform.system() == "Windows":
        command = ["cmd", "/c", "dir"]
        echo_command = ["cmd", "/c", "echo", "Hello from Windows Subprocess!"]
    else:
        command = ["ls", "-l"]
        echo_command = ["echo", "Hello from Unix Subprocess!"]
        
    print("--- 1. Capturing Command Output ---")
    try:
        # Run the command and capture its output (stdout)
        result = subprocess.run(
            echo_command, 
            capture_output=True, 
            text=True, # Decode bytes to string
            check=True # Raise an exception if the command fails
        )
        print("Output captured by Python:")
        print(result.stdout.strip())
        
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code: {e.returncode}")
        
    print("\n--- 2. Running a Command directly ---")
    print("Running directory listing:")
    # If we don't capture_output, it prints directly to the console
    subprocess.run(command)
    
if __name__ == "__main__":
    run_system_commands()
