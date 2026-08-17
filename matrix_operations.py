"""
Matrix Operations - Matrix manipulation and linear algebra basics.
Features: Basic operations, transpose, multiplication, and common algorithms.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Matrix:
    """Matrix implementation with basic operations."""
    
    data: List[List[float]]
    rows: int
    cols: int
    
    def __init__(self, data: List[List[float]]) -> None:
        """
        Initialize matrix from 2D list.
        
        Args:
            data: 2D list of numbers
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
    
    @classmethod
    def zeros(cls, rows: int, cols: int) -> 'Matrix':
        """Create matrix filled with zeros."""
        return cls([[0.0] * cols for _ in range(rows)])
    
    @classmethod
    def ones(cls, rows: int, cols: int) -> 'Matrix':
        """Create matrix filled with ones."""
        return cls([[1.0] * cols for _ in range(rows)])
    
    @classmethod
    def identity(cls, size: int) -> 'Matrix':
        """Create identity matrix."""
        data = [[0.0] * size for _ in range(size)]
        for i in range(size):
            data[i][i] = 1.0
        return cls(data)
    
    def copy(self) -> 'Matrix':
        """Create a copy of the matrix."""
        return Matrix([row[:] for row in self.data])
    
    def transpose(self) -> 'Matrix':
        """
        Transpose the matrix.
        
        Returns:
            Transposed matrix
        """
        transposed = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(transposed)
    
    def add(self, other: 'Matrix') -> 'Matrix':
        """
        Add another matrix element-wise.
        
        Args:
            other: Matrix to add
            
        Returns:
            Result matrix
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)
    
    def subtract(self, other: 'Matrix') -> 'Matrix':
        """
        Subtract another matrix element-wise.
        
        Args:
            other: Matrix to subtract
            
        Returns:
            Result matrix
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)
    
    def multiply_scalar(self, scalar: float) -> 'Matrix':
        """
        Multiply matrix by a scalar.
        
        Args:
            scalar: Scalar value
            
        Returns:
            Result matrix
        """
        result = [
            [self.data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)
    
    def multiply(self, other: 'Matrix') -> 'Matrix':
        """
        Multiply with another matrix.
        
        Args:
            other: Matrix to multiply with
            
        Returns:
            Result matrix
        """
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        
        result = [[0.0] * other.cols for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        
        return Matrix(result)
    
    def get_row(self, row: int) -> List[float]:
        """Get a specific row."""
        if row < 0 or row >= self.rows:
            raise IndexError("Row index out of range")
        return self.data[row][:]
    
    def get_column(self, col: int) -> List[float]:
        """Get a specific column."""
        if col < 0 or col >= self.cols:
            raise IndexError("Column index out of range")
        return [self.data[i][col] for i in range(self.rows)]
    
    def set_element(self, row: int, col: int, value: float) -> None:
        """Set element at specific position."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Index out of range")
        self.data[row][col] = value
    
    def get_element(self, row: int, col: int) -> float:
        """Get element at specific position."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Index out of range")
        return self.data[row][col]
    
    def is_square(self) -> bool:
        """Check if matrix is square."""
        return self.rows == self.cols
    
    def determinant(self) -> float:
        """
        Calculate determinant (for square matrices).
        
        Returns:
            Determinant value
        """
        if not self.is_square():
            raise ValueError("Matrix must be square for determinant")
        
        if self.rows == 1:
            return self.data[0][0]
        
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        
        # Laplace expansion
        det = 0.0
        for j in range(self.cols):
            sign = (-1) ** j
            minor = self._get_minor(0, j)
            det += sign * self.data[0][j] * minor.determinant()
        
        return det
    
    def _get_minor(self, row: int, col: int) -> 'Matrix':
        """Get minor matrix by removing row and column."""
        minor_data = [
            [self.data[i][j] for j in range(self.cols) if j != col]
            for i in range(self.rows) if i != row
        ]
        return Matrix(minor_data)
    
    def trace(self) -> float:
        """
        Calculate trace (sum of diagonal elements).
        
        Returns:
            Trace value
        """
        if not self.is_square():
            raise ValueError("Matrix must be square for trace")
        
        return sum(self.data[i][i] for i in range(self.rows))
    
    def sum(self) -> float:
        """Sum of all elements."""
        return sum(sum(row) for row in self.data)
    
    def max(self) -> float:
        """Maximum element in matrix."""
        return max(max(row) for row in self.data)
    
    def min(self) -> float:
        """Minimum element in matrix."""
        return min(min(row) for row in self.data)
    
    def __str__(self) -> str:
        """String representation of matrix."""
        lines = []
        for row in self.data:
            line = " ".join(f"{val:8.2f}" for val in row)
            lines.append(line)
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Representation of matrix."""
        return f"Matrix({self.rows}x{self.cols})"


def rotate_matrix_clockwise(matrix: Matrix) -> Matrix:
    """
    Rotate matrix 90 degrees clockwise.
    
    Args:
        matrix: Matrix to rotate
        
    Returns:
        Rotated matrix
    """
    transposed = matrix.transpose()
    # Reverse each row
    rotated_data = [row[::-1] for row in transposed.data]
    return Matrix(rotated_data)


def rotate_matrix_counterclockwise(matrix: Matrix) -> Matrix:
    """
    Rotate matrix 90 degrees counterclockwise.
    
    Args:
        matrix: Matrix to rotate
        
    Returns:
        Rotated matrix
    """
    transposed = matrix.transpose()
    # Reverse each column (reverse order of rows)
    rotated_data = transposed.data[::-1]
    return Matrix(rotated_data)


def search_in_matrix(matrix: Matrix, target: float) -> Optional[Tuple[int, int]]:
    """
    Search for element in sorted matrix (row-wise and column-wise sorted).
    
    Args:
        matrix: Sorted matrix to search
        target: Value to search for
        
    Returns:
        Tuple of (row, col) if found, None otherwise
    """
    if matrix.rows == 0 or matrix.cols == 0:
        return None
    
    row, col = 0, matrix.cols - 1
    
    while row < matrix.rows and col >= 0:
        current = matrix.get_element(row, col)
        
        if current == target:
            return (row, col)
        elif current > target:
            col -= 1
        else:
            row += 1
    
    return None


def spiral_traversal(matrix: Matrix) -> List[float]:
    """
    Traverse matrix in spiral order.
    
    Args:
        matrix: Matrix to traverse
        
    Returns:
        List of elements in spiral order
    """
    if matrix.rows == 0 or matrix.cols == 0:
        return []
    
    result = []
    top, bottom = 0, matrix.rows - 1
    left, right = 0, matrix.cols - 1
    
    while top <= bottom and left <= right:
        # Traverse right
        for col in range(left, right + 1):
            result.append(matrix.get_element(top, col))
        top += 1
        
        # Traverse down
        for row in range(top, bottom + 1):
            result.append(matrix.get_element(row, right))
        right -= 1
        
        # Traverse left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix.get_element(bottom, col))
            bottom -= 1
        
        # Traverse up
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix.get_element(row, left))
            left += 1
    
    return result


def main() -> None:
    """Demonstrate matrix operations."""
    
    print("=== Matrix Creation ===")
    zeros = Matrix.zeros(3, 3)
    ones = Matrix.ones(2, 4)
    identity = Matrix.identity(3)
    
    print("Zeros (3x3):")
    print(zeros)
    print("\nOnes (2x4):")
    print(ones)
    print("\nIdentity (3x3):")
    print(identity)
    
    print("\n=== Matrix Operations ===")
    A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
    
    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)
    
    print("\nA + B:")
    print(A.add(B))
    
    print("\nA - B:")
    print(A.subtract(B))
    
    print("\nA * 2:")
    print(A.multiply_scalar(2))
    
    print("\nA * B:")
    print(A.multiply(B))
    
    print("\n=== Transpose ===")
    C = Matrix([[1, 2, 3], [4, 5, 6]])
    print("Original:")
    print(C)
    print("\nTransposed:")
    print(C.transpose())
    
    print("\n=== Matrix Properties ===")
    square = Matrix([[4, 2], [3, 1]])
    print("Square matrix:")
    print(square)
    print(f"Determinant: {square.determinant()}")
    print(f"Trace: {square.trace()}")
    print(f"Sum: {square.sum()}")
    print(f"Max: {square.max()}")
    print(f"Min: {square.min()}")
    
    print("\n=== Rotation ===")
    original = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print("Original:")
    print(original)
    print("\nRotated clockwise:")
    print(rotate_matrix_clockwise(original))
    print("\nRotated counterclockwise:")
    print(rotate_matrix_counterclockwise(original))
    
    print("\n=== Search in Sorted Matrix ===")
    sorted_matrix = Matrix([
        [1, 4, 7, 11],
        [2, 5, 8, 12],
        [3, 6, 9, 16],
        [10, 13, 14, 17]
    ])
    print("Sorted matrix:")
    print(sorted_matrix)
    
    targets = [5, 9, 15, 1]
    for target in targets:
        pos = search_in_matrix(sorted_matrix, target)
        print(f"Search {target}: {pos if pos else 'Not found'}")
    
    print("\n=== Spiral Traversal ===")
    test_matrix = Matrix([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ])
    print("Matrix:")
    print(test_matrix)
    print(f"Spiral traversal: {spiral_traversal(test_matrix)}")


if __name__ == "__main__":
    main()
