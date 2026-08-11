#!/usr/bin/env python3
"""
Grade Calculator Program
Calculates student grades based on scores and assigns letter grades
"""

def get_valid_score(prompt):
    """Get a valid test score (0-100) from user input."""
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def calculate_grade(score):
    """Convert numeric score to letter grade."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def main():
    print("=== Grade Calculator ===")
    
    try:
        num_tests = int(input("How many test scores? "))
        
        if num_tests <= 0:
            print("Number of tests must be positive!")
            return
        
        scores = []
        for i in range(num_tests):
            score = get_valid_score(f"Enter score {i + 1}: ")
            scores.append(score)
        
        average = sum(scores) / len(scores)
        letter_grade = calculate_grade(average)
        
        print(f"\nScores: {scores}")
        print(f"Average: {average:.2f}")
        print(f"Letter Grade: {letter_grade}")
        
        # Show individual grades
        print("\nIndividual grades:")
        for i, score in enumerate(scores):
            print(f"  Test {i + 1}: {score:.1f} -> {calculate_grade(score)}")
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()