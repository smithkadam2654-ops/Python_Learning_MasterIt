import argparse

def demonstrate_argparse():
    """Demonstrate how to parse command line arguments."""
    
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(
        description="A simple script to demonstrate parsing command line arguments."
    )
    
    # 2. Add arguments
    # Positional argument (required)
    parser.add_argument("name", help="The name of the user to greet.")
    
    # Optional argument with a default value
    parser.add_argument("-a", "--age", type=int, help="The age of the user.", default=None)
    
    # Flag argument (True if specified, False otherwise)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    
    # 3. Parse the arguments
    # NOTE: Since we want this to run easily as a demo inside an IDE without passing real args,
    # we'll provide dummy arguments to parse_args() here. 
    # In a real script, you would just call: args = parser.parse_args()
    args = parser.parse_args(["Alice", "--age", "25", "--verbose"])
    
    # 4. Use the arguments
    if args.verbose:
        print("Verbose mode is enabled.")
        print(f"Processing data for user: {args.name}")
        
    print(f"Hello, {args.name}!")
    
    if args.age:
        print(f"You are {args.age} years old.")

if __name__ == "__main__":
    demonstrate_argparse()
