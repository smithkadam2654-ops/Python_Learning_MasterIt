"""
JSON Parser - JSON data handling and manipulation.
Features: Parsing, validation, querying, and transformation.
"""

import json
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Person:
    """Sample data class for JSON serialization."""
    name: str
    age: int
    email: str
    address: Optional[Dict[str, Any]] = None


class JSONUtils:
    """Utility class for JSON operations."""
    
    @staticmethod
    def parse_json(json_string: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON string to Python dictionary.
        
        Args:
            json_string: JSON string to parse
            
        Returns:
            Parsed dictionary, or None if parsing fails
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
    
    @staticmethod
    def to_json(data: Any, indent: int = 2, sort_keys: bool = False) -> str:
        """
        Convert Python object to JSON string.
        
        Args:
            data: Python object to convert
            indent: Number of spaces for indentation
            sort_keys: Whether to sort dictionary keys
            
        Returns:
            JSON string
        """
        return json.dumps(data, indent=indent, sort_keys=sort_keys)
    
    @staticmethod
    def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON from file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed dictionary, or None if loading fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
            return None
    
    @staticmethod
    def save_json_file(data: Any, file_path: str, indent: int = 2) -> bool:
        """
        Save data to JSON file.
        
        Args:
            data: Python object to save
            file_path: Path to save JSON file
            indent: Number of spaces for indentation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent)
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving JSON file: {e}")
            return False
    
    @staticmethod
    def get_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
        """
        Get value from nested dictionary using dot notation path.
        
        Args:
            data: Dictionary to query
            path: Dot-separated path (e.g., "user.address.city")
            default: Default value if path not found
            
        Returns:
            Value at path, or default if not found
        """
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    @staticmethod
    def set_value(data: Dict[str, Any], path: str, value: Any) -> bool:
        """
        Set value in nested dictionary using dot notation path.
        
        Args:
            data: Dictionary to modify
            path: Dot-separated path (e.g., "user.address.city")
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        keys = path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return True
    
    @staticmethod
    def flatten_json(data: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten nested JSON structure.
        
        Args:
            data: Dictionary to flatten
            parent_key: Parent key for nested items
            sep: Separator for keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(JSONUtils.flatten_json(value, new_key, sep).items())
            elif isinstance(value, list):
                # Handle lists by indexing
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        items.extend(JSONUtils.flatten_json(item, f"{new_key}[{i}]", sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))
            else:
                items.append((new_key, value))
        
        return dict(items)
    
    @staticmethod
    def unflatten_json(data: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
        """
        Unflatten a flattened JSON structure.
        
        Args:
            data: Flattened dictionary
            sep: Separator used in keys
            
        Returns:
            Nested dictionary
        """
        result = {}
        
        for key, value in data.items():
            keys = key.split(sep)
            current = result
            
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
        
        return result
    
    @staticmethod
    def merge_json(*dicts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Multiple JSON dictionaries (deep merge).
        
        Args:
            *dicts: Dictionaries to merge
            
        Returns:
            Merged dictionary
        """
        def deep_merge(base: Dict, update: Dict) -> Dict:
            result = base.copy()
            
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            
            return result
        
        if not dicts:
            return {}
        
        result = dicts[0]
        for d in dicts[1:]:
            result = deep_merge(result, d)
        
        return result
    
    @staticmethod
    def filter_json(data: Dict[str, Any], filter_func: callable) -> Dict[str, Any]:
        """
        Filter JSON dictionary based on a function.
        
        Args:
            data: Dictionary to filter
            filter_func: Function that takes (key, value) and returns bool
            
        Returns:
            Filtered dictionary
        """
        return {k: v for k, v in data.items() if filter_func(k, v)}
    
    @staticmethod
    def search_json(data: Union[Dict, List], search_key: str) -> List[Any]:
        """
        Search for all values with a given key in nested JSON.
        
        Args:
            data: Dictionary or list to search
            search_key: Key to search for
            
        Returns:
            List of values found
        """
        results = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key == search_key:
                    results.append(value)
                results.extend(JSONUtils.search_json(value, search_key))
        elif isinstance(data, list):
            for item in data:
                results.extend(JSONUtils.search_json(item, search_key))
        
        return results
    
    @staticmethod
    def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate JSON data against a simple schema.
        
        Args:
            data: Data to validate
            schema: Schema definition (type checking only)
            
        Returns:
            True if valid, False otherwise
        """
        for key, expected_type in schema.items():
            if key not in data:
                return False
            
            if expected_type == dict and not isinstance(data[key], dict):
                return False
            elif expected_type == list and not isinstance(data[key], list):
                return False
            elif expected_type == str and not isinstance(data[key], str):
                return False
            elif expected_type == int and not isinstance(data[key], int):
                return False
            elif expected_type == float and not isinstance(data[key], (int, float)):
                return False
            elif expected_type == bool and not isinstance(data[key], bool):
                return False
        
        return True


def main() -> None:
    """Demonstrate JSON utilities."""
    
    utils = JSONUtils()
    
    print("=== JSON Parsing ===")
    json_string = '{"name": "Alice", "age": 30, "city": "New York"}'
    parsed = utils.parse_json(json_string)
    print(f"Original: {json_string}")
    print(f"Parsed: {parsed}")
    
    print("\n=== JSON Serialization ===")
    person = Person("Bob", 25, "bob@example.com", {"street": "123 Main St", "city": "Boston"})
    person_dict = asdict(person)
    json_str = utils.to_json(person_dict)
    print(f"Person object: {person}")
    print(f"JSON: {json_str}")
    
    print("\n=== Nested Value Access ===")
    data = {
        "user": {
            "name": "Charlie",
            "contact": {
                "email": "charlie@example.com",
                "phone": "123-456-7890"
            }
        }
    }
    
    print(f"Data: {utils.to_json(data)}")
    print(f"Get user.name: {utils.get_value(data, 'user.name')}")
    print(f"Get user.contact.email: {utils.get_value(data, 'user.contact.email')}")
    print(f"Get nonexistent: {utils.get_value(data, 'user.address', 'N/A')}")
    
    print("\n=== Set Nested Value ===")
    utils.set_value(data, 'user.contact.phone', '987-654-3210')
    print(f"After setting phone: {utils.get_value(data, 'user.contact.phone')}")
    
    print("\n=== Flatten/Unflatten ===")
    nested = {"a": {"b": {"c": 1}}, "d": [2, 3, {"e": 4}]}
    print(f"Original: {nested}")
    flattened = utils.flatten_json(nested)
    print(f"Flattened: {flattened}")
    unflattened = utils.unflatten_json(flattened)
    print(f"Unflattened: {unflattened}")
    
    print("\n=== Merge JSON ===")
    dict1 = {"a": 1, "b": {"x": 10}}
    dict2 = {"b": {"y": 20}, "c": 3}
    merged = utils.merge_json(dict1, dict2)
    print(f"Dict1: {dict1}")
    print(f"Dict2: {dict2}")
    print(f"Merged: {merged}")
    
    print("\n=== Filter JSON ===")
    data = {"name": "David", "age": 35, "email": "david@example.com", "active": True}
    filtered = utils.filter_json(data, lambda k, v: isinstance(v, str))
    print(f"Original: {data}")
    print(f"Filtered (strings only): {filtered}")
    
    print("\n=== Search JSON ===")
    data = {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ],
        "admin": {"id": 0, "name": "Admin"}
    }
    names = utils.search_json(data, "name")
    print(f"All 'name' values: {names}")
    
    print("\n=== Schema Validation ===")
    user_data = {"name": "Eve", "age": 28, "email": "eve@example.com"}
    schema = {"name": str, "age": int, "email": str}
    valid = utils.validate_json_schema(user_data, schema)
    print(f"Data: {user_data}")
    print(f"Valid: {valid}")
    
    invalid_data = {"name": "Frank", "age": "thirty"}
    valid = utils.validate_json_schema(invalid_data, schema)
    print(f"Invalid data: {invalid_data}")
    print(f"Valid: {valid}")


if __name__ == "__main__":
    main()
