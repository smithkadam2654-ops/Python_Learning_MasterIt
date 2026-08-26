import random

def main():
    # 1. Generate a random float between 0.0 and 1.0
    rand_float = random.random()
    print(f"Random float: {rand_float}")

    # 2. Generate a random integer between a range (inclusive)
    rand_int = random.randint(1, 100)
    print(f"Random integer (1-100): {rand_int}")

    # 3. Choose a random element from a list
    colors = ["Red", "Blue", "Green", "Yellow", "Purple"]
    chosen_color = random.choice(colors)
    print(f"Randomly chosen color: {chosen_color}")

    # 4. Shuffle a list in place
    numbers = [1, 2, 3, 4, 5]
    print(f"Original list: {numbers}")
    random.shuffle(numbers)
    print(f"Shuffled list: {numbers}")

if __name__ == "__main__":
    main()
