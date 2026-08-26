def write_and_read_file(filename):
    # Writing to a file
    with open(filename, 'w') as file:
        file.write("Hello, World!\n")
        file.write("This is a simple file I/O example in Python.\n")
    print(f"Successfully wrote to {filename}")

    # Reading from a file
    print("\nReading file contents:")
    with open(filename, 'r') as file:
        for line in file:
            print(line.strip())

if __name__ == "__main__":
    write_and_read_file("sample_output.txt")
