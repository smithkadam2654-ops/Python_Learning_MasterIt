"""
Beginner Project 57: Fibonacci Sequence Generator
Generates a Fibonacci sequence up to a specified number of terms.
"""

def generate_fibonacci(terms):
    if terms <= 0:
        return []
    elif terms == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < terms:
        next_number = sequence[-1] + sequence[-2]
        sequence.append(next_number)
        
    return sequence

def main():
    print("Fibonacci Sequence Generator")
    
    try:
        terms = int(input("How many terms do you want to generate? "))
        
        if terms <= 0:
            print("Please enter a positive integer greater than 0.")
            return
            
        fib_seq = generate_fibonacci(terms)
        print(f"\nThe first {terms} terms of the Fibonacci sequence are:")
        print(", ".join(map(str, fib_seq)))
        
    except ValueError:
        print("Invalid input! Please enter a whole number.")

if __name__ == "__main__":
    main()
