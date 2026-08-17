"""
Command Line Parser - Custom argument parser for CLI applications.
Features: Argument parsing, validation, help generation, and subcommands.
"""

import sys
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum


class ArgType(Enum):
    """Argument data types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"


@dataclass
class Argument:
    """Command line argument definition."""
    name: str
    short_name: Optional[str] = None
    help_text: str = ""
    required: bool = False
    default: Any = None
    arg_type: ArgType = ArgType.STRING
    choices: Optional[List[str]] = None


@dataclass
class ParsedArgs:
    """Container for parsed arguments."""
    args: Dict[str, Any]
    positional: List[str]
    
    def get(self, name: str, default: Any = None) -> Any:
        """Get argument value with optional default."""
        return self.args.get(name, default)
    
    def has(self, name: str) -> bool:
        """Check if argument was provided."""
        return name in self.args


class ArgumentParser:
    """Command line argument parser."""
    
    def __init__(self, description: str = "", program_name: Optional[str] = None) -> None:
        """
        Initialize argument parser.
        
        Args:
            description: Program description
            program_name: Program name (defaults to sys.argv[0])
        """
        self.description = description
        self.program_name = program_name or sys.argv[0]
        self.arguments: Dict[str, Argument] = {}
        self.subcommands: Dict[str, 'ArgumentParser'] = {}
        self.current_subcommand: Optional[str] = None
    
    def add_argument(self, name: str, short_name: Optional[str] = None, 
                    help_text: str = "", required: bool = False,
                    default: Any = None, arg_type: ArgType = ArgType.STRING,
                    choices: Optional[List[str]] = None) -> 'ArgumentParser':
        """
        Add an argument to the parser.
        
        Args:
            name: Argument name (long form, e.g., --output)
            short_name: Short form (e.g., -o)
            help_text: Help text for the argument
            required: Whether argument is required
            default: Default value
            arg_type: Argument data type
            choices: List of valid choices
            
        Returns:
            Self for method chaining
        """
        # Remove leading dashes from name
        clean_name = name.replace('-', '')
        
        self.arguments[clean_name] = Argument(
            name=clean_name,
            short_name=short_name,
            help_text=help_text,
            required=required,
            default=default,
            arg_type=arg_type,
            choices=choices
        )
        
        return self
    
    def add_subcommand(self, name: str, parser: 'ArgumentParser') -> 'ArgumentParser':
        """
        Add a subcommand parser.
        
        Args:
            name: Subcommand name
            parser: Parser for the subcommand
            
        Returns:
            Self for method chaining
        """
        self.subcommands[name] = parser
        return self
    
    def _convert_value(self, value: str, arg_type: ArgType) -> Any:
        """Convert string value to specified type."""
        if arg_type == ArgType.INTEGER:
            return int(value)
        elif arg_type == ArgType.FLOAT:
            return float(value)
        elif arg_type == ArgType.BOOLEAN:
            return value.lower() in ('true', 'yes', '1', 't', 'y')
        elif arg_type == ArgType.LIST:
            return value.split(',')
        else:
            return value
    
    def _parse_argument(self, arg: str, args: List[str], index: int) -> tuple[str, Any, int]:
        """Parse a single argument."""
        # Check for short form (-a)
        if arg.startswith('-') and not arg.startswith('--'):
            arg_name = arg[1:]
            arg_def = None
            
            # Find argument by short name
            for name, definition in self.arguments.items():
                if definition.short_name == arg_name:
                    arg_def = definition
                    arg_name = name
                    break
            
            if arg_def is None:
                raise ValueError(f"Unknown argument: {arg}")
            
            # Boolean flags don't need values
            if arg_def.arg_type == ArgType.BOOLEAN:
                return arg_name, True, index + 1
            
            # Get value
            if index + 1 >= len(args):
                raise ValueError(f"Argument {arg} requires a value")
            
            value = args[index + 1]
            return arg_name, self._convert_value(value, arg_def.arg_type), index + 2
        
        # Check for long form (--argument)
        elif arg.startswith('--'):
            arg_name = arg[2:]
            
            # Handle --arg=value format
            if '=' in arg_name:
                arg_name, value = arg_name.split('=', 1)
            else:
                if index + 1 >= len(args):
                    raise ValueError(f"Argument {arg} requires a value")
                value = args[index + 1]
                index += 1
            
            if arg_name not in self.arguments:
                raise ValueError(f"Unknown argument: {arg}")
            
            arg_def = self.arguments[arg_name]
            
            # Boolean flags
            if arg_def.arg_type == ArgType.BOOLEAN:
                if '=' in arg:
                    return arg_name, self._convert_value(value, ArgType.BOOLEAN), index + 1
                return arg_name, True, index + 1
            
            return arg_name, self._convert_value(value, arg_def.arg_type), index + 1
        
        # Positional argument
        else:
            return None, arg, index + 1
    
    def parse_args(self, args: Optional[List[str]] = None) -> ParsedArgs:
        """
        Parse command line arguments.
        
        Args:
            args: List of arguments (defaults to sys.argv[1:])
            
        Returns:
            ParsedArgs object with parsed values
        """
        if args is None:
            args = sys.argv[1:]
        
        parsed_args = {}
        positional = []
        index = 0
        
        # Check for subcommand
        if args and args[0] in self.subcommands:
            subcommand = args[0]
            self.current_subcommand = subcommand
            return self.subcommands[subcommand].parse_args(args[1:])
        
        while index < len(args):
            arg = args[index]
            
            if arg.startswith('-'):
                name, value, new_index = self._parse_argument(arg, args, index)
                index = new_index
                
                if name:
                    parsed_args[name] = value
            else:
                positional.append(arg)
                index += 1
        
        # Validate required arguments
        for name, arg_def in self.arguments.items():
            if arg_def.required and name not in parsed_args:
                raise ValueError(f"Required argument --{name} not provided")
            
            # Set defaults
            if name not in parsed_args and arg_def.default is not None:
                parsed_args[name] = arg_def.default
            
            # Validate choices
            if name in parsed_args and arg_def.choices:
                if parsed_args[name] not in arg_def.choices:
                    raise ValueError(f"Invalid choice for --{name}: {parsed_args[name]}")
        
        return ParsedArgs(args=parsed_args, positional=positional)
    
    def print_help(self) -> None:
        """Print help message."""
        print(f"Usage: {self.program_name} [OPTIONS]")
        
        if self.description:
            print(f"\n{self.description}")
        
        if self.arguments:
            print("\nOptions:")
            
            for name, arg in self.arguments.items():
                short = f"-{arg.short_name}, " if arg.short_name else "    "
                print(f"  {short}--{name:<15} {arg.help_text}")
                
                if arg.default is not None:
                    print(f"{'':22}Default: {arg.default}")
                
                if arg.choices:
                    print(f"{'':22}Choices: {', '.join(arg.choices)}")
        
        if self.subcommands:
            print("\nSubcommands:")
            for name in self.subcommands:
                print(f"  {name}")
    
    def generate_help(self) -> str:
        """Generate help message as string."""
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            self.print_help()
        return output.getvalue()


class CLIApplication:
    """CLI application framework."""
    
    def __init__(self, name: str, description: str = "") -> None:
        """
        Initialize CLI application.
        
        Args:
            name: Application name
            description: Application description
        """
        self.name = name
        self.description = description
        self.parser = ArgumentParser(description, name)
        self.commands: Dict[str, Callable[[ParsedArgs], int]] = {}
    
    def add_command(self, name: str, handler: Callable[[ParsedArgs], int],
                    help_text: str = "") -> 'CLIApplication':
        """
        Add a command to the application.
        
        Args:
            name: Command name
            handler: Function to handle the command
            help_text: Help text for the command
            
        Returns:
            Self for method chaining
        """
        self.commands[name] = handler
        return self
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI application.
        
        Args:
            args: Command line arguments
            
        Returns:
            Exit code
        """
        try:
            parsed = self.parser.parse_args(args)
            
            # Check for help
            if parsed.has('help') or not parsed.positional:
                self.parser.print_help()
                return 0
            
            # Execute command
            command = parsed.positional[0] if parsed.positional else None
            
            if command in self.commands:
                return self.commands[command](parsed)
            else:
                print(f"Unknown command: {command}")
                self.parser.print_help()
                return 1
                
        except ValueError as e:
            print(f"Error: {e}")
            self.parser.print_help()
            return 1
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return 130


def main() -> None:
    """Demonstrate command line parser."""
    
    print("=== Basic Argument Parsing ===")
    parser = ArgumentParser(
        description="A sample command line tool",
        program_name="mytool"
    )
    
    parser.add_argument("--input", "-i", help_text="Input file", required=True)
    parser.add_argument("--output", "-o", help_text="Output file", default="output.txt")
    parser.add_argument("--verbose", "-v", help_text="Verbose output", arg_type=ArgType.BOOLEAN)
    parser.add_argument("--count", "-c", help_text="Number of iterations", arg_type=ArgType.INTEGER, default=1)
    parser.add_argument("--format", help_text="Output format", choices=["json", "csv", "xml"])
    
    # Simulate command line arguments
    test_args = ["--input", "data.txt", "--output", "result.txt", "--verbose", "--count", "5"]
    
    try:
        parsed = parser.parse_args(test_args)
        print(f"Parsed arguments:")
        print(f"  Input: {parsed.get('input')}")
        print(f"  Output: {parsed.get('output')}")
        print(f"  Verbose: {parsed.get('verbose')}")
        print(f"  Count: {parsed.get('count')}")
        print(f"  Format: {parsed.get('format')}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== Help Generation ===")
    parser.print_help()
    
    print("\n=== CLI Application ===")
    app = CLIApplication("myapp", "A sample CLI application")
    
    def handle_greet(args: ParsedArgs) -> int:
        """Handle greet command."""
        name = args.get('name', 'World')
        count = args.get('count', 1)
        
        for _ in range(count):
            print(f"Hello, {name}!")
        
        return 0
    
    def handle_version(args: ParsedArgs) -> int:
        """Handle version command."""
        print("MyApp v1.0.0")
        return 0
    
    # Add command-specific arguments
    app.parser.add_argument("--name", "-n", help_text="Name to greet", default="World")
    app.parser.add_argument("--count", "-c", help_text="Number of times", arg_type=ArgType.INTEGER, default=1)
    
    # Run with simulated arguments
    print("Running: greet --name Alice --count 3")
    exit_code = app.run(["greet", "--name", "Alice", "--count", "3"])
    print(f"Exit code: {exit_code}")
    
    print("\nRunning: version")
    exit_code = app.run(["version"])
    print(f"Exit code: {exit_code}")


if __name__ == "__main__":
    main()
