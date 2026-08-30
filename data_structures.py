def explore_data_structures():
    # Lists and List Comprehensions
    numbers = [1, 2, 3, 4, 5]
    squares = [n**2 for n in numbers]
    print(f"Original numbers: {numbers}")
    print(f"Squares: {squares}")
    
    # Dictionaries
    student_scores = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78
    }
    
    print("\nStudent Scores:")
    for student, score in student_scores.items():
        print(f"{student}: {score}")
        
    # Adding a new entry
    student_scores["David"] = 95
    
    # Filtering a dictionary using dictionary comprehension
    top_students = {name: score for name, score in student_scores.items() if score >= 90}
    print(f"\nTop Students (Score >= 90): {top_students}")

if __name__ == "__main__":
    explore_data_structures()
