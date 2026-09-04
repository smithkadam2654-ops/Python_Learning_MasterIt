"""
Template Method - Template method pattern for algorithm skeleton.
Features: Abstract base class, step customization, and hook methods.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


class DataProcessor(ABC):
    """Abstract data processor with template method."""
    
    def process(self, data: List) -> List:
        """
        Template method - defines algorithm skeleton.
        
        Args:
            data: Data to process
            
        Returns:
            Processed data
        """
        print("Starting data processing...")
        
        # Step 1: Validate
        validated = self.validate(data)
        if not validated:
            print("Validation failed")
            return []
        
        # Hook: Pre-processing
        self.pre_process(data)
        
        # Step 2: Transform
        transformed = self.transform(data)
        
        # Hook: Post-processing
        self.post_process(transformed)
        
        # Step 3: Output
        result = self.output(transformed)
        
        print("Data processing complete")
        return result
    
    @abstractmethod
    def validate(self, data: List) -> bool:
        """Validate input data."""
        pass
    
    @abstractmethod
    def transform(self, data: List) -> List:
        """Transform the data."""
        pass
    
    @abstractmethod
    def output(self, data: List) -> List:
        """Output the result."""
        pass
    
    def pre_process(self, data: List) -> None:
        """Hook for pre-processing (optional override)."""
        pass
    
    def post_process(self, data: List) -> None:
        """Hook for post-processing (optional override)."""
        pass


class NumberProcessor(DataProcessor):
    """Processor for number data."""
    
    def validate(self, data: List) -> bool:
        """Validate that all items are numbers."""
        return all(isinstance(x, (int, float)) for x in data)
    
    def transform(self, data: List) -> List:
        """Square all numbers."""
        return [x ** 2 for x in data]
    
    def output(self, data: List) -> List:
        """Return transformed data."""
        return data
    
    def pre_process(self, data: List) -> None:
        """Log pre-processing."""
        print(f"Pre-processing {len(data)} numbers")
    
    def post_process(self, data: List) -> None:
        """Log post-processing."""
        print(f"Post-processing {len(data)} squared numbers")


class TextProcessor(DataProcessor):
    """Processor for text data."""
    
    def validate(self, data: List) -> bool:
        """Validate that all items are strings."""
        return all(isinstance(x, str) for x in data)
    
    def transform(self, data: List) -> List:
        """Convert all strings to uppercase."""
        return [x.upper() for x in data]
    
    def output(self, data: List) -> List:
        """Return transformed data."""
        return data


class ReportGenerator(ABC):
    """Abstract report generator with template method."""
    
    def generate(self) -> str:
        """
        Template method for report generation.
        
        Returns:
            Generated report
        """
        report = []
        
        # Header
        report.append(self.generate_header())
        
        # Body
        report.append(self.generate_body())
        
        # Footer
        report.append(self.generate_footer())
        
        return "\n".join(report)
    
    @abstractmethod
    def generate_header(self) -> str:
        """Generate report header."""
        pass
    
    @abstractmethod
    def generate_body(self) -> str:
        """Generate report body."""
        pass
    
    @abstractmethod
    def generate_footer(self) -> str:
        """Generate report footer."""
        pass


class HTMLReport(ReportGenerator):
    """HTML report generator."""
    
    def __init__(self, title: str, content: str) -> None:
        """
        Initialize HTML report.
        
        Args:
            title: Report title
            content: Report content
        """
        self.title = title
        self.content = content
    
    def generate_header(self) -> str:
        """Generate HTML header."""
        return f"<html><head><title>{self.title}</title></head><body>"
    
    def generate_body(self) -> str:
        """Generate HTML body."""
        return f"<h1>{self.title}</h1><p>{self.content}</p>"
    
    def generate_footer(self) -> str:
        """Generate HTML footer."""
        return "<footer>Generated with HTML Report</footer></body></html>"


class MarkdownReport(ReportGenerator):
    """Markdown report generator."""
    
    def __init__(self, title: str, content: str) -> None:
        """
        Initialize Markdown report.
        
        Args:
            title: Report title
            content: Report content
        """
        self.title = title
        self.content = content
    
    def generate_header(self) -> str:
        """Generate Markdown header."""
        return f"# {self.title}"
    
    def generate_body(self) -> str:
        """Generate Markdown body."""
        return f"\n{self.content}"
    
    def generate_footer(self) -> str:
        """Generate Markdown footer."""
        return "\n---\n*Generated with Markdown Report*"


class GameAI(ABC):
    """Abstract game AI with template method."""
    
    def take_turn(self) -> str:
        """
        Template method for AI turn.
        
        Returns:
            Action description
        """
        actions = []
        
        # Analyze situation
        situation = self.analyze_situation()
        actions.append(f"Analyzed: {situation}")
        
        # Select action
        action = self.select_action()
        actions.append(f"Selected: {action}")
        
        # Execute action
        result = self.execute_action(action)
        actions.append(f"Executed: {result}")
        
        return " -> ".join(actions)
    
    @abstractmethod
    def analyze_situation(self) -> str:
        """Analyze current game situation."""
        pass
    
    @abstractmethod
    def select_action(self) -> str:
        """Select an action."""
        pass
    
    @abstractmethod
    def execute_action(self, action: str) -> str:
        """Execute the selected action."""
        pass


class ChessAI(GameAI):
    """Chess AI implementation."""
    
    def analyze_situation(self) -> str:
        """Analyze chess position."""
        return "White has material advantage, Black has better position"
    
    def select_action(self) -> str:
        """Select chess move."""
        return "Move knight to f3"
    
    def execute_action(self, action: str) -> str:
        """Execute chess move."""
        return f"{action} - Position improved"


class TicTacToeAI(GameAI):
    """Tic-Tac-Toe AI implementation."""
    
    def analyze_situation(self) -> str:
        """Analyze Tic-Tac-Toe board."""
        return "X has two in a row, need to block"
    
    def select_action(self) -> str:
        """Select Tic-Tac-Toe move."""
        return "Place O in center"
    
    def execute_action(self, action: str) -> str:
        """Execute Tic-Tac-Toe move."""
        return f"{action} - Blocked X's win"


class BeverageMaker(ABC):
    """Abstract beverage maker with template method."""
    
    def make(self) -> str:
        """
        Template method for making beverage.
        
        Returns:
            Beverage preparation steps
        """
        steps = []
        
        # Boil water
        steps.append(self.boil_water())
        
        # Brew
        steps.append(self.brew())
        
        # Pour in cup
        steps.append(self.pour_in_cup())
        
        # Add condiments (hook)
        if self.want_condiments():
            steps.append(self.add_condiments())
        
        return "\n".join(steps)
    
    def boil_water(self) -> str:
        """Boil water."""
        return "Boiling water"
    
    def pour_in_cup(self) -> str:
        """Pour in cup."""
        return "Pouring into cup"
    
    @abstractmethod
    def brew(self) -> str:
        """Brew the beverage."""
        pass
    
    @abstractmethod
    def add_condiments(self) -> str:
        """Add condiments."""
        pass
    
    def want_condiments(self) -> bool:
        """Hook to determine if condiments should be added."""
        return True


class CoffeeMaker(BeverageMaker):
    """Coffee maker implementation."""
    
    def brew(self) -> str:
        """Brew coffee."""
        return "Dripping coffee through filter"
    
    def add_condiments(self) -> str:
        """Add sugar and milk."""
        return "Adding sugar and milk"
    
    def want_condiments(self) -> bool:
        """Coffee always has condiments."""
        return True


class TeaMaker(BeverageMaker):
    """Tea maker implementation."""
    
    def brew(self) -> str:
        """Brew tea."""
        return "Steeping tea bag"
    
    def add_condiments(self) -> str:
        """Add lemon."""
        return "Adding lemon"
    
    def want_condiments(self) -> bool:
        """Tea might not have condiments."""
        return False  # Pure tea


def main() -> None:
    """Demonstrate template method pattern."""
    
    print("=== Data Processors ===")
    
    number_processor = NumberProcessor()
    text_processor = TextProcessor()
    
    numbers = [1, 2, 3, 4, 5]
    print(f"\nProcessing numbers: {numbers}")
    result = number_processor.process(numbers)
    print(f"Result: {result}")
    
    texts = ["hello", "world", "python"]
    print(f"\nProcessing texts: {texts}")
    result = text_processor.process(texts)
    print(f"Result: {result}")
    
    invalid_data = [1, "two", 3]
    print(f"\nProcessing invalid data: {invalid_data}")
    result = number_processor.process(invalid_data)
    print(f"Result: {result}")
    
    print("\n=== Report Generators ===")
    
    html_report = HTMLReport("Sales Report", "Sales increased by 25%")
    print("\nHTML Report:")
    print(html_report.generate())
    
    markdown_report = MarkdownReport("Sales Report", "Sales increased by 25%")
    print("\nMarkdown Report:")
    print(markdown_report.generate())
    
    print("\n=== Game AI ===")
    
    chess_ai = ChessAI()
    print("\nChess AI Turn:")
    print(chess_ai.take_turn())
    
    tictactoe_ai = TicTacToeAI()
    print("\nTic-Tac-Toe AI Turn:")
    print(tictactoe_ai.take_turn())
    
    print("\n=== Beverage Makers ===")
    
    coffee_maker = CoffeeMaker()
    print("\nMaking Coffee:")
    print(coffee_maker.make())
    
    tea_maker = TeaMaker()
    print("\nMaking Tea:")
    print(tea_maker.make())


if __name__ == "__main__":
    main()
