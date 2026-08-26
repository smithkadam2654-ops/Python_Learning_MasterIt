# Type hinting doesn't enforce types at runtime, but helps developers 
# and tools (like IDEs or linters like mypy) catch errors early.

# We can hint what types the arguments should be, and what the function returns
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."

def process_scores(scores: list[int]) -> float:
    # Calculates the average of a list of integers
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def main():
    # Calling our hinted functions
    greeting = greet("Alice", 25)
    print(greeting)
    
    # Python won't crash if we pass the wrong type here, but an IDE would warn us!
    # greeting_wrong = greet(123, "Bob") 

    my_scores = [90, 85, 95, 80]
    avg = process_scores(my_scores)
    print(f"Average score: {avg}")

if __name__ == "__main__":
    main()
