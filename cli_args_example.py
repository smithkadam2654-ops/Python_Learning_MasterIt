import argparse
import sys

def main():
    # 1. Initialize the ArgumentParser
    parser = argparse.ArgumentParser(
        description="A simple script that greets a user and optionally shouts."
    )
    
    # 2. Add arguments
    # Positional argument (required)
    parser.add_argument("name", help="The name of the person to greet")
    
    # Optional arguments (flags)
    parser.add_argument("-a", "--age", type=int, help="The age of the person")
    parser.add_argument("-s", "--shout", action="store_true", help="Print the greeting in ALL CAPS")
    
    # 3. Parse the arguments passed from the terminal
    # If the user passes invalid arguments or uses -h/--help, argparse handles it automatically!
    args = parser.parse_args()
    
    # 4. Use the parsed arguments
    greeting = f"Hello, {args.name}!"
    
    if args.age is not None:
        greeting += f" I see you are {args.age} years old."
        
    if args.shout:
        greeting = greeting.upper()
        
    print(greeting)

if __name__ == "__main__":
    # If run without arguments, print a helpful message
    if len(sys.argv) == 1:
        print("Tip: Run this script with '-h' or '--help' to see available options.")
        print("Try running: python cli_args_example.py Alice --age 30 --shout\n")
    
    # Run the main parser
    main()
