"""
Expression Calculator - Mathematical expression parser and evaluator.
Features: Arithmetic operations, functions, and variable support.
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Token types."""
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"
    OPERATOR = "OPERATOR"
    FUNCTION = "FUNCTION"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    COMMA = "COMMA"


@dataclass
class Token:
    """Token."""
    type: TokenType
    value: str
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.type.value}({self.value})"


class ExpressionCalculator:
    """Mathematical expression calculator."""
    
    def __init__(self) -> None:
        """Initialize calculator."""
        self.variables: Dict[str, float] = {}
        self.functions: Dict[str, callable] = {
            'sin': lambda x: __import__('math').sin(x),
            'cos': lambda x: __import__('math').cos(x),
            'tan': lambda x: __import__('math').tan(x),
            'sqrt': lambda x: __import__('math').sqrt(x),
            'abs': lambda x: abs(x),
            'log': lambda x: __import__('math').log(x),
            'log10': lambda x: __import__('math').log10(x),
            'exp': lambda x: __import__('math').exp(x),
            'pow': lambda x, y: __import__('math').pow(x, y),
            'min': lambda *args: min(args),
            'max': lambda *args: max(args),
            'sum': lambda *args: sum(args),
        }
    
    def set_variable(self, name: str, value: float) -> None:
        """
        Set variable value.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Optional[float]:
        """
        Get variable value.
        
        Args:
            name: Variable name
            
        Returns:
            Variable value or None
        """
        return self.variables.get(name)
    
    def add_function(self, name: str, func: callable) -> None:
        """
        Add custom function.
        
        Args:
            name: Function name
            func: Function
        """
        self.functions[name] = func
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize expression.
        
        Args:
            expression: Expression string
            
        Returns:
            List of tokens
        """
        tokens = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Number
            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, num_str))
                continue
            
            # Variable or function
            if char.isalpha():
                name_str = ""
                while i < len(expression) and expression[i].isalnum():
                    name_str += expression[i]
                    i += 1
                
                if name_str in self.functions:
                    tokens.append(Token(TokenType.FUNCTION, name_str))
                else:
                    tokens.append(Token(TokenType.VARIABLE, name_str))
                continue
            
            # Operator
            if char in '+-*/^%':
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                continue
            
            # Parentheses
            if char == '(':
                tokens.append(Token(TokenType.LPAREN, char))
                i += 1
                continue
            
            if char == ')':
                tokens.append(Token(TokenType.RPAREN, char))
                i += 1
                continue
            
            # Comma
            if char == ',':
                tokens.append(Token(TokenType.COMMA, char))
                i += 1
                continue
            
            raise ValueError(f"Invalid character: {char}")
        
        return tokens
    
    def evaluate(self, expression: str) -> float:
        """
        Evaluate expression.
        
        Args:
            expression: Expression string
            
        Returns:
            Result
        """
        tokens = self.tokenize(expression)
        result = self._parse_expression(tokens)
        return result
    
    def _parse_expression(self, tokens: List[Token]) -> float:
        """Parse and evaluate expression."""
        return self._parse_addition(tokens)
    
    def _parse_addition(self, tokens: List[Token]) -> float:
        """Parse addition and subtraction."""
        left = self._parse_multiplication(tokens)
        
        while tokens and tokens[0].type == TokenType.OPERATOR and tokens[0].value in '+-':
            op = tokens.pop(0)
            right = self._parse_multiplication(tokens)
            
            if op.value == '+':
                left += right
            else:
                left -= right
        
        return left
    
    def _parse_multiplication(self, tokens: List[Token]) -> float:
        """Parse multiplication and division."""
        left = self._parse_power(tokens)
        
        while tokens and tokens[0].type == TokenType.OPERATOR and tokens[0].value in '*/%':
            op = tokens.pop(0)
            right = self._parse_power(tokens)
            
            if op.value == '*':
                left *= right
            elif op.value == '/':
                left /= right
            elif op.value == '%':
                left %= right
        
        return left
    
    def _parse_power(self, tokens: List[Token]) -> float:
        """Parse power operation."""
        left = self._parse_unary(tokens)
        
        if tokens and tokens[0].type == TokenType.OPERATOR and tokens[0].value == '^':
            tokens.pop(0)
            right = self._parse_unary(tokens)
            left = left ** right
        
        return left
    
    def _parse_unary(self, tokens: List[Token]) -> float:
        """Parse unary operators."""
        if tokens and tokens[0].type == TokenType.OPERATOR and tokens[0].value in '+-':
            op = tokens.pop(0)
            value = self._parse_unary(tokens)
            return -value if op.value == '-' else value
        
        return self._parse_primary(tokens)
    
    def _parse_primary(self, tokens: List[Token]) -> float:
        """Parse primary expression."""
        if not tokens:
            raise ValueError("Unexpected end of expression")
        
        token = tokens[0]
        
        # Number
        if token.type == TokenType.NUMBER:
            tokens.pop(0)
            return float(token.value)
        
        # Variable
        if token.type == TokenType.VARIABLE:
            tokens.pop(0)
            if token.value in self.variables:
                return self.variables[token.value]
            raise ValueError(f"Unknown variable: {token.value}")
        
        # Function
        if token.type == TokenType.FUNCTION:
            tokens.pop(0)
            if not tokens or tokens[0].type != TokenType.LPAREN:
                raise ValueError("Expected '(' after function")
            tokens.pop(0)  # Remove '('
            
            args = []
            if tokens and tokens[0].type != TokenType.RPAREN:
                args.append(self._parse_expression(tokens))
                
                while tokens and tokens[0].type == TokenType.COMMA:
                    tokens.pop(0)  # Remove ','
                    args.append(self._parse_expression(tokens))
            
            if not tokens or tokens[0].type != TokenType.RPAREN:
                raise ValueError("Expected ')' after function arguments")
            tokens.pop(0)  # Remove ')'
            
            if token.value in self.functions:
                return self.functions[token.value](*args)
            raise ValueError(f"Unknown function: {token.value}")
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            tokens.pop(0)  # Remove '('
            result = self._parse_expression(tokens)
            if not tokens or tokens[0].type != TokenType.RPAREN:
                raise ValueError("Expected ')'")
            tokens.pop(0)  # Remove ')'
            return result
        
        raise ValueError(f"Unexpected token: {token}")
    
    def get_tokens(self, expression: str) -> List[Token]:
        """
        Get tokens for expression (for debugging).
        
        Args:
            expression: Expression string
            
        Returns:
            List of tokens
        """
        return self.tokenize(expression)


def main() -> None:
    """Demonstrate expression calculator."""
    
    print("=== Expression Calculator Demo ===")
    
    calc = ExpressionCalculator()
    
    # Set variables
    calc.set_variable('x', 5)
    calc.set_variable('y', 3)
    calc.set_variable('pi', 3.14159)
    
    # Test expressions
    expressions = [
        "2 + 3",
        "10 - 4",
        "3 * 4",
        "15 / 3",
        "2 ^ 3",
        "(2 + 3) * 4",
        "x + y",
        "sin(pi/2)",
        "sqrt(16)",
        "max(5, 10, 3)",
        "sum(1, 2, 3, 4, 5)",
        "2 * x + y",
        "abs(-5)",
        "log10(100)"
    ]
    
    for expr in expressions:
        try:
            result = calc.evaluate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} = Error: {e}")
    
    # Show tokens
    print("\n=== Tokenization ===")
    expr = "2 + 3 * sin(x)"
    tokens = calc.get_tokens(expr)
    print(f"Expression: {expr}")
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    
    # Custom function
    print("\n=== Custom Function ===")
    calc.add_function('double', lambda x: x * 2)
    print(f"double(5) = {calc.evaluate('double(5)')}")
    
    calc.add_function('avg', lambda *args: sum(args) / len(args))
    print(f"avg(10, 20, 30) = {calc.evaluate('avg(10, 20, 30)')}")


if __name__ == "__main__":
    main()
