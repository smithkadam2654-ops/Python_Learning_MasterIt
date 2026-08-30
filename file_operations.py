import os

def write_and_read_file(filename):
    # Writing to a file
    with open(filename, 'w') as f:
        f.write("This is the first line.\n")
        f.write("Here is the second line.\n")
        f.write("Python makes file I/O easy!\n")
    print(f"Successfully wrote to {filename}")

    # Reading from a file
    print(f"\nReading contents of {filename}:")
    with open(filename, 'r') as f:
        for line_number, line in enumerate(f, 1):
            # strip() removes the trailing newline character
            print(f"Line {line_number}: {line.strip()}")
            
    # Cleaning up
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\nDeleted {filename} to clean up.")

if __name__ == "__main__":
    write_and_read_file("sample_text.txt")
