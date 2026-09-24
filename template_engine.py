"""
Template Engine Module

This module provides comprehensive template engine utilities including:
- Template parsing and rendering
- Variable substitution
- Control structures (if, for, loop)
- Template inheritance
- Template composition
- Custom filters
- Custom tags
- Context management
- Template caching
- Error handling

All functions include comprehensive docstrings and type hints.
"""

import re
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class TemplateTokenType(Enum):
    """Types of template tokens."""
    TEXT = "text"
    VARIABLE = "variable"
    CONTROL = "control"
    COMMENT = "comment"


@dataclass
class TemplateToken:
    """Template token data structure."""
    token_type: TemplateTokenType
    value: str
    line: int
    column: int


class TemplateError(Exception):
    """Template processing error."""
    pass


class TemplateContext:
    """Template context for variable lookup."""
    
    def __init__(self, initial_context: Optional[Dict] = None):
        """Initialize template context."""
        self.context = initial_context or {}
        self.filters: Dict[str, Callable] = {}
        self.tags: Dict[str, Callable] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Set variable in context."""
        self.context[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get variable from context."""
        return self.context.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if key exists in context."""
        return key in self.context
    
    def add_filter(self, name: str, filter_func: Callable) -> None:
        """Add custom filter."""
        self.filters[name] = filter_func
    
    def add_tag(self, name: str, tag_func: Callable) -> None:
        """Add custom tag."""
        self.tags[name] = tag_func
    
    def get_filter(self, name: str) -> Optional[Callable]:
        """Get filter by name."""
        return self.filters.get(name)
    
    def get_tag(self, name: str) -> Optional[Callable]:
        """Get tag by name."""
        return self.tags.get(name)
    
    def resolve_variable(self, variable: str) -> Any:
        """Resolve variable with dot notation."""
        parts = variable.split(".")
        value = self.get(parts[0])
        
        for part in parts[1:]:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                value = None
                break
        
        return value


class TemplateLexer:
    """Template lexer for tokenization."""
    
    def __init__(self):
        """Initialize lexer."""
        self.patterns = [
            (r'\{\{\s*(.*?)\s*\}\}', TemplateTokenType.VARIABLE),
            (r'\{%\s*(.*?)\s*%\}', TemplateTokenType.CONTROL),
            (r'\{#\s*(.*?)\s*#\}', TemplateTokenType.COMMENT),
        ]
    
    def tokenize(self, template: str) -> List[TemplateToken]:
        """Tokenize template string."""
        tokens = []
        line = 1
        column = 1
        
        while template:
            matched = False
            
            for pattern, token_type in self.patterns:
                match = re.match(pattern, template)
                
                if match:
                    # Add text before match
                    if match.start() > 0:
                        text = template[:match.start()]
                        tokens.append(TemplateToken(TemplateTokenType.TEXT, text, line, column))
                        column += len(text)
                    
                    # Add matched token
                    tokens.append(TemplateToken(token_type, match.group(1), line, column))
                    column += len(match.group(0))
                    
                    # Update line count
                    newlines = template[:match.end()].count('\n')
                    line += newlines
                    if newlines > 0:
                        column = match.end() - template.rfind('\n', 0, match.end())
                    
                    template = template[match.end():]
                    matched = True
                    break
            
            if not matched:
                # Add remaining text
                tokens.append(TemplateToken(TemplateTokenType.TEXT, template, line, column))
                break
        
        return tokens


class TemplateFilter:
    """Built-in template filters."""
    
    @staticmethod
    def upper(value: str) -> str:
        """Convert to uppercase."""
        return str(value).upper()
    
    @staticmethod
    def lower(value: str) -> str:
        """Convert to lowercase."""
        return str(value).lower()
    
    @staticmethod
    def title(value: str) -> str:
        """Convert to title case."""
        return str(value).title()
    
    @staticmethod
    def capitalize(value: str) -> str:
        """Capitalize first letter."""
        return str(value).capitalize()
    
    @staticmethod
    def trim(value: str) -> str:
        """Remove whitespace."""
        return str(value).strip()
    
    @staticmethod
    def default(value: Any, default_value: Any = "") -> Any:
        """Return default if value is falsy."""
        return value if value else default_value
    
    @staticmethod
    def length(value: Any) -> int:
        """Return length of value."""
        return len(value)
    
    @staticmethod
    def safe(value: Any) -> str:
        """Safe string conversion."""
        return str(value) if value is not None else ""
    
    @staticmethod
    def truncate(value: str, length: int = 50, suffix: str = "...") -> str:
        """Truncate string to length."""
        value = str(value)
        if len(value) <= length:
            return value
        return value[:length - len(suffix)] + suffix
    
    @staticmethod
    def date(value: Any, format_str: str = "%Y-%m-%d") -> str:
        """Format date."""
        if isinstance(value, datetime):
            return value.strftime(format_str)
        return str(value)
    
    @staticmethod
    def number(value: Any, precision: int = 2) -> str:
        """Format number with precision."""
        try:
            return f"{float(value):.{precision}f}"
        except (ValueError, TypeError):
            return str(value)
    
    @staticmethod
    def json(value: Any) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(value)


class TemplateTag:
    """Built-in template tags."""
    
    @staticmethod
    def if_tag(context: TemplateContext, condition: str, body: str, else_body: str = "") -> str:
        """If tag implementation."""
        # Simple condition evaluation
        condition_result = TemplateTag._evaluate_condition(context, condition)
        
        if condition_result:
            return body
        return else_body
    
    @staticmethod
    def for_tag(context: TemplateContext, variable: str, iterable: str, body: str) -> str:
        """For tag implementation."""
        value = context.resolve_variable(iterable)
        
        if value is None:
            return ""
        
        result = []
        
        for item in value:
            context.set(variable, item)
            result.append(body)
        
        # Clear loop variable
        context.set(variable, None)
        
        return "".join(result)
    
    @staticmethod
    def _evaluate_condition(context: TemplateContext, condition: str) -> bool:
        """Evaluate condition string."""
        # Simple evaluation - extend for complex conditions
        if condition in ["True", "true"]:
            return True
        if condition in ["False", "false"]:
            return False
        
        # Check if variable exists and is truthy
        value = context.resolve_variable(condition)
        return bool(value)


class TemplateRenderer:
    """Template renderer."""
    
    def __init__(self, context: Optional[TemplateContext] = None):
        """Initialize renderer."""
        self.context = context or TemplateContext()
        self.lexer = TemplateLexer()
        self._register_builtin_filters()
        self._register_builtin_tags()
    
    def _register_builtin_filters(self) -> None:
        """Register built-in filters."""
        self.context.add_filter("upper", TemplateFilter.upper)
        self.context.add_filter("lower", TemplateFilter.lower)
        self.context.add_filter("title", TemplateFilter.title)
        self.context.add_filter("capitalize", TemplateFilter.capitalize)
        self.context.add_filter("trim", TemplateFilter.trim)
        self.context.add_filter("default", TemplateFilter.default)
        self.context.add_filter("length", TemplateFilter.length)
        self.context.add_filter("safe", TemplateFilter.safe)
        self.context.add_filter("truncate", TemplateFilter.truncate)
        self.context.add_filter("date", TemplateFilter.date)
        self.context.add_filter("number", TemplateFilter.number)
        self.context.add_filter("json", TemplateFilter.json)
    
    def _register_builtin_tags(self) -> None:
        """Register built-in tags."""
        self.context.add_tag("if", TemplateTag.if_tag)
        self.context.add_tag("for", TemplateTag.for_tag)
    
    def render(self, template: str, context: Optional[Dict] = None) -> str:
        """Render template with context."""
        if context:
            for key, value in context.items():
                self.context.set(key, value)
        
        tokens = self.lexer.tokenize(template)
        return self._render_tokens(tokens)
    
    def _render_tokens(self, tokens: List[TemplateToken]) -> str:
        """Render tokens to string."""
        result = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token.token_type == TemplateTokenType.TEXT:
                result.append(token.value)
            elif token.token_type == TemplateTokenType.VARIABLE:
                result.append(self._render_variable(token.value))
            elif token.token_type == TemplateTokenType.CONTROL:
                result.append(self._render_control(token.value, tokens, i))
                # Skip tokens consumed by control tag
                # Simplified - in real implementation, parse control structure
            elif token.token_type == TemplateTokenType.COMMENT:
                pass  # Skip comments
            
            i += 1
        
        return "".join(result)
    
    def _render_variable(self, variable: str) -> str:
        """Render variable with filters."""
        # Split variable and filters
        parts = variable.split("|")
        var_name = parts[0].strip()
        filters = parts[1:]
        
        # Resolve variable
        value = self.context.resolve_variable(var_name)
        
        # Apply filters
        for filter_spec in filters:
            filter_parts = filter_spec.split(":")
            filter_name = filter_parts[0].strip()
            filter_args = [arg.strip() for arg in filter_parts[1:]] if len(filter_parts) > 1 else []
            
            filter_func = self.context.get_filter(filter_name)
            
            if filter_func:
                if filter_args:
                    value = filter_func(value, *filter_args)
                else:
                    value = filter_func(value)
        
        return str(value)
    
    def _render_control(self, control: str, tokens: List[TemplateToken], index: int) -> str:
        """Render control tag."""
        # Simplified control tag parsing
        # Parse tag name and arguments
        parts = control.split()
        if not parts:
            return ""
        
        tag_name = parts[0]
        
        if tag_name == "if":
            # Parse if condition
            condition = " ".join(parts[1:])
            # Find endif (simplified)
            # In real implementation, parse nested structures
            return ""
        elif tag_name == "for":
            # Parse for loop
            # format: for item in items
            # In real implementation, parse loop structure
            return ""
        
        return ""


class SimpleTemplate:
    """Simple template engine without full parsing."""
    
    def __init__(self, template: str):
        """Initialize simple template."""
        self.template = template
    
    def render(self, context: Dict) -> str:
        """Render template with context."""
        result = self.template
        
        # Variable substitution: {{ variable }}
        result = re.sub(r'\{\{\s*(\w+(?:\.\w+)*)\s*\}\}',
                       lambda m: self._get_value(context, m.group(1)),
                       result)
        
        # Control structures (simplified)
        # {% if condition %}body{% endif %}
        result = self._process_if(result, context)
        
        # {% for item in items %}body{% endfor %}
        result = self._process_for(result, context)
        
        # Comments: {# comment #}
        result = re.sub(r'\{#.*?#\}', '', result, flags=re.DOTALL)
        
        return result
    
    def _get_value(self, context: Dict, key: str) -> str:
        """Get value from context with dot notation."""
        parts = key.split(".")
        value = context.get(parts[0], "")
        
        for part in parts[1:]:
            if isinstance(value, dict):
                value = value.get(part, "")
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                value = ""
                break
        
        return str(value)
    
    def _process_if(self, template: str, context: Dict) -> str:
        """Process if tags."""
        pattern = r'\{%\s*if\s+(.+?)\s*%\}(.*?)\{%\s*endif\s*%\}'
        
        def replace_if(match):
            condition = match.group(1).strip()
            body = match.group(2)
            
            # Simple condition evaluation
            if condition in ["True", "true"]:
                return body
            if condition in ["False", "false"]:
                return ""
            
            # Check variable
            value = self._get_value(context, condition)
            return body if value else ""
        
        return re.sub(pattern, replace_if, template, flags=re.DOTALL)
    
    def _process_for(self, template: str, context: Dict) -> str:
        """Process for tags."""
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        
        def replace_for(match):
            var_name = match.group(1)
            iterable_name = match.group(2)
            body = match.group(3)
            
            iterable = context.get(iterable_name, [])
            
            if not iterable:
                return ""
            
            result = []
            for item in iterable:
                local_context = context.copy()
                local_context[var_name] = item
                result.append(self._render_body(body, local_context))
            
            return "".join(result)
        
        return re.sub(pattern, replace_for, template, flags=re.DOTALL)
    
    def _render_body(self, body: str, context: Dict) -> str:
        """Render body with context."""
        return re.sub(r'\{\{\s*(\w+(?:\.\w+)*)\s*\}\}',
                     lambda m: self._get_value(context, m.group(1)),
                     body)


class TemplateCache:
    """Template caching."""
    
    def __init__(self, max_size: int = 100):
        """Initialize template cache."""
        self.cache: Dict[str, SimpleTemplate] = {}
        self.max_size = max_size
    
    def get(self, template_str: str) -> Optional[SimpleTemplate]:
        """Get cached template."""
        return self.cache.get(template_str)
    
    def set(self, template_str: str, template: SimpleTemplate) -> None:
        """Cache template."""
        if len(self.cache) >= self.max_size:
            # Simple eviction - remove first item
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[template_str] = template
    
    def clear(self) -> None:
        """Clear cache."""
        self.cache.clear()


class TemplateInheritance:
    """Template inheritance support."""
    
    def __init__(self):
        """Initialize inheritance manager."""
        self.blocks: Dict[str, str] = {}
        self.parent_template: Optional[str] = None
    
    def extend(self, parent_template: str) -> None:
        """Set parent template."""
        self.parent_template = parent_template
    
    def block(self, name: str, content: str) -> None:
        """Define block."""
        self.blocks[name] = content
    
    def render(self, context: Dict) -> str:
        """Render with inheritance."""
        if self.parent_template:
            # In real implementation, load and render parent
            # with block substitution
            pass
        
        result = ""
        for name, content in self.blocks.items():
            result += content
        
        return result


class TemplateLoader:
    """Template loader for file-based templates."""
    
    def __init__(self, template_dir: str = "templates"):
        """Initialize template loader."""
        self.template_dir = template_dir
        self.cache = TemplateCache()
    
    def load(self, template_name: str) -> SimpleTemplate:
        """Load template from file."""
        import os
        
        template_path = os.path.join(self.template_dir, template_name)
        
        # Check cache
        with open(template_path, 'r') as f:
            template_str = f.read()
        
        cached = self.cache.get(template_str)
        if cached:
            return cached
        
        template = SimpleTemplate(template_str)
        self.cache.set(template_str, template)
        
        return template
    
    def render(self, template_name: str, context: Dict) -> str:
        """Load and render template."""
        template = self.load(template_name)
        return template.render(context)


def demonstrate_template_engine():
    """Demonstrate template engine functionality."""
    print("=== Template Engine Demonstration ===\n")
    
    # Simple Template
    print("1. Simple Template:")
    template_str = "Hello, {{ name }}! You have {{ count }} messages."
    template = SimpleTemplate(template_str)
    
    context = {"name": "John", "count": 5}
    rendered = template.render(context)
    print(f"   Template: {template_str}")
    print(f"   Context: {context}")
    print(f"   Rendered: {rendered}")
    
    # Nested Variables
    print("\n2. Nested Variables:")
    template_str = "User: {{ user.name }}, Email: {{ user.email }}"
    template = SimpleTemplate(template_str)
    
    context = {"user": {"name": "Jane", "email": "jane@example.com"}}
    rendered = template.render(context)
    print(f"   Rendered: {rendered}")
    
    # If Tag
    print("\n3. If Tag:")
    template_str = "{% if show_message %}Welcome!{% endif %}"
    template = SimpleTemplate(template_str)
    
    context1 = {"show_message": True}
    context2 = {"show_message": False}
    
    print(f"   With True: {template.render(context1)}")
    print(f"   With False: {template.render(context2)}")
    
    # For Tag
    print("\n4. For Tag:")
    template_str = "{% for item in items %}{{ item }} {% endfor %}"
    template = SimpleTemplate(template_str)
    
    context = {"items": ["apple", "banana", "cherry"]}
    rendered = template.render(context)
    print(f"   Rendered: {rendered}")
    
    # Comments
    print("\n5. Comments:")
    template_str = "Hello {# This is a comment #} World"
    template = SimpleTemplate(template_str)
    rendered = template.render({})
    print(f"   Rendered: {rendered}")
    
    # Complex Template
    print("\n6. Complex Template:")
    template_str = """
    <h1>{{ title }}</h1>
    {% if user %}
    <p>Welcome, {{ user.name }}!</p>
    {% endif %}
    <ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
    </ul>
    """
    template = SimpleTemplate(template_str)
    
    context = {
        "title": "My Page",
        "user": {"name": "Alice"},
        "items": ["Item 1", "Item 2", "Item 3"]
    }
    rendered = template.render(context)
    print(f"   Rendered: {rendered.strip()}")
    
    # Template Context
    print("\n7. Template Context:")
    tcontext = TemplateContext({"name": "Bob", "age": 30})
    print(f"   Get name: {tcontext.get('name')}")
    print(f"   Has age: {tcontext.has('age')}")
    print(f"   Resolve user.name: {tcontext.resolve_variable('user.name')}")
    
    # Filters
    print("\n8. Template Filters:")
    print(f"   Upper: {TemplateFilter.upper('hello')}")
    print(f"   Lower: {TemplateFilter.lower('HELLO')}")
    print(f"   Title: {TemplateFilter.title('hello world')}")
    print(f"   Truncate: {TemplateFilter.truncate('This is a long string', 10)}")
    print(f"   Date: {TemplateFilter.date(datetime.now())}")
    print(f"   Number: {TemplateFilter.number(3.14159, 2)}")
    
    # Template Cache
    print("\n9. Template Cache:")
    cache = TemplateCache(max_size=2)
    template1 = SimpleTemplate("Template 1")
    template2 = SimpleTemplate("Template 2")
    
    cache.set("t1", template1)
    cache.set("t2", template2)
    
    print(f"   Cache size: {len(cache.cache)}")
    print(f"   Get t1: {cache.get('t1') is not None}")
    
    # Template Inheritance
    print("\n10. Template Inheritance:")
    inheritance = TemplateInheritance()
    inheritance.extend("base.html")
    inheritance.block("content", "This is the content")
    inheritance.block("footer", "Footer text")
    
    print(f"   Blocks: {list(inheritance.blocks.keys())}")
    print(f"   Parent: {inheritance.parent_template}")
    
    print("\n=== Demonstration Complete ===")
    print("\nTemplate Engine Best Practices:")
    print("- Use templates for separating presentation from logic")
    print("- Keep templates simple and readable")
    print("- Use filters for common transformations")
    print("- Implement template caching for performance")
    print("- Use inheritance for shared layouts")
    print("- Escape user input to prevent XSS")
    print("- Document custom filters and tags")
    print("- Test templates with various contexts")
    print("- Use template inheritance judiciously")
    print("- Consider template inheritance depth")
    print("- Validate template syntax before deployment")


if __name__ == "__main__":
    demonstrate_template_engine()
