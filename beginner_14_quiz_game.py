def main():
    questions = {
        "What is the capital of France?": "Paris",
        "Who wrote 'Hamlet'?": "William Shakespeare",
        "What is 5 + 7?": "12",
        "What is the largest planet in our solar system?": "Jupiter",
        "Which programming language is this game written in?": "Python"
    }
    
    print("Welcome to the Quiz Game!")
    print("Answer the following questions:\n")
    
    score = 0
    total_questions = len(questions)
    
    for question, correct_answer in questions.items():
        print(question)
        user_answer = input("Your answer: ")
        
        if user_answer.strip().lower() == correct_answer.lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The correct answer was: {correct_answer}\n")
            
    print("--- Quiz Completed ---")
    print(f"Your final score is {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Percentage: {percentage:.2f}%")

if __name__ == "__main__":
    main()
