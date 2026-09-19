"""
Data Serialization Module

This module provides comprehensive data serialization utilities including:
- JSON serialization and deserialization
- XML parsing and generation
- YAML handling
- TOML configuration management
- INI file operations
- Pickle serialization
- CSV processing
- Protocol Buffers (protobuf) helpers
- Data format conversion
- Custom serializers

Note: This module uses pyyaml for YAML and toml for TOML support.
Install with: pip install pyyaml toml

All functions include comprehensive docstrings and type hints.
"""

import json
import pickle
import csv
import configparser
import base64
import hashlib
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import io


try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


try:
    import toml
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False


class SerializationFormat(Enum):
    """Supported serialization formats."""
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    TOML = "toml"
    INI = "ini"
    PICKLE = "pickle"
    CSV = "csv"
    PROTOBUF = "protobuf"


@dataclass
class SerializationResult:
    """Container for serialization results."""
    success: bool
    data: Any
    format: SerializationFormat
    size: int
    error_message: Optional[str] = None


class JSONSerializer:
    """JSON serialization utilities."""
    
    @staticmethod
    def serialize(data: Any, indent: int = 2, 
                 ensure_ascii: bool = False) -> str:
        """Serialize data to JSON string."""
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=str)
    
    @staticmethod
    def deserialize(json_string: str) -> Any:
        """Deserialize JSON string to Python object."""
        return json.loads(json_string)
    
    @staticmethod
    def save_to_file(data: Any, file_path: str, 
                     indent: int = 2) -> bool:
        """Save data to JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=str)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Any]:
        """Load data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None
    
    @staticmethod
    def validate_json(json_string: str) -> bool:
        """Validate JSON string."""
        try:
            json.loads(json_string)
            return True
        except:
            return False
    
    @staticmethod
    def pretty_print(data: Any) -> str:
        """Pretty print JSON data."""
        return json.dumps(data, indent=2, default=str)


class XMLHandler:
    """XML parsing and generation utilities."""
    
    @staticmethod
    def dict_to_xml(data: Dict, root_tag: str = "root") -> str:
        """Convert dictionary to XML string."""
        def build_xml(element, parent=None):
            if isinstance(element, dict):
                xml_str = ""
                for key, value in element.items():
                    if isinstance(value, (list, tuple)):
                        for item in value:
                            xml_str += f"<{key}>{build_xml(item)}</{key}>"
                    else:
                        xml_str += f"<{key}>{build_xml(value)}</{key}>"
                return xml_str
            elif isinstance(element, (list, tuple)):
                return "".join(build_xml(item) for item in element)
            else:
                return str(element)
        
        xml_content = build_xml(data)
        return f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<{root_tag}>{xml_content}</{root_tag}>"
    
    @staticmethod
    def xml_to_dict(xml_string: str) -> Dict:
        """Parse XML string to dictionary (simplified)."""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_string)
            
            def element_to_dict(element):
                result = {}
                
                # Handle attributes
                if element.attrib:
                    result.update(element.attrib)
                
                # Handle children
                children = list(element)
                if children:
                    child_dict = {}
                    for child in children:
                        child_data = element_to_dict(child)
                        
                        if child.tag in child_dict:
                            if not isinstance(child_dict[child.tag], list):
                                child_dict[child.tag] = [child_dict[child.tag]]
                            child_dict[child.tag].append(child_data)
                        else:
                            child_dict[child.tag] = child_data
                    
                    result.update(child_dict)
                
                # Handle text content
                if element.text and element.text.strip():
                    if children:
                        result["#text"] = element.text.strip()
                    else:
                        return element.text.strip()
                
                return result
            
            return {root.tag: element_to_dict(root)}
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return {}
    
    @staticmethod
    def extract_tag(xml_string: str, tag: str) -> List[str]:
        """Extract all occurrences of a specific tag."""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_string)
            
            elements = root.findall(f".//{tag}")
            return [elem.text for elem in elements if elem.text]
        except Exception as e:
            print(f"Error extracting tag: {e}")
            return []


class YAMLHandler:
    """YAML handling utilities."""
    
    @staticmethod
    def serialize(data: Any) -> str:
        """Serialize data to YAML string."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required. Install with: pip install pyyaml")
        
        return yaml.dump(data, default_flow_style=False)
    
    @staticmethod
    def deserialize(yaml_string: str) -> Any:
        """Deserialize YAML string to Python object."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required")
        
        return yaml.safe_load(yaml_string)
    
    @staticmethod
    def save_to_file(data: Any, file_path: str) -> bool:
        """Save data to YAML file."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving YAML: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Any]:
        """Load data from YAML file."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading YAML: {e}")
            return None


class TOMLHandler:
    """TOML configuration management."""
    
    @staticmethod
    def serialize(data: Dict) -> str:
        """Serialize data to TOML string."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required. Install with: pip install toml")
        
        return toml.dumps(data)
    
    @staticmethod
    def deserialize(toml_string: str) -> Dict:
        """Deserialize TOML string to Python dictionary."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required")
        
        return toml.loads(toml_string)
    
    @staticmethod
    def save_to_file(data: Dict, file_path: str) -> bool:
        """Save data to TOML file."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                toml.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving TOML: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Dict]:
        """Load data from TOML file."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except Exception as e:
            print(f"Error loading TOML: {e}")
            return None


class INIHandler:
    """INI file operations."""
    
    @staticmethod
    def save_to_file(data: Dict, file_path: str) -> bool:
        """Save data to INI file."""
        try:
            config = configparser.ConfigParser()
            
            for section, section_data in data.items():
                config[section] = section_data
            
            with open(file_path, 'w', encoding='utf-8') as f:
                config.write(f)
            return True
        except Exception as e:
            print(f"Error saving INI: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Dict]:
        """Load data from INI file."""
        try:
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            
            result = {}
            for section in config.sections():
                result[section] = dict(config[section])
            
            return result
        except Exception as e:
            print(f"Error loading INI: {e}")
            return None
    
    @staticmethod
    def get_value(file_path: str, section: str, key: str,
                  fallback: str = "") -> str:
        """Get specific value from INI file."""
        try:
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            return config.get(section, key, fallback=fallback)
        except Exception as e:
            print(f"Error getting INI value: {e}")
            return fallback


class PickleSerializer:
    """Pickle serialization for Python objects."""
    
    @staticmethod
    def serialize(data: Any) -> bytes:
        """Serialize data to pickle bytes."""
        return pickle.dumps(data)
    
    @staticmethod
    def deserialize(pickle_bytes: bytes) -> Any:
        """Deserialize pickle bytes to Python object."""
        return pickle.loads(pickle_bytes)
    
    @staticmethod
    def save_to_file(data: Any, file_path: str) -> bool:
        """Save data to pickle file."""
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving pickle: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Any]:
        """Load data from pickle file."""
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading pickle: {e}")
            return None


class CSVHandler:
    """CSV processing utilities."""
    
    @staticmethod
    def save_to_file(data: List[Dict], file_path: str,
                    fieldnames: Optional[List[str]] = None) -> bool:
        """Save list of dictionaries to CSV file."""
        try:
            if not data:
                return False
            
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> List[Dict]:
        """Load data from CSV file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []
    
    @staticmethod
    def save_to_file_lists(data: List[List], file_path: str) -> bool:
        """Save list of lists to CSV file."""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error saving CSV lists: {e}")
            return False
    
    @staticmethod
    def load_from_file_lists(file_path: str) -> List[List]:
        """Load data from CSV file as list of lists."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            print(f"Error loading CSV lists: {e}")
            return []


class DataConverter:
    """Data format conversion utilities."""
    
    @staticmethod
    def json_to_xml(json_string: str, root_tag: str = "root") -> str:
        """Convert JSON string to XML."""
        data = json.loads(json_string)
        return XMLHandler.dict_to_xml(data, root_tag)
    
    @staticmethod
    def xml_to_json(xml_string: str) -> str:
        """Convert XML string to JSON."""
        data = XMLHandler.xml_to_dict(xml_string)
        return json.dumps(data, indent=2)
    
    @staticmethod
    def json_to_yaml(json_string: str) -> str:
        """Convert JSON string to YAML."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required")
        
        data = json.loads(json_string)
        return yaml.dump(data, default_flow_style=False)
    
    @staticmethod
    def yaml_to_json(yaml_string: str) -> str:
        """Convert YAML string to JSON."""
        if not YAML_AVAILABLE:
            raise ImportError("pyyaml library is required")
        
        data = yaml.safe_load(yaml_string)
        return json.dumps(data, indent=2)
    
    @staticmethod
    def json_to_toml(json_string: str) -> str:
        """Convert JSON string to TOML."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required")
        
        data = json.loads(json_string)
        return toml.dumps(data)
    
    @staticmethod
    def toml_to_json(toml_string: str) -> str:
        """Convert TOML string to JSON."""
        if not TOML_AVAILABLE:
            raise ImportError("toml library is required")
        
        data = toml.loads(toml_string)
        return json.dumps(data, indent=2)


class CustomSerializer:
    """Custom serialization for complex objects."""
    
    @staticmethod
    def serialize_dataclass(obj: Any) -> Dict:
        """Serialize dataclass to dictionary."""
        if hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        return obj.__dict__
    
    @staticmethod
    def deserialize_dataclass(data: Dict, cls: type) -> Any:
        """Deserialize dictionary to dataclass."""
        return cls(**data)
    
    @staticmethod
    def serialize_datetime(obj: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return obj.isoformat()
    
    @staticmethod
    def deserialize_datetime(date_string: str) -> datetime:
        """Deserialize ISO format string to datetime."""
        return datetime.fromisoformat(date_string)
    
    @staticmethod
    def serialize_binary(data: bytes) -> str:
        """Serialize binary data to base64 string."""
        return base64.b64encode(data).decode()
    
    @staticmethod
    def deserialize_binary(encoded_string: str) -> bytes:
        """Deserialize base64 string to binary data."""
        return base64.b64decode(encoded_string.encode())


class DataValidator:
    """Data validation for serialized data."""
    
    @staticmethod
    def validate_schema(data: Dict, schema: Dict) -> bool:
        """Validate data against schema."""
        for key, expected_type in schema.items():
            if key not in data:
                return False
            
            if not isinstance(data[key], expected_type):
                return False
        
        return True
    
    @staticmethod
    def validate_json_structure(json_string: str, 
                                required_keys: List[str]) -> bool:
        """Validate JSON structure has required keys."""
        try:
            data = json.loads(json_string)
            return all(key in data for key in required_keys)
        except:
            return False
    
    @staticmethod
    def sanitize_data(data: Dict, 
                     sensitive_keys: List[str] = None) -> Dict:
        """Remove sensitive data from dictionary."""
        if sensitive_keys is None:
            sensitive_keys = ["password", "secret", "token", "api_key"]
        
        sanitized = data.copy()
        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***REDACTED***"
        
        return sanitized


class DataCompressor:
    """Data compression utilities."""
    
    @staticmethod
    def compress_string(data: str) -> bytes:
        """Compress string using zlib."""
        import zlib
        return zlib.compress(data.encode())
    
    @staticmethod
    def decompress_string(compressed_data: bytes) -> str:
        """Decompress zlib compressed string."""
        import zlib
        return zlib.decompress(compressed_data).decode()
    
    @staticmethod
    def calculate_hash(data: Union[str, bytes], 
                      algorithm: str = "sha256") -> str:
        """Calculate hash of data."""
        if isinstance(data, str):
            data = data.encode()
        
        if algorithm == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(data).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(data).hexdigest()
        else:
            return hashlib.sha256(data).hexdigest()


class SerializationManager:
    """High-level serialization management."""
    
    def __init__(self):
        """Initialize serialization manager."""
        self.serializers = {
            SerializationFormat.JSON: JSONSerializer(),
            SerializationFormat.YAML: YAMLHandler() if YAML_AVAILABLE else None,
            SerializationFormat.TOML: TOMLHandler() if TOML_AVAILABLE else None,
            SerializationFormat.INI: INIHandler(),
            SerializationFormat.PICKLE: PickleSerializer(),
            SerializationFormat.CSV: CSVHandler()
        }
    
    def serialize(self, data: Any, format: SerializationFormat,
                 **kwargs) -> SerializationResult:
        """Serialize data using specified format."""
        serializer = self.serializers.get(format)
        
        if serializer is None:
            return SerializationResult(
                success=False,
                data=None,
                format=format,
                size=0,
                error_message=f"Format {format} not available"
            )
        
        try:
            if format == SerializationFormat.JSON:
                result = serializer.serialize(data, **kwargs)
            elif format == SerializationFormat.YAML:
                result = serializer.serialize(data)
            elif format == SerializationFormat.TOML:
                result = serializer.serialize(data)
            else:
                result = str(data)
            
            return SerializationResult(
                success=True,
                data=result,
                format=format,
                size=len(result),
                error_message=None
            )
        except Exception as e:
            return SerializationResult(
                success=False,
                data=None,
                format=format,
                size=0,
                error_message=str(e)
            )
    
    def deserialize(self, data: str, format: SerializationFormat) -> SerializationResult:
        """Deserialize data using specified format."""
        serializer = self.serializers.get(format)
        
        if serializer is None:
            return SerializationResult(
                success=False,
                data=None,
                format=format,
                size=0,
                error_message=f"Format {format} not available"
            )
        
        try:
            if format == SerializationFormat.JSON:
                result = serializer.deserialize(data)
            elif format == SerializationFormat.YAML:
                result = serializer.deserialize(data)
            elif format == SerializationFormat.TOML:
                result = serializer.deserialize(data)
            elif format == SerializationFormat.PICKLE:
                result = serializer.deserialize(data.encode())
            else:
                result = data
            
            return SerializationResult(
                success=True,
                data=result,
                format=format,
                size=len(data),
                error_message=None
            )
        except Exception as e:
            return SerializationResult(
                success=False,
                data=None,
                format=format,
                size=0,
                error_message=str(e)
            )
    
    def save_to_file(self, data: Any, file_path: str,
                    format: SerializationFormat, **kwargs) -> bool:
        """Save data to file using specified format."""
        serializer = self.serializers.get(format)
        
        if serializer is None:
            return False
        
        try:
            if format == SerializationFormat.JSON:
                return serializer.save_to_file(data, file_path, **kwargs)
            elif format == SerializationFormat.YAML:
                return serializer.save_to_file(data, file_path)
            elif format == SerializationFormat.TOML:
                return serializer.save_to_file(data, file_path)
            elif format == SerializationFormat.INI:
                return serializer.save_to_file(data, file_path)
            elif format == SerializationFormat.PICKLE:
                return serializer.save_to_file(data, file_path)
            elif format == SerializationFormat.CSV:
                return serializer.save_to_file(data, file_path, **kwargs)
            else:
                return False
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False
    
    def load_from_file(self, file_path: str,
                      format: SerializationFormat) -> Optional[Any]:
        """Load data from file using specified format."""
        serializer = self.serializers.get(format)
        
        if serializer is None:
            return None
        
        try:
            if format == SerializationFormat.JSON:
                return serializer.load_from_file(file_path)
            elif format == SerializationFormat.YAML:
                return serializer.load_from_file(file_path)
            elif format == SerializationFormat.TOML:
                return serializer.load_from_file(file_path)
            elif format == SerializationFormat.INI:
                return serializer.load_from_file(file_path)
            elif format == SerializationFormat.PICKLE:
                return serializer.load_from_file(file_path)
            elif format == SerializationFormat.CSV:
                return serializer.load_from_file(file_path)
            else:
                return None
        except Exception as e:
            print(f"Error loading from file: {e}")
            return None


def demonstrate_data_serialization():
    """Demonstrate data serialization functionality."""
    print("=== Data Serialization Demonstration ===\n")
    
    # JSON Serialization
    print("1. JSON Serialization:")
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "swimming"],
        "metadata": {"created": "2024-01-01"}
    }
    
    json_string = JSONSerializer.serialize(data)
    print(f"   JSON string: {json_string[:100]}...")
    
    deserialized = JSONSerializer.deserialize(json_string)
    print(f"   Deserialized: {deserialized['name']}")
    
    # XML Handling
    print("\n2. XML Handling:")
    xml_data = {
        "person": {
            "name": "Jane Doe",
            "age": "25",
            "address": {
                "street": "123 Main St",
                "city": "Boston"
            }
        }
    }
    
    xml_string = XMLHandler.dict_to_xml(xml_data, "person")
    print(f"   XML: {xml_string[:150]}...")
    
    xml_dict = XMLHandler.xml_to_dict(xml_string)
    print(f"   Parsed XML: {list(xml_dict.keys())}")
    
    # YAML Handling
    print("\n3. YAML Handling:")
    if YAML_AVAILABLE:
        yaml_string = YAMLHandler.serialize(data)
        print(f"   YAML: {yaml_string[:100]}...")
        
        yaml_data = YAMLHandler.deserialize(yaml_string)
        print(f"   Deserialized YAML: {yaml_data['name']}")
    else:
        print("   Install pyyaml: pip install pyyaml")
    
    # TOML Handling
    print("\n4. TOML Handling:")
    if TOML_AVAILABLE:
        toml_string = TOMLHandler.serialize(data)
        print(f"   TOML: {toml_string[:100]}...")
        
        toml_data = TOMLHandler.deserialize(toml_string)
        print(f"   Deserialized TOML: {toml_data['name']}")
    else:
        print("   Install toml: pip install toml")
    
    # INI Handling
    print("\n5. INI Handling:")
    ini_data = {
        "database": {
            "host": "localhost",
            "port": "5432",
            "name": "mydb"
        },
        "server": {
            "host": "0.0.0.0",
            "port": "8080"
        }
    }
    
    INIHandler.save_to_file(ini_data, "config.ini")
    loaded_ini = INIHandler.load_from_file("config.ini")
    print(f"   Loaded INI: {list(loaded_ini.keys())}")
    
    # Pickle Serialization
    print("\n6. Pickle Serialization:")
    class CustomObject:
        def __init__(self, value):
            self.value = value
            self.timestamp = datetime.now()
    
    obj = CustomObject(42)
    pickle_bytes = PickleSerializer.serialize(obj)
    print(f"   Pickle size: {len(pickle_bytes)} bytes")
    
    restored_obj = PickleSerializer.deserialize(pickle_bytes)
    print(f"   Restored value: {restored_obj.value}")
    
    # CSV Handling
    print("\n7. CSV Handling:")
    csv_data = [
        {"name": "Alice", "age": "25", "city": "NYC"},
        {"name": "Bob", "age": "30", "city": "LA"},
        {"name": "Charlie", "age": "35", "city": "Chicago"}
    ]
    
    CSVHandler.save_to_file(csv_data, "data.csv")
    loaded_csv = CSVHandler.load_from_file("data.csv")
    print(f"   Loaded CSV rows: {len(loaded_csv)}")
    
    # Data Conversion
    print("\n8. Data Conversion:")
    json_data = '{"name": "Test", "value": 123}'
    
    if YAML_AVAILABLE:
        yaml_converted = DataConverter.json_to_yaml(json_data)
        print(f"   JSON to YAML: {yaml_converted[:50]}...")
    
    if TOML_AVAILABLE:
        toml_converted = DataConverter.json_to_toml(json_data)
        print(f"   JSON to TOML: {toml_converted[:50]}...")
    
    # Custom Serialization
    print("\n9. Custom Serialization:")
    @dataclass
    class Person:
        name: str
        age: int
        city: str
    
    person = Person("Alice", 25, "Boston")
    person_dict = CustomSerializer.serialize_dataclass(person)
    print(f"   Dataclass to dict: {person_dict}")
    
    restored_person = CustomSerializer.deserialize_dataclass(person_dict, Person)
    print(f"   Restored person: {restored_person.name}")
    
    # Data Validation
    print("\n10. Data Validation:")
    schema = {"name": str, "age": int, "city": str}
    is_valid = DataValidator.validate_schema(data, schema)
    print(f"   Schema validation: {is_valid}")
    
    sanitized = DataValidator.sanitize_data({"username": "admin", "password": "secret123"})
    print(f"   Sanitized data: {sanitized}")
    
    # Data Compression
    print("\n11. Data Compression:")
    original_string = "This is a test string for compression purposes"
    compressed = DataCompressor.compress_string(original_string)
    print(f"   Original size: {len(original_string)} bytes")
    print(f"   Compressed size: {len(compressed)} bytes")
    
    decompressed = DataCompressor.decompress_string(compressed)
    print(f"   Decompressed: {decompressed[:30]}...")
    
    # Serialization Manager
    print("\n12. Serialization Manager:")
    manager = SerializationManager()
    
    result = manager.serialize(data, SerializationFormat.JSON)
    print(f"   Serialize JSON: {result.success}, size: {result.size}")
    
    # Cleanup
    import os
    for file in ["config.ini", "data.csv"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n=== Demonstration Complete ===")
    print("\nData Serialization Best Practices:")
    print("- Choose appropriate format for your use case")
    print("- JSON is best for web APIs and configuration")
    print("- YAML is human-readable and supports comments")
    print("- TOML is great for configuration files")
    print("- Pickle is Python-specific but powerful")
    print("- CSV is ideal for tabular data")
    print("- Validate data before serialization")
    print("- Handle errors gracefully")
    print("- Consider compression for large datasets")
    print("- Use proper encoding (UTF-8) for text data")


if __name__ == "__main__":
    demonstrate_data_serialization()