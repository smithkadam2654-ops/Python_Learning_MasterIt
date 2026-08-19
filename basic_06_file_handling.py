def main():
    filename = "sample_output.txt"
    
    # Writing to a file using 'with' which automatically closes the file
    with open(filename, "w") as file:
        file.write("Hello! This is a sample file.\n")
        file.write("It contains some basic text.")
    print(f"Successfully wrote to {filename}")
    
    # Reading from a file
    print("\nReading contents back:")
    with open(filename, "r") as file:
        content = file.read()
        print(content)

if __name__ == "__main__":
    main()
