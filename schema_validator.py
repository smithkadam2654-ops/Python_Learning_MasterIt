"""
Schema Validator - Data validation with schema definitions.
Features: Type checking, field validation, custom validators, and nested schemas.
"""

from typing import Any, Dict, List, Optional, Callable, Type, get_type_hints
from dataclasses import dataclass, field
from enum import Enum


class ValidationError(Exception):
    """Validation error with details."""
    
    def __init__(self, field: str, message: str, value: Any = None) -> None:
        """
        Initialize validation error.
        
        Args:
            field: Field name that failed validation
            message: Error message
            value: Value that failed validation
        """
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"{field}: {message}")


class FieldType(Enum):
    """Field types for validation."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ANY = "any"


@dataclass
class FieldValidator:
    """Field validator definition."""
    field_type: FieldType
    required: bool = True
    default: Any = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[Any]] = None
    custom_validator: Optional[Callable[[Any], bool]] = None
    custom_message: Optional[str] = None
    
    def validate(self, field_name: str, value: Any) -> None:
        """
        Validate a field value.
        
        Args:
            field_name: Name of the field
            value: Value to validate
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if value is None:
            if self.required:
                raise ValidationError(field_name, "Field is required")
            return
        
        # Type validation
        if not self._validate_type(value):
            raise ValidationError(
                field_name, 
                f"Expected {self.field_type.value}, got {type(value).__name__}",
                value
            )
        
        # Length validation for strings and lists
        if self.field_type in (FieldType.STRING, FieldType.LIST):
            if self.min_length is not None and len(value) < self.min_length:
                raise ValidationError(
                    field_name,
                    f"Minimum length is {self.min_length}",
                    value
                )
            if self.max_length is not None and len(value) > self.max_length:
                raise ValidationError(
                    field_name,
                    f"Maximum length is {self.max_length}",
                    value
                )
        
        # Value range validation for numbers
        if self.field_type in (FieldType.INTEGER, FieldType.FLOAT):
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(
                    field_name,
                    f"Minimum value is {self.min_value}",
                    value
                )
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(
                    field_name,
                    f"Maximum value is {self.max_value}",
                    value
                )
        
        # Allowed values validation
        if self.allowed_values is not None and value not in self.allowed_values:
            raise ValidationError(
                field_name,
                f"Must be one of: {self.allowed_values}",
                value
            )
        
        # Custom validator
        if self.custom_validator is not None:
            if not self.custom_validator(value):
                message = self.custom_message or "Custom validation failed"
                raise ValidationError(field_name, message, value)
    
    def _validate_type(self, value: Any) -> bool:
        """Validate value type."""
        if self.field_type == FieldType.ANY:
            return True
        elif self.field_type == FieldType.STRING:
            return isinstance(value, str)
        elif self.field_type == FieldType.INTEGER:
            return isinstance(value, int) and not isinstance(value, bool)
        elif self.field_type == FieldType.FLOAT:
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif self.field_type == FieldType.BOOLEAN:
            return isinstance(value, bool)
        elif self.field_type == FieldType.LIST:
            return isinstance(value, list)
        elif self.field_type == FieldType.DICT:
            return isinstance(value, dict)
        return False


class Schema:
    """Schema definition for data validation."""
    
    def __init__(self) -> None:
        """Initialize schema."""
        self.fields: Dict[str, FieldValidator] = {}
        self.nested_schemas: Dict[str, 'Schema'] = {}
    
    def add_field(self, name: str, validator: FieldValidator) -> 'Schema':
        """
        Add a field to the schema.
        
        Args:
            name: Field name
            validator: Field validator
            
        Returns:
            Self for method chaining
        """
        self.fields[name] = validator
        return self
    
    def add_nested_schema(self, field_name: str, schema: 'Schema') -> 'Schema':
        """
        Add a nested schema.
        
        Args:
            field_name: Field name
            schema: Nested schema
            
        Returns:
            Self for method chaining
        """
        self.nested_schemas[field_name] = schema
        return self
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate data against schema.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate fields
        for field_name, validator in self.fields.items():
            value = data.get(field_name)
            
            # Use default if value is None and default is set
            if value is None and validator.default is not None:
                value = validator.default
            
            try:
                validator.validate(field_name, value)
            except ValidationError as e:
                raise e
        
        # Validate nested schemas
        for field_name, schema in self.nested_schemas.items():
            if field_name in data:
                if not isinstance(data[field_name], dict):
                    raise ValidationError(field_name, "Expected object/dict")
                schema.validate(data[field_name])
        
        return True
    
    def validate_with_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data and apply defaults.
        
        Args:
            data: Data to validate
            
        Returns:
            Validated data with defaults applied
        """
        result = data.copy()
        
        for field_name, validator in self.fields.items():
            if field_name not in result or result[field_name] is None:
                if validator.default is not None:
                    result[field_name] = validator.default
        
        self.validate(result)
        return result


class SchemaBuilder:
    """Builder for creating schemas."""
    
    def __init__(self) -> None:
        """Initialize schema builder."""
        self.schema = Schema()
    
    def string(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add string field."""
        validator = FieldValidator(FieldType.STRING, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def integer(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add integer field."""
        validator = FieldValidator(FieldType.INTEGER, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def float(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add float field."""
        validator = FieldValidator(FieldType.FLOAT, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def boolean(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add boolean field."""
        validator = FieldValidator(FieldType.BOOLEAN, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def list(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add list field."""
        validator = FieldValidator(FieldType.LIST, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def dict(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add dict field."""
        validator = FieldValidator(FieldType.DICT, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def any(self, name: str, required: bool = True, **kwargs) -> 'SchemaBuilder':
        """Add any-type field."""
        validator = FieldValidator(FieldType.ANY, required, **kwargs)
        self.schema.add_field(name, validator)
        return self
    
    def nested(self, field_name: str, schema: Schema) -> 'SchemaBuilder':
        """Add nested schema."""
        self.schema.add_nested_schema(field_name, schema)
        return self
    
    def build(self) -> Schema:
        """Build and return the schema."""
        return self.schema


def main() -> None:
    """Demonstrate schema validator functionality."""
    
    print("=== Basic Schema Validation ===")
    schema = (SchemaBuilder()
              .string("name", required=True, min_length=2, max_length=50)
              .integer("age", required=True, min_value=0, max_value=150)
              .string("email", required=True)
              .build())
    
    valid_data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
    try:
        schema.validate(valid_data)
        print(f"✓ Valid data: {valid_data}")
    except ValidationError as e:
        print(f"✗ Validation error: {e}")
    
    invalid_data = {"name": "A", "age": 200, "email": "test"}
    try:
        schema.validate(invalid_data)
        print(f"✓ Valid data: {invalid_data}")
    except ValidationError as e:
        print(f"✗ Validation error: {e}")
    
    print("\n=== Schema with Defaults ===")
    schema_with_defaults = (SchemaBuilder()
                           .string("name", required=True)
                           .integer("age", required=False, default=18)
                           .boolean("active", required=False, default=True)
                           .build())
    
    partial_data = {"name": "Bob"}
    validated = schema_with_defaults.validate_with_defaults(partial_data)
    print(f"Original: {partial_data}")
    print(f"Validated: {validated}")
    
    print("\n=== Allowed Values ===")
    status_schema = (SchemaBuilder()
                    .string("status", required=True, 
                            allowed_values=["active", "inactive", "pending"])
                    .build())
    
    try:
        status_schema.validate({"status": "active"})
        print("✓ Valid status")
    except ValidationError as e:
        print(f"✗ {e}")
    
    try:
        status_schema.validate({"status": "deleted"})
        print("✓ Valid status")
    except ValidationError as e:
        print(f"✗ {e}")
    
    print("\n=== Custom Validator ===")
    def validate_email(value: str) -> bool:
        """Validate email format."""
        return "@" in value and "." in value.split("@")[-1]
    
    email_schema = (SchemaBuilder()
                   .string("email", required=True, 
                           custom_validator=validate_email,
                           custom_message="Invalid email format")
                   .build())
    
    try:
        email_schema.validate({"email": "valid@example.com"})
        print("✓ Valid email")
    except ValidationError as e:
        print(f"✗ {e}")
    
    try:
        email_schema.validate({"email": "invalid"})
        print("✓ Valid email")
    except ValidationError as e:
        print(f"✗ {e}")
    
    print("\n=== Nested Schema ===")
    address_schema = (SchemaBuilder()
                     .string("street", required=True)
                     .string("city", required=True)
                     .string("zip", required=True, min_length=5, max_length=10)
                     .build())
    
    user_schema = (SchemaBuilder()
                 .string("name", required=True)
                 .nested("address", address_schema)
                 .build())
    
    valid_user = {
        "name": "Charlie",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zip": "12345"
        }
    }
    
    try:
        user_schema.validate(valid_user)
        print(f"✓ Valid user: {valid_user}")
    except ValidationError as e:
        print(f"✗ {e}")
    
    invalid_user = {
        "name": "Charlie",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zip": "12"  # Too short
        }
    }
    
    try:
        user_schema.validate(invalid_user)
        print(f"✓ Valid user: {invalid_user}")
    except ValidationError as e:
        print(f"✗ {e}")


if __name__ == "__main__":
    main()
