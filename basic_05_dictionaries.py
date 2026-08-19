def main():
    # A dictionary stores key-value pairs
    person = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }

    print("Accessing dictionary values:")
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    
    print("\nIterating through dictionary:")
    for key, value in person.items():
        print(f"{key.capitalize()}: {value}")

if __name__ == "__main__":
    main()
