"""
JSON Processor - JSON data processing and manipulation.
Features: Validation, transformation, and querying.
"""

import json
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class JSONPathType(Enum):
    """JSON path types."""
    KEY = "key"
    INDEX = "index"
    WILDCARD = "wildcard"


@dataclass
class JSONPath:
    """JSON path component."""
    path_type: JSONPathType
    value: Any = None


class JSONProcessor:
    """JSON data processor."""
    
    def __init__(self, data: Any = None) -> None:
        """
        Initialize JSON processor.
        
        Args:
            data: Initial JSON data
        """
        self.data = data if data is not None else {}
    
    def load_from_string(self, json_string: str) -> bool:
        """
        Load JSON from string.
        
        Args:
            json_string: JSON string
            
        Returns:
            True if successful
        """
        try:
            self.data = json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False
    
    def load_from_file(self, file_path: str) -> bool:
        """
        Load JSON from file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'r') as f:
                self.data = json.load(f)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def to_string(self, indent: int = 2) -> str:
        """
        Convert to JSON string.
        
        Args:
            indent: Indentation level
            
        Returns:
            JSON string
        """
        return json.dumps(self.data, indent=indent)
    
    def save_to_file(self, file_path: str, indent: int = 2) -> bool:
        """
        Save to JSON file.
        
        Args:
            file_path: Path to save
            indent: Indentation level
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.data, f, indent=indent)
            return True
        except Exception:
            return False
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get value by JSON path.
        
        Args:
            path: JSON path (e.g., "users[0].name")
            default: Default value if not found
            
        Returns:
            Value at path or default
        """
        try:
            components = self._parse_path(path)
            current = self.data
            
            for component in components:
                if component.path_type == JSONPathType.KEY:
                    current = current[component.value]
                elif component.path_type == JSONPathType.INDEX:
                    current = current[component.value]
                elif component.path_type == JSONPathType.WILDCARD:
                    return current  # Return entire array/object
            
            return current
        except (KeyError, IndexError, TypeError):
            return default
    
    def set(self, path: str, value: Any) -> bool:
        """
        Set value by JSON path.
        
        Args:
            path: JSON path
            value: Value to set
            
        Returns:
            True if successful
        """
        try:
            components = self._parse_path(path)
            current = self.data
            
            # Navigate to parent
            for component in components[:-1]:
                if component.path_type == JSONPathType.KEY:
                    current = current[component.value]
                elif component.path_type == JSONPathType.INDEX:
                    current = current[component.value]
            
            # Set value
            last = components[-1]
            if last.path_type == JSONPathType.KEY:
                current[last.value] = value
            elif last.path_type == JSONPathType.INDEX:
                current[last.value] = value
            
            return True
        except (KeyError, IndexError, TypeError):
            return False
    
    def delete(self, path: str) -> bool:
        """
        Delete value by JSON path.
        
        Args:
            path: JSON path
            
        Returns:
            True if successful
        """
        try:
            components = self._parse_path(path)
            current = self.data
            
            # Navigate to parent
            for component in components[:-1]:
                if component.path_type == JSONPathType.KEY:
                    current = current[component.value]
                elif component.path_type == JSONPathType.INDEX:
                    current = current[component.value]
            
            # Delete value
            last = components[-1]
            if last.path_type == JSONPathType.KEY:
                del current[last.value]
            elif last.path_type == JSONPathType.INDEX:
                del current[last.value]
            
            return True
        except (KeyError, IndexError, TypeError):
            return False
    
    def _parse_path(self, path: str) -> List[JSONPath]:
        """Parse JSON path string."""
        components = []
        current = ""
        in_brackets = False
        in_quotes = False
        
        for char in path:
            if char == '"' and not in_brackets:
                in_quotes = not in_quotes
            elif char == '[' and not in_quotes:
                if current:
                    components.append(JSONPath(JSONPathType.KEY, current))
                    current = ""
                in_brackets = True
            elif char == ']' and not in_quotes:
                if current:
                    components.append(JSONPath(JSONPathType.INDEX, int(current)))
                    current = ""
                in_brackets = False
            elif char == '.' and not in_brackets and not in_quotes:
                if current:
                    components.append(JSONPath(JSONPathType.KEY, current))
                    current = ""
            else:
                current += char
        
        if current:
            components.append(JSONPath(JSONPathType.KEY, current))
        
        return components
    
    def query(self, filter_func: Callable[[Any], bool]) -> List[Any]:
        """
        Query JSON data with filter function.
        
        Args:
            filter_func: Filter function
            
        Returns:
            List of matching values
        """
        results = []
        self._query_recursive(self.data, filter_func, results)
        return results
    
    def _query_recursive(self, data: Any, filter_func: Callable, results: List[Any]) -> None:
        """Recursively query data."""
        if filter_func(data):
            results.append(data)
        
        if isinstance(data, dict):
            for value in data.values():
                self._query_recursive(value, filter_func, results)
        elif isinstance(data, list):
            for item in data:
                self._query_recursive(item, filter_func, results)
    
    def transform(self, transform_func: Callable[[Any], Any]) -> None:
        """
        Transform all values in JSON data.
        
        Args:
            transform_func: Transform function
        """
        self.data = self._transform_recursive(self.data, transform_func)
    
    def _transform_recursive(self, data: Any, transform_func: Callable) -> Any:
        """Recursively transform data."""
        if isinstance(data, dict):
            return {k: self._transform_recursive(v, transform_func) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._transform_recursive(item, transform_func) for item in data]
        else:
            return transform_func(data)
    
    def merge(self, other: 'JSONProcessor', overwrite: bool = True) -> None:
        """
        Merge with another JSON processor.
        
        Args:
            other: Other JSON processor
            overwrite: Whether to overwrite existing keys
        """
        self.data = self._merge_recursive(self.data, other.data, overwrite)
    
    def _merge_recursive(self, data1: Any, data2: Any, overwrite: bool) -> Any:
        """Recursively merge data."""
        if isinstance(data1, dict) and isinstance(data2, dict):
            result = data1.copy()
            for key, value in data2.items():
                if key in result:
                    if overwrite:
                        result[key] = self._merge_recursive(result[key], value, overwrite)
                else:
                    result[key] = value
            return result
        elif isinstance(data1, list) and isinstance(data2, list):
            return data1 + data2
        else:
            return data2 if overwrite else data1
    
    def validate_schema(self, schema: Dict) -> bool:
        """
        Validate data against schema.
        
        Args:
            schema: Schema definition
            
        Returns:
            True if valid
        """
        return self._validate_recursive(self.data, schema)
    
    def _validate_recursive(self, data: Any, schema: Any) -> bool:
        """Recursively validate against schema."""
        if isinstance(schema, dict):
            if 'type' in schema:
                expected_type = schema['type']
                if expected_type == 'object':
                    return isinstance(data, dict)
                elif expected_type == 'array':
                    return isinstance(data, list)
                elif expected_type == 'string':
                    return isinstance(data, str)
                elif expected_type == 'number':
                    return isinstance(data, (int, float))
                elif expected_type == 'boolean':
                    return isinstance(data, bool)
            if 'properties' in schema and isinstance(data, dict):
                for key, prop_schema in schema['properties'].items():
                    if key in data:
                        if not self._validate_recursive(data[key], prop_schema):
                            return False
        return True


def main() -> None:
    """Demonstrate JSON processor."""
    
    print("=== JSON Processor Demo ===")
    
    # Create JSON processor
    processor = JSONProcessor()
    
    # Load from string
    json_string = '''
    {
        "users": [
            {"name": "Alice", "age": 30, "city": "NYC"},
            {"name": "Bob", "age": 25, "city": "LA"},
            {"name": "Charlie", "age": 35, "city": "NYC"}
        ],
        "settings": {
            "theme": "dark",
            "notifications": true
        }
    }
    '''
    
    processor.load_from_string(json_string)
    print("Loaded JSON:")
    print(processor.to_string())
    
    # Get values
    print(f"\nGet users[0].name: {processor.get('users[0].name')}")
    print(f"Get settings.theme: {processor.get('settings.theme')}")
    print(f"Get non-existent: {processor.get('nonexistent', 'default')}")
    
    # Set values
    processor.set('users[0].age', 31)
    processor.set('settings.language', 'en')
    print(f"\nAfter setting values:")
    print(f"users[0].age: {processor.get('users[0].age')}")
    print(f"settings.language: {processor.get('settings.language')}")
    
    # Query
    print(f"\nQuery for NYC users:")
    nyc_users = processor.query(lambda x: isinstance(x, dict) and x.get('city') == 'NYC')
    for user in nyc_users:
        print(f"  {user}")
    
    # Transform
    print(f"\nTransform - uppercase all strings:")
    processor.transform(lambda x: x.upper() if isinstance(x, str) else x)
    print(processor.to_string())
    
    # Merge
    print(f"\nMerge with new data:")
    new_data = {"users": [{"name": "David", "age": 28, "city": "Chicago"}]}
    new_processor = JSONProcessor(new_data)
    processor.merge(new_processor)
    print(f"Total users: {len(processor.get('users'))}")
    
    # Validate schema
    print(f"\nSchema validation:")
    schema = {
        "type": "object",
        "properties": {
            "users": {"type": "array"},
            "settings": {"type": "object"}
        }
    }
    print(f"Valid: {processor.validate_schema(schema)}")


if __name__ == "__main__":
    main()
