"""
CLI Utilities Module

This module provides comprehensive command-line interface utilities including:
- Command-line argument parsing
- Interactive menu systems
- Progress bars and spinners
- Terminal colors and formatting
- Input validation and prompts
- Table and data display
- Configuration file handling
- Logging to console
- User authentication helpers
- Shell command execution

All functions include comprehensive docstrings and type hints.
"""

import sys
import os
import getpass
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import time


class TerminalColors:
    """ANSI color codes for terminal output."""
    
    # Reset
    RESET = '\033[0m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Cursor positioning
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[K'
    MOVE_UP = '\033[1A'
    MOVE_DOWN = '\033[1B'
    MOVE_RIGHT = '\033[1C'
    MOVE_LEFT = '\033[1D'


class TerminalFormatter:
    """Terminal formatting utilities."""
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Apply color to text."""
        return f"{color}{text}{TerminalColors.RESET}"
    
    @staticmethod
    def style(text: str, style: str) -> str:
        """Apply style to text."""
        return f"{style}{text}{TerminalColors.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        """Format text as success message."""
        return TerminalFormatter.colorize(f"✓ {text}", TerminalColors.GREEN)
    
    @staticmethod
    def error(text: str) -> str:
        """Format text as error message."""
        return TerminalFormatter.colorize(f"✗ {text}", TerminalColors.RED)
    
    @staticmethod
    def warning(text: str) -> str:
        """Format text as warning message."""
        return TerminalFormatter.colorize(f"⚠ {text}", TerminalColors.YELLOW)
    
    @staticmethod
    def info(text: str) -> str:
        """Format text as info message."""
        return TerminalFormatter.colorize(f"ℹ {text}", TerminalColors.BLUE)
    
    @staticmethod
    def bold(text: str) -> str:
        """Format text as bold."""
        return TerminalFormatter.style(text, TerminalColors.BOLD)
    
    @staticmethod
    def underline(text: str) -> str:
        """Format text as underlined."""
        return TerminalFormatter.style(text, TerminalColors.UNDERLINE)
    
    @staticmethod
    def title(text: str) -> str:
        """Format text as title."""
        return TerminalFormatter.style(TerminalFormatter.bold(text), TerminalColors.CYAN)
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        print(TerminalColors.CLEAR_SCREEN, end='')
    
    @staticmethod
    def clear_line() -> None:
        """Clear the current line."""
        print(TerminalColors.CLEAR_LINE, end='')
    
    @staticmethod
    def move_cursor_up(lines: int = 1) -> None:
        """Move cursor up by specified lines."""
        print(f"\033[{lines}A", end='')
    
    @staticmethod
    def move_cursor_down(lines: int = 1) -> None:
        """Move cursor down by specified lines."""
        print(f"\033[{lines}B", end='')


class ProgressBar:
    """Progress bar for terminal display."""
    
    def __init__(self, total: int, width: int = 50, 
                 prefix: str = "Progress:", 
                 suffix: str = "Complete",
                 show_percentage: bool = True):
        """Initialize progress bar."""
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.show_percentage = show_percentage
        self.current = 0
    
    def update(self, amount: int = 1) -> None:
        """Update progress by specified amount."""
        self.current += amount
        self._display()
    
    def set_progress(self, current: int) -> None:
        """Set progress to specific value."""
        self.current = current
        self._display()
    
    def _display(self) -> None:
        """Display the progress bar."""
        percent = self.current / self.total if self.total > 0 else 0
        filled_length = int(self.width * percent)
        bar = '█' * filled_length + '-' * (self.width - filled_length)
        
        if self.show_percentage:
            progress_str = f"\r{self.prefix} |{bar}| {percent:.1%} {self.suffix}"
        else:
            progress_str = f"\r{self.prefix} |{bar}| {self.suffix}"
        
        print(progress_str, end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete
    
    def finish(self) -> None:
        """Ensure progress bar is completed."""
        self.current = self.total
        self._display()


class Spinner:
    """Loading spinner for terminal display."""
    
    def __init__(self, message: str = "Loading...", 
                 style: str = "dots",
                 color: str = TerminalColors.CYAN):
        """Initialize spinner."""
        self.message = message
        self.style = style
        self.color = color
        self.running = False
        self.spinner_chars = self._get_spinner_chars()
    
    def _get_spinner_chars(self) -> List[str]:
        """Get spinner characters based on style."""
        styles = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "arrows": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "lines": ["|", "/", "-", "\\"],
            "blocks": ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
            "simple": [".", "..", "..."]
        }
        return styles.get(self.style, styles["dots"])
    
    def start(self) -> None:
        """Start the spinner."""
        self.running = True
        self._animate()
    
    def stop(self) -> None:
        """Stop the spinner."""
        self.running = False
        TerminalFormatter.clear_line()
    
    def _animate(self) -> None:
        """Animate the spinner."""
        import itertools
        spinner_cycle = itertools.cycle(self.spinner_chars)
        
        while self.running:
            spinner_char = next(spinner_cycle)
            message = f"{self.color}{spinner_char} {self.message}{TerminalColors.RESET}"
            print(f"\r{message}", end='', flush=True)
            time.sleep(0.1)


class InputValidator:
    """Input validation utilities."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        import re
        pattern = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/.*)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        import re
        pattern = r'^\+?[\d\s-()]{10,}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_range(value: str, min_val: float, max_val: float) -> bool:
        """Validate numeric value is within range."""
        try:
            num = float(value)
            return min_val <= num <= max_val
        except ValueError:
            return False
    
    @staticmethod
    def validate_length(value: str, min_len: int, max_len: int) -> bool:
        """Validate string length is within range."""
        return min_len <= len(value) <= max_len
    
    @staticmethod
    def validate_choice(value: str, choices: List[str], 
                       case_sensitive: bool = False) -> bool:
        """Validate value is in allowed choices."""
        if not case_sensitive:
            value = value.lower()
            choices = [c.lower() for c in choices]
        return value in choices


class InputPrompt:
    """Interactive input prompts."""
    
    @staticmethod
    def prompt_text(message: str, default: str = "", 
                   required: bool = False) -> str:
        """Prompt for text input."""
        if default:
            prompt = f"{message} [{default}]: "
        else:
            prompt = f"{message}: "
        
        while True:
            value = input(prompt).strip()
            
            if not value:
                if default:
                    return default
                elif required:
                    print(TerminalFormatter.error("This field is required"))
                    continue
            
            return value
    
    @staticmethod
    def prompt_password(message: str = "Password: ",
                       confirm: bool = False) -> str:
        """Prompt for password input."""
        while True:
            password = getpass.getpass(message)
            
            if not password:
                print(TerminalFormatter.error("Password cannot be empty"))
                continue
            
            if confirm:
                confirm_password = getpass.getpass("Confirm password: ")
                if password != confirm_password:
                    print(TerminalFormatter.error("Passwords do not match"))
                    continue
            
            return password
    
    @staticmethod
    def prompt_number(message: str, min_val: Optional[float] = None,
                     max_val: Optional[float] = None,
                     default: Optional[float] = None,
                     integer: bool = False) -> Union[int, float]:
        """Prompt for numeric input."""
        while True:
            if default is not None:
                prompt = f"{message} [{default}]: "
            else:
                prompt = f"{message}: "
            
            value = input(prompt).strip()
            
            if not value and default is not None:
                return default
            
            try:
                if integer:
                    num = int(value)
                else:
                    num = float(value)
                
                if min_val is not None and num < min_val:
                    print(TerminalFormatter.error(f"Value must be at least {min_val}"))
                    continue
                
                if max_val is not None and num > max_val:
                    print(TerminalFormatter.error(f"Value must be at most {max_val}"))
                    continue
                
                return num
                
            except ValueError:
                print(TerminalFormatter.error("Please enter a valid number"))
    
    @staticmethod
    def prompt_choice(message: str, choices: List[str],
                     default: Optional[str] = None,
                     case_sensitive: bool = False) -> str:
        """Prompt for choice from list."""
        print(f"\n{message}")
        
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        
        while True:
            if default:
                prompt = f"Choice [1-{len(choices)}, default={choices.index(default)+1}]: "
            else:
                prompt = f"Choice [1-{len(choices)}]: "
            
            value = input(prompt).strip()
            
            if not value and default:
                return default
            
            try:
                index = int(value) - 1
                if 0 <= index < len(choices):
                    return choices[index]
                else:
                    print(TerminalFormatter.error("Invalid choice"))
            except ValueError:
                # Check if they entered the choice text
                if not case_sensitive:
                    value = value.lower()
                    normalized_choices = [c.lower() for c in choices]
                    if value in normalized_choices:
                        return choices[normalized_choices.index(value)]
                elif value in choices:
                    return value
                
                print(TerminalFormatter.error("Invalid choice"))
    
    @staticmethod
    def prompt_yes_no(message: str, default: bool = False) -> bool:
        """Prompt for yes/no confirmation."""
        default_str = "Y/n" if default else "y/N"
        
        while True:
            value = input(f"{message} [{default_str}]: ").strip().lower()
            
            if not value:
                return default
            
            if value in ['y', 'yes']:
                return True
            elif value in ['n', 'no']:
                return False
            else:
                print(TerminalFormatter.error("Please enter 'y' or 'n'"))


class MenuSystem:
    """Interactive menu system."""
    
    def __init__(self, title: str = "Main Menu"):
        """Initialize menu system."""
        self.title = title
        self.menu_items: List[Dict[str, Any]] = []
        self.submenus: Dict[str, 'MenuSystem'] = {}
    
    def add_item(self, label: str, action: Callable, 
                 key: Optional[str] = None) -> None:
        """Add menu item."""
        if key is None:
            key = str(len(self.menu_items) + 1)
        
        self.menu_items.append({
            "key": key,
            "label": label,
            "action": action
        })
    
    def add_submenu(self, label: str, submenu: 'MenuSystem',
                   key: Optional[str] = None) -> None:
        """Add submenu."""
        if key is None:
            key = str(len(self.menu_items) + 1)
        
        self.menu_items.append({
            "key": key,
            "label": label,
            "action": None,
            "submenu": submenu
        })
        self.submenus[key] = submenu
    
    def display(self) -> None:
        """Display the menu."""
        print(f"\n{TerminalFormatter.title(self.title)}")
        print("=" * len(self.title))
        
        for item in self.menu_items:
            key = item["key"]
            label = item["label"]
            print(f"  [{key}] {label}")
        
        print("  [0] Exit")
    
    def run(self) -> None:
        """Run the menu system."""
        while True:
            self.display()
            
            choice = input(f"\nSelect option: ").strip()
            
            if choice == "0":
                print(TerminalFormatter.info("Exiting..."))
                break
            
            # Find matching menu item
            selected_item = None
            for item in self.menu_items:
                if item["key"] == choice:
                    selected_item = item
                    break
            
            if selected_item is None:
                print(TerminalFormatter.error("Invalid choice"))
                continue
            
            # Execute action or submenu
            if "submenu" in selected_item:
                selected_item["submenu"].run()
            elif selected_item["action"]:
                try:
                    selected_item["action"]()
                except Exception as e:
                    print(TerminalFormatter.error(f"Error: {e}"))


class TableDisplay:
    """Table data display for terminal."""
    
    @staticmethod
    def display_table(headers: List[str], 
                     rows: List[List[str]],
                     max_width: Optional[int] = None) -> None:
        """Display data as formatted table."""
        if not rows:
            print(TerminalFormatter.warning("No data to display"))
            return
        
        # Calculate column widths
        col_widths = [len(str(header)) for header in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                cell_str = str(cell)
                if max_width and len(cell_str) > max_width:
                    cell_str = cell_str[:max_width-3] + "..."
                col_widths[i] = max(col_widths[i], len(cell_str))
        
        # Display header
        header_line = " | ".join(
            header.ljust(width) for header, width in zip(headers, col_widths)
        )
        print(TerminalFormatter.bold(header_line))
        
        # Display separator
        separator = "-+-".join("-" * width for width in col_widths)
        print(separator)
        
        # Display rows
        for row in rows:
            row_line = " | ".join(
                str(cell).ljust(width) for cell, width in zip(row, col_widths)
            )
            print(row_line)
    
    @staticmethod
    def display_dict_table(data: List[Dict], 
                          keys: Optional[List[str]] = None,
                          max_width: Optional[int] = None) -> None:
        """Display list of dictionaries as table."""
        if not data:
            print(TerminalFormatter.warning("No data to display"))
            return
        
        # Determine keys to display
        if keys is None:
            keys = list(data[0].keys())
        
        # Create headers and rows
        headers = keys
        rows = []
        
        for item in data:
            row = [str(item.get(key, "")) for key in keys]
            rows.append(row)
        
        TableDisplay.display_table(headers, rows, max_width)


class ConfigManager:
    """Configuration file management."""
    
    @staticmethod
    def load_config(file_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        import json
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(TerminalFormatter.warning(f"Config file not found: {file_path}"))
            return {}
        except json.JSONDecodeError as e:
            print(TerminalFormatter.error(f"Invalid JSON in config file: {e}"))
            return {}
    
    @staticmethod
    def save_config(config: Dict[str, Any], file_path: str) -> bool:
        """Save configuration to JSON file."""
        import json
        
        try:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(TerminalFormatter.error(f"Failed to save config: {e}"))
            return False
    
    @staticmethod
    def get_config_value(config: Dict[str, Any], 
                        key: str, 
                        default: Any = None) -> Any:
        """Get configuration value with dot notation support."""
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @staticmethod
    def set_config_value(config: Dict[str, Any],
                        key: str,
                        value: Any) -> Dict[str, Any]:
        """Set configuration value with dot notation support."""
        keys = key.split('.')
        current = config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        return config


class ShellExecutor:
    """Shell command execution utilities."""
    
    @staticmethod
    def execute_command(command: str, 
                       capture_output: bool = True,
                       check: bool = True) -> Tuple[int, str, str]:
        """Execute shell command and return exit code, stdout, stderr."""
        import subprocess
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check
            )
            
            return (
                result.returncode,
                result.stdout if capture_output else "",
                result.stderr if capture_output else ""
            )
        except subprocess.CalledProcessError as e:
            return (
                e.returncode,
                e.stdout if capture_output else "",
                e.stderr if capture_output else ""
            )
    
    @staticmethod
    def execute_interactive(command: str) -> int:
        """Execute interactive command."""
        import subprocess
        return subprocess.call(command, shell=True)
    
    @staticmethod
    def which(program: str) -> Optional[str]:
        """Find executable in system PATH."""
        return shutil.which(program)


class ConsoleLogger:
    """Console logging utilities."""
    
    def __init__(self, name: str = "App", level: str = "INFO"):
        """Initialize console logger."""
        self.name = name
        self.level = level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    
    def _should_log(self, message_level: str) -> bool:
        """Check if message should be logged based on level."""
        return self.levels.get(message_level, 1) >= self.levels.get(self.level, 1)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        if self._should_log("DEBUG"):
            print(f"{TerminalColors.DIM}[DEBUG] {self.name}: {message}{TerminalColors.RESET}")
    
    def info(self, message: str) -> None:
        """Log info message."""
        if self._should_log("INFO"):
            print(f"{TerminalColors.CYAN}[INFO] {self.name}: {message}{TerminalColors.RESET}")
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        if self._should_log("WARNING"):
            print(f"{TerminalColors.YELLOW}[WARNING] {self.name}: {message}{TerminalColors.RESET}")
    
    def error(self, message: str) -> None:
        """Log error message."""
        if self._should_log("ERROR"):
            print(f"{TerminalColors.RED}[ERROR] {self.name}: {message}{TerminalColors.RESET}")


def demonstrate_cli_utils():
    """Demonstrate CLI utilities functionality."""
    print("=== CLI Utilities Demonstration ===\n")
    
    # Terminal Formatting
    print("1. Terminal Formatting:")
    print(TerminalFormatter.success("Operation completed successfully"))
    print(TerminalFormatter.error("An error occurred"))
    print(TerminalFormatter.warning("This is a warning"))
    print(TerminalFormatter.info("This is information"))
    print(TerminalFormatter.bold("Bold text"))
    print(TerminalFormatter.title("Title Text"))
    
    # Progress Bar
    print("\n2. Progress Bar:")
    progress = ProgressBar(total=50, prefix="Processing:", suffix="Done")
    for i in range(51):
        progress.update()
        time.sleep(0.02)
    
    # Input Validation
    print("\n3. Input Validation:")
    print(f"   Valid email: {InputValidator.validate_email('test@example.com')}")
    print(f"   Invalid email: {InputValidator.validate_email('invalid-email')}")
    print(f"   Valid URL: {InputValidator.validate_url('https://example.com')}")
    print(f"   Valid phone: {InputValidator.validate_phone('+1-555-123-4567')}")
    print(f"   Range check: {InputValidator.validate_range('50', 0, 100)}")
    
    # Table Display
    print("\n4. Table Display:")
    headers = ["Name", "Age", "City"]
    rows = [
        ["John", "30", "New York"],
        ["Jane", "25", "Los Angeles"],
        ["Bob", "35", "Chicago"]
    ]
    TableDisplay.display_table(headers, rows)
    
    # Dict Table
    print("\n5. Dictionary Table:")
    data = [
        {"name": "Alice", "age": 28, "department": "Engineering"},
        {"name": "Charlie", "age": 32, "department": "Marketing"}
    ]
    TableDisplay.display_dict_table(data)
    
    # Configuration Management
    print("\n6. Configuration Management:")
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb"
        },
        "api": {
            "key": "secret_key",
            "timeout": 30
        }
    }
    
    host = ConfigManager.get_config_value(config, "database.host")
    print(f"   Database host: {host}")
    
    timeout = ConfigManager.get_config_value(config, "api.timeout", default=10)
    print(f"   API timeout: {timeout}")
    
    # Console Logger
    print("\n7. Console Logger:")
    logger = ConsoleLogger("DemoApp", level="DEBUG")
    logger.debug("This is a debug message")
    logger.info("Application started")
    logger.warning("Low memory warning")
    logger.error("Connection failed")
    
    # Shell Execution
    print("\n8. Shell Execution:")
    exit_code, stdout, stderr = ShellExecutor.execute_command("echo 'Hello from shell'")
    print(f"   Exit code: {exit_code}")
    print(f"   Output: {stdout.strip()}")
    
    # String Utilities
    print("\n9. String Utilities:")
    text = "Hello World"
    print(f"   Uppercase: {text.upper()}")
    print(f"   Lowercase: {text.lower()}")
    print(f"   Reversed: {text[::-1]}")
    print(f"   Word count: {len(text.split())}")
    
    print("\n=== Demonstration Complete ===")
    print("\nNote: Interactive prompts and menus require user input")
    print("and are not demonstrated in automated mode.")


if __name__ == "__main__":
    demonstrate_cli_utils()