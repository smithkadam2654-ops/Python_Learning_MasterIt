"""
API Validation Module

This module provides comprehensive API validation utilities including:
- Request validation
- Response validation
- Schema validation
- Data type checking
- Business rule validation
- Rate limiting validation
- Authentication validation
- Input sanitization
- Error handling and reporting
- Validation middleware

All functions include comprehensive docstrings and type hints.
"""

import re
import json
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import hashlib


class ValidationType(Enum):
    """Types of validation."""
    REQUIRED = "required"
    TYPE = "type"
    FORMAT = "format"
    RANGE = "range"
    LENGTH = "length"
    PATTERN = "pattern"
    CUSTOM = "custom"
    BUSINESS = "business"


class DataType(Enum):
    """Data types for validation."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    DATE = "date"
    DATETIME = "datetime"
    EMAIL = "email"
    URL = "url"
    UUID = "uuid"


@dataclass
class ValidationError:
    """Container for validation errors."""
    field: str
    message: str
    validation_type: ValidationType
    value: Any
    constraints: Dict[str, Any]


@dataclass
class ValidationResult:
    """Container for validation results."""
    valid: bool
    errors: List[ValidationError]
    warnings: List[str]
    validated_data: Dict[str, Any]


class SchemaValidator:
    """Schema validation for API requests."""
    
    @staticmethod
    def validate_required(data: Dict[str, Any], 
                        required_fields: List[str]) -> ValidationResult:
        """Validate required fields are present."""
        errors = []
        
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' is required",
                    validation_type=ValidationType.REQUIRED,
                    value=data.get(field),
                    constraints={}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=data
        )
    
    @staticmethod
    def validate_type(data: Dict[str, Any],
                      type_rules: Dict[str, DataType]) -> ValidationResult:
        """Validate field types."""
        errors = []
        
        for field, expected_type in type_rules.items():
            if field not in data:
                continue
            
            value = data[field]
            
            if expected_type == DataType.STRING:
                if not isinstance(value, str):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be a string",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.INTEGER:
                if not isinstance(value, int) or isinstance(value, bool):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be an integer",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.FLOAT:
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be a number",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.BOOLEAN:
                if not isinstance(value, bool):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be a boolean",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.ARRAY:
                if not isinstance(value, list):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be an array",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.OBJECT:
                if not isinstance(value, dict):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be an object",
                        validation_type=ValidationType.TYPE,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.EMAIL:
                if not isinstance(value, str) or not SchemaValidator._is_valid_email(value):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be a valid email",
                        validation_type=ValidationType.FORMAT,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
            
            elif expected_type == DataType.URL:
                if not isinstance(value, str) or not SchemaValidator._is_valid_url(value):
                    errors.append(ValidationError(
                        field=field,
                        message=f"Field '{field}' must be a valid URL",
                        validation_type=ValidationType.FORMAT,
                        value=value,
                        constraints={"expected": expected_type.value}
                    ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=data
        )
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Check if email is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if URL is valid."""
        pattern = r'^https?://(?:[-\w.]|(?:%[0-9a-fA-F]{2}))+'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_range(data: Dict[str, Any],
                       range_rules: Dict[str, Tuple[Any, Any]]) -> ValidationResult:
        """Validate numeric ranges."""
        errors = []
        
        for field, (min_val, max_val) in range_rules.items():
            if field not in data:
                continue
            
            value = data[field]
            
            if not isinstance(value, (int, float)):
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' must be numeric for range validation",
                    validation_type=ValidationType.RANGE,
                    value=value,
                    constraints={"min": min_val, "max": max_val}
                ))
                continue
            
            if value < min_val or value > max_val:
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' must be between {min_val} and {max_val}",
                    validation_type=ValidationType.RANGE,
                    value=value,
                    constraints={"min": min_val, "max": max_val}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=data
        )
    
    @staticmethod
    def validate_length(data: Dict[str, Any],
                       length_rules: Dict[str, Tuple[int, int]]) -> ValidationResult:
        """Validate string/array lengths."""
        errors = []
        
        for field, (min_len, max_len) in length_rules.items():
            if field not in data:
                continue
            
            value = data[field]
            
            if not isinstance(value, (str, list)):
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' must be a string or array for length validation",
                    validation_type=ValidationType.LENGTH,
                    value=value,
                    constraints={"min": min_len, "max": max_len}
                ))
                continue
            
            length = len(value)
            
            if length < min_len or length > max_len:
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' length must be between {min_len} and {max_len}",
                    validation_type=ValidationType.LENGTH,
                    value=value,
                    constraints={"min": min_len, "max": max_len}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=data
        )
    
    @staticmethod
    def validate_pattern(data: Dict[str, Any],
                        pattern_rules: Dict[str, str]) -> ValidationResult:
        """Validate against regex patterns."""
        errors = []
        
        for field, pattern in pattern_rules.items():
            if field not in data:
                continue
            
            value = data[field]
            
            if not isinstance(value, str):
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' must be a string for pattern validation",
                    validation_type=ValidationType.PATTERN,
                    value=value,
                    constraints={"pattern": pattern}
                ))
                continue
            
            if not re.match(pattern, value):
                errors.append(ValidationError(
                    field=field,
                    message=f"Field '{field}' does not match required pattern",
                    validation_type=ValidationType.PATTERN,
                    value=value,
                    constraints={"pattern": pattern}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=data
        )
    
    @staticmethod
    def validate_schema(data: Dict[str, Any],
                        schema: Dict[str, Dict]) -> ValidationResult:
        """Validate data against complete schema."""
        all_errors = []
        all_warnings = []
        
        # Extract validation rules from schema
        required_fields = []
        type_rules = {}
        range_rules = {}
        length_rules = {}
        pattern_rules = {}
        custom_validators = {}
        
        for field, rules in schema.items():
            if "required" in rules and rules["required"]:
                required_fields.append(field)
            if "type" in rules:
                type_rules[field] = DataType(rules["type"])
            if "min" in rules or "max" in rules:
                range_rules[field] = (rules.get("min", float('-inf')), rules.get("max", float('inf')))
            if "min_length" in rules or "max_length" in rules:
                length_rules[field] = (rules.get("min_length", 0), rules.get("max_length", float('inf')))
            if "pattern" in rules:
                pattern_rules[field] = rules["pattern"]
            if "validator" in rules:
                custom_validators[field] = rules["validator"]
        
        # Required fields
        if required_fields:
            required_result = SchemaValidator.validate_required(data, required_fields)
            all_errors.extend(required_result.errors)
        
        # Type validation
        if type_rules:
            type_result = SchemaValidator.validate_type(data, type_rules)
            all_errors.extend(type_result.errors)
        
        # Range validation
        if range_rules:
            range_result = SchemaValidator.validate_range(data, range_rules)
            all_errors.extend(range_result.errors)
        
        # Length validation
        if length_rules:
            length_result = SchemaValidator.validate_length(data, length_rules)
            all_errors.extend(length_result.errors)
        
        # Pattern validation
        if pattern_rules:
            pattern_result = SchemaValidator.validate_pattern(data, pattern_rules)
            all_errors.extend(pattern_result.errors)
        
        # Custom validation
        for field, validator in custom_validators.items():
            if field in data:
                try:
                    is_valid, message = validator(data[field])
                    if not is_valid:
                        all_errors.append(ValidationError(
                            field=field,
                            message=message or f"Field '{field}' failed custom validation",
                            validation_type=ValidationType.CUSTOM,
                            value=data[field],
                            constraints={}
                        ))
                except Exception as e:
                    all_errors.append(ValidationError(
                        field=field,
                        message=f"Custom validation error: {str(e)}",
                        validation_type=ValidationType.CUSTOM,
                        value=data[field],
                        constraints={}
                    ))
        
        return ValidationResult(
            valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            validated_data=data
        )


class RequestValidator:
    """API request validation."""
    
    @staticmethod
    def validate_json_body(body: str) -> ValidationResult:
        """Validate JSON body is valid."""
        try:
            data = json.loads(body)
            return ValidationResult(
                valid=True,
                errors=[],
                warnings=[],
                validated_data=data
            )
        except json.JSONDecodeError as e:
            return ValidationResult(
                valid=False,
                errors=[ValidationError(
                    field="body",
                    message=f"Invalid JSON: {str(e)}",
                    validation_type=ValidationType.FORMAT,
                    value=body,
                    constraints={}
                )],
                warnings=[],
                validated_data={}
            )
    
    @staticmethod
    def validate_headers(headers: Dict[str, str],
                         required_headers: List[str] = None) -> ValidationResult:
        """Validate request headers."""
        errors = []
        
        if required_headers:
            for header in required_headers:
                if header not in headers:
                    errors.append(ValidationError(
                        field=header,
                        message=f"Required header '{header}' is missing",
                        validation_type=ValidationType.REQUIRED,
                        value=None,
                        constraints={}
                    ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=headers
        )
    
    @staticmethod
    def validate_query_params(params: Dict[str, str],
                             allowed_params: List[str] = None) -> ValidationResult:
        """Validate query parameters."""
        errors = []
        warnings = []
        
        if allowed_params:
            for param in params:
                if param not in allowed_params:
                    warnings.append(f"Query parameter '{param}' is not in allowed list")
        
        return ValidationResult(
            valid=True,
            errors=errors,
            warnings=warnings,
            validated_data=params
        )
    
    @staticmethod
    def validate_content_type(content_type: str,
                              allowed_types: List[str]) -> ValidationResult:
        """Validate content type."""
        if content_type in allowed_types:
            return ValidationResult(
                valid=True,
                errors=[],
                warnings=[],
                validated_data={"content_type": content_type}
            )
        
        return ValidationResult(
            valid=False,
            errors=[ValidationError(
                field="content_type",
                message=f"Content type '{content_type}' is not allowed",
                validation_type=ValidationType.FORMAT,
                value=content_type,
                constraints={"allowed": allowed_types}
            )],
            warnings=[],
            validated_data={"content_type": content_type}
        )


class ResponseValidator:
    """API response validation."""
    
    @staticmethod
    def validate_status_code(status_code: int,
                              allowed_codes: List[int] = None) -> ValidationResult:
        """Validate HTTP status code."""
        if allowed_codes and status_code not in allowed_codes:
            return ValidationResult(
                valid=False,
                errors=[ValidationError(
                    field="status_code",
                    message=f"Status code {status_code} is not allowed",
                    validation_type=ValidationType.RANGE,
                    value=status_code,
                    constraints={"allowed": allowed_codes}
                )],
                warnings=[],
                validated_data={"status_code": status_code}
            )
        
        return ValidationResult(
            valid=True,
            errors=[],
            warnings=[],
            validated_data={"status_code": status_code}
        )
    
    @staticmethod
    def validate_response_structure(response_data: Dict[str, Any],
                                    required_fields: List[str]) -> ValidationResult:
        """Validate response has required fields."""
        errors = []
        
        for field in required_fields:
            if field not in response_data:
                errors.append(ValidationError(
                    field=field,
                    message=f"Required field '{field}' is missing from response",
                    validation_type=ValidationType.REQUIRED,
                    value=None,
                    constraints={}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data=response_data
        )
    
    @staticmethod
    def validate_response_data_type(response_data: Dict[str, Any],
                                    field_types: Dict[str, DataType]) -> ValidationResult:
        """Validate response field types."""
        return SchemaValidator.validate_type(response_data, field_types)


class InputSanitizer:
    """Input sanitization for API requests."""
    
    @staticmethod
    def sanitize_string(input_string: str,
                        max_length: int = 1000,
                        remove_html: bool = True,
                        remove_sql: bool = True) -> str:
        """Sanitize string input."""
        if not isinstance(input_string, str):
            return ""
        
        # Truncate length
        if len(input_string) > max_length:
            input_string = input_string[:max_length]
        
        # Remove HTML tags
        if remove_html:
            input_string = re.sub(r'<[^>]+>', '', input_string)
        
        # Remove SQL injection attempts
        if remove_sql:
            input_string = re.sub(r'(\'|\"|;|--|\b(OR|AND|SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b)', 
                               '', input_string, flags=re.IGNORECASE)
        
        # Trim whitespace
        input_string = input_string.strip()
        
        return input_string
    
    @staticmethod
    def sanitize_number(input_value: Any,
                        min_val: Optional[float] = None,
                        max_val: Optional[float] = None) -> float:
        """Sanitize numeric input."""
        try:
            value = float(input_value)
            
            if min_val is not None and value < min_val:
                value = min_val
            if max_val is not None and value > max_val:
                value = max_val
            
            return value
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def sanitize_boolean(input_value: Any) -> bool:
        """Sanitize boolean input."""
        if isinstance(input_value, bool):
            return input_value
        
        if isinstance(input_value, str):
            return input_value.lower() in ['true', '1', 'yes', 'on']
        
        return bool(input_value)
    
    @staticmethod
    def sanitize_array(input_value: Any,
                      max_items: int = 100) -> list:
        """Sanitize array input."""
        if isinstance(input_value, list):
            return input_value[:max_items]
        
        if isinstance(input_value, str):
            # Try to parse as JSON array
            try:
                parsed = json.loads(input_value)
                if isinstance(parsed, list):
                    return parsed[:max_items]
            except:
                return [input_value]
        
        return [input_value]
    
    @staticmethod
    def sanitize_dict(input_value: Any,
                     allowed_keys: List[str] = None) -> Dict:
        """Sanitize dictionary input."""
        if not isinstance(input_value, dict):
            return {}
        
        if allowed_keys:
            return {k: v for k, v in input_value.items() if k in allowed_keys}
        
        return input_value


class RateLimitValidator:
    """Rate limiting validation."""
    
    @staticmethod
    def check_rate_limit(request_data: Dict[str, Any],
                        rate_limit: int,
                        time_window: int = 60,
                        request_history: List[Dict] = None) -> ValidationResult:
        """Check if request is within rate limit."""
        if request_history is None:
            request_history = []
        
        current_time = time.time()
        
        # Remove old requests outside time window
        request_history = [
            req for req in request_history
            if current_time - req.get("timestamp", 0) < time_window
        ]
        
        if len(request_history) >= rate_limit:
            return ValidationResult(
                valid=False,
                errors=[ValidationError(
                    field="rate_limit",
                    message=f"Rate limit exceeded ({rate_limit} requests per {time_window}s)",
                    validation_type=ValidationType.BUSINESS,
                    value=len(request_history),
                    constraints={"limit": rate_limit, "window": time_window}
                )],
                warnings=[],
                validated_data={}
            )
        
        return ValidationResult(
            valid=True,
            errors=[],
            warnings=[],
            validated_data={"requests_in_window": len(request_history)}
        )


class AuthValidator:
    """Authentication validation."""
    
    @staticmethod
    def validate_api_key(api_key: str,
                      min_length: int = 32,
                      max_length: int = 128) -> ValidationResult:
        """Validate API key format."""
        errors = []
        
        if not api_key:
            errors.append(ValidationError(
                field="api_key",
                message="API key is required",
                validation_type=ValidationType.REQUIRED,
                value=api_key,
                constraints={}
            ))
        else:
            length = len(api_key)
            if length < min_length or length > max_length:
                errors.append(ValidationError(
                    field="api_key",
                    message=f"API key must be between {min_length} and {max_length} characters",
                    validation_type=ValidationType.LENGTH,
                    value=api_key,
                    constraints={"min": min_length, "max": max_length}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data={"api_key": api_key}
        )
    
    @staticmethod
    def validate_bearer_token(token: str) -> ValidationResult:
        """Validate Bearer token format."""
        errors = []
        
        if not token:
            errors.append(ValidationError(
                field="authorization",
                message="Bearer token is required",
                validation_type=ValidationType.REQUIRED,
                value=token,
                constraints={}
            ))
        elif not token.startswith("Bearer "):
            errors.append(ValidationError(
                field="authorization",
                message="Authorization header must start with 'Bearer '",
                validation_type=ValidationType.FORMAT,
                value=token,
                constraints={}
            ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data={"token": token.replace("Bearer ", "") if token.startswith("Bearer ") else token}
        )
    
    @staticmethod
    def validate_basic_auth(auth_header: str) -> ValidationResult:
        """Validate Basic Auth header format."""
        errors = []
        
        if not auth_header:
            errors.append(ValidationError(
                field="authorization",
                message="Basic auth header is required",
                validation_type=ValidationType.REQUIRED,
                value=auth_header,
                constraints={}
            ))
        elif not auth_header.startswith("Basic "):
            errors.append(ValidationError(
                field="authorization",
                message="Authorization header must start with 'Basic '",
                validation_type=ValidationType.FORMAT,
                value=auth_header,
                constraints={}
            ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            validated_data={"auth_header": auth_header}
        )


class BusinessRuleValidator:
    """Business rule validation."""
    
    @staticmethod
    def validate_business_rules(data: Dict[str, Any],
                                 rules: Dict[str, Callable]) -> ValidationResult:
        """Validate against custom business rules."""
        errors = []
        warnings = []
        
        for field, rule in rules.items():
            if field not in data:
                continue
            
            try:
                is_valid, message = rule(data[field])
                if not is_valid:
                    errors.append(ValidationError(
                        field=field,
                        message=message or f"Field '{field}' failed business rule validation",
                        validation_type=ValidationType.BUSINESS,
                        value=data[field],
                        constraints={}
                    ))
            except Exception as e:
                errors.append(ValidationError(
                    field=field,
                    message=f"Business rule validation error: {str(e)}",
                    validation_type=ValidationType.BUSINESS,
                    value=data[field],
                    constraints={}
                ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=data
        )


class ValidationMiddleware:
    """Validation middleware for API endpoints."""
    
    def __init__(self):
        """Initialize validation middleware."""
        self.schemas: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, Dict] = {}
        self.request_history: Dict[str, List[Dict]] = {}
    
    def add_schema(self, endpoint: str, schema: Dict[str, Dict]) -> None:
        """Add validation schema for endpoint."""
        self.schemas[endpoint] = schema
    
    def set_rate_limit(self, endpoint: str, limit: int, window: int = 60) -> None:
        """Set rate limit for endpoint."""
        self.rate_limits[endpoint] = {"limit": limit, "window": window}
    
    def validate_request(self, endpoint: str, request_data: Dict[str, Any]) -> ValidationResult:
        """Validate request against schema and rate limits."""
        all_errors = []
        all_warnings = []
        
        # Rate limit check
        if endpoint in self.rate_limits:
            rate_config = self.rate_limits[endpoint]
            rate_result = RateLimitValidator.check_rate_limit(
                request_data,
                rate_config["limit"],
                rate_config["window"],
                self.request_history.get(endpoint, [])
            )
            
            if not rate_result.valid:
                all_errors.extend(rate_result.errors)
                all_warnings.extend(rate_result.warnings)
        
        # Schema validation
        if endpoint in self.schemas:
            schema_result = SchemaValidator.validate_schema(request_data, self.schemas[endpoint])
            all_errors.extend(schema_result.errors)
            all_warnings.extend(schema_result.warnings)
        
        # Record request for rate limiting
        if endpoint in self.rate_limits:
            if endpoint not in self.request_history:
                self.request_history[endpoint] = []
            self.request_history[endpoint].append({
                "timestamp": time.time(),
                "data": request_data
            })
        
        return ValidationResult(
            valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            validated_data=request_data
        )


def validate_custom_field(value: Any) -> Tuple[bool, str]:
    """Example custom validator function."""
    if value is None:
        return False, "Value cannot be None"
    if isinstance(value, str) and len(value) < 3:
        return False, "Value must be at least 3 characters"
    return True, ""


def demonstrate_api_validation():
    """Demonstrate API validation functionality."""
    print("=== API Validation Demonstration ===\n")
    
    # Schema Validation
    print("1. Schema Validation:")
    schema = {
        "username": {
            "required": True,
            "type": "string",
            "min_length": 3,
            "max_length": 20,
            "pattern": r"^[a-zA-Z0-9_]+$"
        },
        "email": {
            "required": True,
            "type": "email"
        },
        "age": {
            "required": True,
            "type": "integer",
            "min": 18,
            "max": 120
        }
    }
    
    validator = SchemaValidator()
    
    valid_data = {"username": "john_doe", "email": "john@example.com", "age": 25}
    invalid_data = {"username": "a", "email": "invalid", "age": 150}
    
    valid_result = validator.validate_schema(valid_data, schema)
    print(f"   Valid data: {valid_result.valid}")
    
    invalid_result = validator.validate_schema(invalid_data, schema)
    print(f"   Invalid data: {invalid_result.valid}")
    print(f"   Errors: {len(invalid_result.errors)}")
    
    # Request Validation
    print("\n2. Request Validation:")
    request_validator = RequestValidator()
    
    headers = {"Content-Type": "application/json", "Authorization": "Bearer token123"}
    header_result = request_validator.validate_headers(headers, ["Content-Type"])
    print(f"   Headers valid: {header_result.valid}")
    
    body = '{"name": "test", "value": 123}'
    body_result = request_validator.validate_json_body(body)
    print(f"   JSON body valid: {body_result.valid}")
    
    # Input Sanitization
    print("\n3. Input Sanitization:")
    sanitizer = InputSanitizer()
    
    dirty_string = "<script>alert('xss')</script> test' OR '1'='1"
    clean_string = sanitizer.sanitize_string(dirty_string)
    print(f"   Sanitized: {clean_string}")
    
    dirty_number = "999999"
    clean_number = sanitizer.sanitize_number(dirty_number, max_val=100)
    print(f"   Sanitized number: {clean_number}")
    
    # Rate Limiting
    print("\n4. Rate Limiting:")
    rate_validator = RateLimitValidator()
    
    # Simulate requests
    history = [{"timestamp": time.time() - i * 10} for i in range(5)]
    rate_result = rate_validator.check_rate_limit({}, 3, 60, history)
    print(f"   Rate limit check: {rate_result.valid}")
    
    # Authentication Validation
    print("\n5. Authentication Validation:")
    auth_validator = AuthValidator()
    
    api_key_result = auth_validator.validate_api_key("valid_api_key_12345678")
    print(f"   API key valid: {api_key_result.valid}")
    
    bearer_result = auth_validator.validate_bearer_token("Bearer valid_token")
    print(f"   Bearer token valid: {bearer_result.valid}")
    
    # Business Rules
    print("\n6. Business Rules:")
    business_validator = BusinessRuleValidator()
    
    rules = {
        "amount": lambda x: (x > 0, "Amount must be positive"),
        "quantity": lambda x: (x >= 1, "Quantity must be at least 1")
    }
    
    business_data = {"amount": 100, "quantity": 5}
    business_result = business_validator.validate_business_rules(business_data, rules)
    print(f"   Business rules valid: {business_result.valid}")
    
    # Validation Middleware
    print("\n7. Validation Middleware:")
    middleware = ValidationMiddleware()
    
    middleware.add_schema("/api/users", schema)
    middleware.set_rate_limit("/api/users", 10, 60)
    
    middleware_result = middleware.validate_request("/api/users", valid_data)
    print(f"   Middleware validation: {middleware_result.valid}")
    
    # Custom Validation
    print("\n8. Custom Validation:")
    custom_valid = validate_custom_field("test")
    print(f"   Custom validator: {custom_valid}")
    
    print("\n=== Demonstration Complete ===")
    print("\nAPI Validation Best Practices:")
    print("- Always validate and sanitize user input")
    print("- Use schema validation for structured data")
    "- Implement rate limiting to prevent abuse")
    "- Validate authentication credentials")
    "- Use strong typing for field validation")
    "- Provide clear error messages for failed validation")
    "- Log validation failures for security monitoring")
    print("- Use HTTPS for all authenticated endpoints")
    "- Implement proper error handling and reporting")
    print("- Consider using validation libraries for complex schemas")


if __name__ == "__main__":
    import time
    demonstrate_api_validation()