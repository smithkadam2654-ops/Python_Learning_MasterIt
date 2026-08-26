import json

def main():
    # 1. Parsing a JSON string into a Python dictionary (Loads)
    json_string = '{"name": "Alice", "age": 30, "city": "New York", "has_pets": false}'
    
    parsed_data = json.loads(json_string)
    print("Parsed JSON data (Dictionary):")
    print(parsed_data)
    print(f"Name: {parsed_data['name']}")

    # 2. Converting a Python dictionary to a JSON string (Dumps)
    python_dict = {
        "title": "Python Basics",
        "author": "John Doe",
        "pages": 150,
        "is_published": True
    }
    
    # indent=4 makes the output pretty and readable
    json_output = json.dumps(python_dict, indent=4)
    print("\nGenerated JSON string:")
    print(json_output)

if __name__ == "__main__":
    main()
