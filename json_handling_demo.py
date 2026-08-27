import json

def demonstrate_json_handling():
    """Demonstrate how to parse JSON strings and write Python objects to JSON."""
    
    # 1. Parsing JSON string to a Python dictionary (Loads)
    json_string = '''
    {
        "name": "Jane Doe",
        "age": 30,
        "is_employed": true,
        "skills": ["Python", "Machine Learning", "SQL"]
    }
    '''
    
    user_data = json.loads(json_string)
    print("Parsed JSON data:")
    print(f"Name: {user_data['name']}")
    print(f"First skill: {user_data['skills'][0]}")
    
    # 2. Converting a Python dictionary to a JSON string (Dumps)
    new_data = {
        "title": "Data Scientist",
        "department": "Analytics",
        "years_active": 5
    }
    
    # Dump with indentation for readability
    json_output = json.dumps(new_data, indent=4)
    print("\nGenerated JSON string:")
    print(json_output)

if __name__ == "__main__":
    demonstrate_json_handling()
