def main():
    # Basic sorting
    numbers = [5, 2, 9, 1, 5, 6]
    print(f"Original: {numbers}")
    
    # sorted() returns a NEW sorted list
    print(f"Sorted ascending: {sorted(numbers)}")
    print(f"Sorted descending: {sorted(numbers, reverse=True)}")
    
    # Using a custom key for sorting
    words = ["banana", "apple", "cherry", "date"]
    
    # By default, strings are sorted alphabetically
    print(f"\nAlphabetical: {sorted(words)}")
    
    # Sort by length using the len() function as the key
    print(f"By length: {sorted(words, key=len)}")
    
    # Sorting a list of dictionaries
    students = [
        {"name": "Alice", "grade": "B", "age": 20},
        {"name": "Bob", "grade": "A", "age": 19},
        {"name": "Charlie", "grade": "C", "age": 21}
    ]
    
    # Sort by age using a lambda function as the key
    sorted_by_age = sorted(students, key=lambda student: student["age"])
    
    print("\nStudents sorted by age:")
    for student in sorted_by_age:
        print(f"{student['name']} - Age {student['age']}")

if __name__ == "__main__":
    main()
