import random
import time

def run_quiz(num_questions=5):
    print(f"--- 🧮 Mental Math Quiz ({num_questions} questions) ---")
    score = 0
    start_time = time.time()
    
    for i in range(num_questions):
        # Generate two random numbers
        num1 = random.randint(2, 20)
        num2 = random.randint(2, 20)
        
        # Pick an operator (+, -, or *)
        operator = random.choice(['+', '-', '*'])
        
        # Calculate the correct answer to check against
        if operator == '+':
            correct_answer = num1 + num2
        elif operator == '-':
            # Swap if num1 is smaller, to avoid negative answers for simplicity
            if num1 < num2:
                num1, num2 = num2, num1
            correct_answer = num1 - num2
        else:
            correct_answer = num1 * num2
            
        print(f"\nQuestion {i+1}: What is {num1} {operator} {num2}?")
        
        try:
            user_answer = int(input("Your answer: "))
            if user_answer == correct_answer:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. The right answer was {correct_answer}.")
        except ValueError:
            print(f"❌ Invalid input (must be a number). The right answer was {correct_answer}.")
            
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "="*30)
    print(f"Quiz Complete! Score: {score}/{num_questions}")
    print(f"Time taken: {total_time:.1f} seconds")
    print("="*30)

if __name__ == "__main__":
    run_quiz()
