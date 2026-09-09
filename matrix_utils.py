"""
Matrix Utilities - Common matrix operations and algorithms.
Features: Matrix multiplication, transpose, determinant, and basic linear algebra.
"""

from typing import List, Optional


class MatrixUtils:
    """Matrix utility functions and operations."""
    
    @staticmethod
    def create_matrix(rows: int, cols: int, default: float = 0) -> List[List[float]]:
        """
        Create a matrix with given dimensions.
        
        Args:
            rows: Number of rows
            cols: Number of columns
            default: Default value
            
        Returns:
            Matrix
        """
        return [[default for _ in range(cols)] for _ in range(rows)]
    
    @staticmethod
    def add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Add two matrices.
        
        Args:
            A: First matrix
            B: Second matrix
            
        Returns:
            Sum matrix
        """
        rows = len(A)
        cols = len(A[0])
        result = MatrixUtils.create_matrix(rows, cols)
        
        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] + B[i][j]
        
        return result
    
    @staticmethod
    def subtract(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Subtract two matrices.
        
        Args:
            A: First matrix
            B: Second matrix
            
        Returns:
            Difference matrix
        """
        rows = len(A)
        cols = len(A[0])
        result = MatrixUtils.create_matrix(rows, cols)
        
        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] - B[i][j]
        
        return result
    
    @staticmethod
    def multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Multiply two matrices.
        
        Args:
            A: First matrix
            B: Second matrix
            
        Returns:
            Product matrix
        """
        rows_a = len(A)
        cols_a = len(A[0])
        cols_b = len(B[0])
        
        result = MatrixUtils.create_matrix(rows_a, cols_b)
        
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    @staticmethod
    def scalar_multiply(A: List[List[float]], scalar: float) -> List[List[float]]:
        """
        Multiply matrix by scalar.
        
        Args:
            A: Matrix
            scalar: Scalar value
            
        Returns:
            Scaled matrix
        """
        rows = len(A)
        cols = len(A[0])
        result = MatrixUtils.create_matrix(rows, cols)
        
        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] * scalar
        
        return result
    
    @staticmethod
    def transpose(A: List[List[float]]) -> List[List[float]]:
        """
        Transpose matrix.
        
        Args:
            A: Matrix
            
        Returns:
            Transposed matrix
        """
        rows = len(A)
        cols = len(A[0])
        result = MatrixUtils.create_matrix(cols, rows)
        
        for i in range(rows):
            for j in range(cols):
                result[j][i] = A[i][j]
        
        return result
    
    @staticmethod
    def is_square(A: List[List[float]]) -> bool:
        """
        Check if matrix is square.
        
        Args:
            A: Matrix
            
        Returns:
            True if square
        """
        return len(A) == len(A[0]) if A else False
    
    @staticmethod
    def determinant(A: List[List[float]]) -> float:
        """
        Calculate determinant using recursive expansion.
        
        Args:
            A: Square matrix
            
        Returns:
            Determinant
        """
        if not MatrixUtils.is_square(A):
            raise ValueError("Matrix must be square")
        
        n = len(A)
        
        if n == 1:
            return A[0][0]
        
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        
        det = 0
        for j in range(n):
            # Get cofactor
            minor = MatrixUtils._get_minor(A, 0, j)
            sign = (-1) ** j
            det += sign * A[0][j] * MatrixUtils.determinant(minor)
        
        return det
    
    @staticmethod
    def _get_minor(A: List[List[float]], row: int, col: int) -> List[List[float]]:
        """Get minor matrix by removing row and column."""
        return [row[:col] + row[col + 1:] for i, row in enumerate(A) if i != row]
    
    @staticmethod
    def identity(n: int) -> List[List[float]]:
        """
        Create identity matrix.
        
        Args:
            n: Size
            
        Returns:
            Identity matrix
        """
        result = MatrixUtils.create_matrix(n, n)
        for i in range(n):
            result[i][i] = 1
        return result
    
    @staticmethod
    def power(A: List[List[float]], n: int) -> List[List[float]]:
        """
        Raise matrix to power n using exponentiation by squaring.
        
        Args:
            A: Square matrix
            n: Power (non-negative)
            
        Returns:
            Matrix raised to power n
        """
        if not MatrixUtils.is_square(A):
            raise ValueError("Matrix must be square")
        
        if n == 0:
            return MatrixUtils.identity(len(A))
        
        if n == 1:
            return A
        
        if n % 2 == 0:
            half = MatrixUtils.power(A, n // 2)
            return MatrixUtils.multiply(half, half)
        else:
            return MatrixUtils.multiply(A, MatrixUtils.power(A, n - 1))
    
    @staticmethod
    def strassen_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Strassen's algorithm for matrix multiplication (divide and conquer).
        
        Args:
            A: First matrix (must be square and size power of 2)
            B: Second matrix
            
        Returns:
            Product matrix
        """
        n = len(A)
        
        if n == 1:
            return [[A[0][0] * B[0][0]]]
        
        # Divide matrices into quadrants
        mid = n // 2
        
        A11 = [row[:mid] for row in A[:mid]]
        A12 = [row[mid:] for row in A[:mid]]
        A21 = [row[:mid] for row in A[mid:]]
        A22 = [row[mid:] for row in A[mid:]]
        
        B11 = [row[:mid] for row in B[:mid]]
        B12 = [row[mid:] for row in B[:mid]]
        B21 = [row[:mid] for row in B[mid:]]
        B22 = [row[mid:] for row in B[mid:]]
        
        # Calculate 7 products
        M1 = MatrixUtils.strassen_multiply(
            MatrixUtils.add(A11, A22), MatrixUtils.add(B11, B22))
        M2 = MatrixUtils.strassen_multiply(
            MatrixUtils.add(A21, A22), B11)
        M3 = MatrixUtils.strassen_multiply(
            A11, MatrixUtils.subtract(B12, B22))
        M4 = MatrixUtils.strassen_multiply(
            A22, MatrixUtils.subtract(B21, B11))
        M5 = MatrixUtils.strassen_multiply(
            MatrixUtils.add(A11, A12), B22)
        M6 = MatrixUtils.strassen_multiply(
            MatrixUtils.subtract(A21, A11), MatrixUtils.add(B11, B12))
        M7 = MatrixUtils.strassen_multiply(
            MatrixUtils.subtract(A12, A22), MatrixUtils.add(B21, B22))
        
        # Combine results
        C11 = MatrixUtils.add(MatrixUtils.subtract(MatrixUtils.add(M1, M4), M5), M7)
        C12 = MatrixUtils.add(M3, M5)
        C21 = MatrixUtils.add(M2, M4)
        C22 = MatrixUtils.add(MatrixUtils.subtract(MatrixUtils.add(M1, M3), M2), M6)
        
        # Combine quadrants
        result = MatrixUtils.create_matrix(n, n)
        for i in range(mid):
            for j in range(mid):
                result[i][j] = C11[i][j]
                result[i][j + mid] = C12[i][j]
                result[i + mid][j] = C21[i][j]
                result[i + mid][j + mid] = C22[i][j]
        
        return result
    
    @staticmethod
    def print_matrix(A: List[List[float]]) -> None:
        """
        Print matrix in readable format.
        
        Args:
            A: Matrix
        """
        for row in A:
            print("  ".join(f"{val:8.2f}" for val in row))


def main() -> None:
    """Demonstrate matrix utilities."""
    
    print("=== Matrix Utilities Demo ===")
    
    # Create matrices
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    
    print("Matrix A:")
    MatrixUtils.print_matrix(A)
    
    print("\nMatrix B:")
    MatrixUtils.print_matrix(B)
    
    # Addition
    print("\n--- Addition ---")
    C = MatrixUtils.add(A, B)
    MatrixUtils.print_matrix(C)
    
    # Subtraction
    print("\n--- Subtraction ---")
    D = MatrixUtils.subtract(A, B)
    MatrixUtils.print_matrix(D)
    
    # Multiplication
    print("\n--- Multiplication ---")
    E = MatrixUtils.multiply(A, B)
    MatrixUtils.print_matrix(E)
    
    # Scalar multiplication
    print("\n--- Scalar Multiplication ---")
    F = MatrixUtils.scalar_multiply(A, 2)
    MatrixUtils.print_matrix(F)
    
    # Transpose
    print("\n--- Transpose ---")
    G = MatrixUtils.transpose(A)
    MatrixUtils.print_matrix(G)
    
    # Determinant
    print("\n--- Determinant ---")
    det = MatrixUtils.determinant(A)
    print(f"Determinant of A: {det}")
    
    # Identity
    print("\n--- Identity ---")
    I = MatrixUtils.identity(3)
    MatrixUtils.print_matrix(I)
    
    # Power
    print("\n--- Matrix Power ---")
    A_pow = MatrixUtils.power(A, 2)
    print("A^2:")
    MatrixUtils.print_matrix(A_pow)
    
    # Strassen multiplication (power of 2 size)
    print("\n--- Strassen Multiplication ---")
    A2 = [[1, 2], [3, 4]]
    B2 = [[5, 6], [7, 8]]
    print("A2:")
    MatrixUtils.print_matrix(A2)
    print("B2:")
    MatrixUtils.print_matrix(B2)
    C2 = MatrixUtils.strassen_multiply(A2, B2)
    print("A2 * B2 (Strassen):")
    MatrixUtils.print_matrix(C2)


if __name__ == "__main__":
    main()
