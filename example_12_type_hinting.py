from typing import List, Dict, Optional, Union, Callable

# Simple type hints for arguments and return types
def greet_user(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old!"

# Using complex types from the typing module
def process_scores(scores: List[float], student_info: Dict[str, Union[str, int]]) -> Optional[float]:
    """
    Takes a list of floats and a dictionary (with string keys and string/int values).
    Returns an Optional float (either a float or None).
    """
    if not scores:
        return None
    
    average = sum(scores) / len(scores)
    print(f"Processing student: {student_info.get('name', 'Unknown')}")
    return average

# Type hints with callables (functions passed as arguments)
def execute_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    return operation(x, y)

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print(greet_user("Alice", 30))
    
    avg = process_scores(
        scores=[85.5, 92.0, 78.5], 
        student_info={"name": "Bob", "id": 12345}
    )
    print(f"Average score: {avg}")
    
    result = execute_operation(10, 5, add)
    print(f"10 + 5 = {result}")
    
    # Note: Python itself does not enforce these types at runtime!
    # They are used by tools like 'mypy' or your IDE (VSCode/PyCharm) to catch errors early.
