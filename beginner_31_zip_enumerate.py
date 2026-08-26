def main():
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]

    # 1. Using enumerate()
    # enumerate() gives you both the index and the item while looping
    print("Using enumerate():")
    for index, name in enumerate(names):
        # index + 1 is used to make it 1-based instead of 0-based for display
        print(f"Student {index + 1}: {name}")

    # 2. Using zip()
    # zip() pairs items from multiple iterables (like lists) together
    print("\nUsing zip():")
    for name, score in zip(names, scores):
        print(f"{name} scored {score} points")

    # 3. Combining both
    print("\nCombining enumerate() and zip():")
    for index, (name, score) in enumerate(zip(names, scores)):
        print(f"Row {index}: {name} - {score}")

if __name__ == "__main__":
    main()
