"""
Strategy Pattern - Strategy pattern for interchangeable algorithms.
Features: Strategy interface, context management, and runtime strategy switching.
"""

from typing import List, Callable, Any
from dataclasses import dataclass
from enum import Enum


class SortStrategy:
    """Base sorting strategy."""
    
    def sort(self, data: List) -> List:
        """Sort the data."""
        raise NotImplementedError


class BubbleSort(SortStrategy):
    """Bubble sort strategy."""
    
    def sort(self, data: List) -> List:
        """Sort using bubble sort."""
        result = data.copy()
        n = len(result)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        
        return result


class QuickSort(SortStrategy):
    """Quick sort strategy."""
    
    def sort(self, data: List) -> List:
        """Sort using quick sort."""
        result = data.copy()
        self._quicksort(result, 0, len(result) - 1)
        return result
    
    def _quicksort(self, arr: List, low: int, high: int) -> None:
        """Quick sort helper."""
        if low < high:
            pi = self._partition(arr, low, high)
            self._quicksort(arr, low, pi - 1)
            self._quicksort(arr, pi + 1, high)
    
    def _partition(self, arr: List, low: int, high: int) -> int:
        """Partition helper."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


class MergeSort(SortStrategy):
    """Merge sort strategy."""
    
    def sort(self, data: List) -> List:
        """Sort using merge sort."""
        result = data.copy()
        return self._mergesort(result)
    
    def _mergesort(self, arr: List) -> List:
        """Merge sort helper."""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._mergesort(arr[:mid])
        right = self._mergesort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List, right: List) -> List:
        """Merge helper."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class SortContext:
    """Context for sorting with strategy."""
    
    def __init__(self, strategy: SortStrategy) -> None:
        """
        Initialize context.
        
        Args:
            strategy: Initial sorting strategy
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        """
        Change sorting strategy.
        
        Args:
            strategy: New sorting strategy
        """
        self._strategy = strategy
    
    def sort(self, data: List) -> List:
        """
        Sort data using current strategy.
        
        Args:
            data: Data to sort
            
        Returns:
            Sorted data
        """
        return self._strategy.sort(data)


class PaymentStrategy:
    """Base payment strategy."""
    
    def pay(self, amount: float) -> str:
        """Process payment."""
        raise NotImplementedError


class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy."""
    
    def __init__(self, card_number: str, expiry: str) -> None:
        """
        Initialize credit card payment.
        
        Args:
            card_number: Card number
            expiry: Expiry date
        """
        self.card_number = card_number
        self.expiry = expiry
    
    def pay(self, amount: float) -> str:
        """Pay with credit card."""
        return f"Paid ${amount:.2f} with credit card ending in {self.card_number[-4:]}"


class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy."""
    
    def __init__(self, email: str) -> None:
        """
        Initialize PayPal payment.
        
        Args:
            email: PayPal email
        """
        self.email = email
    
    def pay(self, amount: float) -> str:
        """Pay with PayPal."""
        return f"Paid ${amount:.2f} via PayPal ({self.email})"


class BankTransferPayment(PaymentStrategy):
    """Bank transfer payment strategy."""
    
    def __init__(self, account_number: str, bank_name: str) -> None:
        """
        Initialize bank transfer payment.
        
        Args:
            account_number: Bank account number
            bank_name: Bank name
        """
        self.account_number = account_number
        self.bank_name = bank_name
    
    def pay(self, amount: float) -> str:
        """Pay with bank transfer."""
        return f"Paid ${amount:.2f} via bank transfer from {self.bank_name}"


class PaymentContext:
    """Context for payment processing."""
    
    def __init__(self, strategy: PaymentStrategy) -> None:
        """
        Initialize payment context.
        
        Args:
            strategy: Initial payment strategy
        """
        self._strategy = strategy
    
    def set_payment_method(self, strategy: PaymentStrategy) -> None:
        """
        Change payment method.
        
        Args:
            strategy: New payment strategy
        """
        self._strategy = strategy
    
    def process_payment(self, amount: float) -> str:
        """
        Process payment using current strategy.
        
        Args:
            amount: Amount to pay
            
        Returns:
            Payment result
        """
        return self._strategy.pay(amount)


class CompressionStrategy:
    """Base compression strategy."""
    
    def compress(self, data: str) -> str:
        """Compress data."""
        raise NotImplementedError
    
    def decompress(self, data: str) -> str:
        """Decompress data."""
        raise NotImplementedError


class RunLengthEncoding(CompressionStrategy):
    """Run-length encoding compression."""
    
    def compress(self, data: str) -> str:
        """Compress using RLE."""
        if not data:
            return ""
        
        result = []
        count = 1
        
        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                count += 1
            else:
                result.append(f"{data[i - 1]}{count}")
                count = 1
        
        result.append(f"{data[-1]}{count}")
        return "".join(result)
    
    def decompress(self, data: str) -> str:
        """Decompress RLE."""
        result = []
        i = 0
        
        while i < len(data):
            char = data[i]
            i += 1
            count_str = ""
            
            while i < len(data) and data[i].isdigit():
                count_str += data[i]
                i += 1
            
            count = int(count_str) if count_str else 1
            result.append(char * count)
        
        return "".join(result)


class SimpleCompression(CompressionStrategy):
    """Simple compression (removes spaces)."""
    
    def compress(self, data: str) -> str:
        """Compress by removing spaces."""
        return data.replace(" ", "")
    
    def decompress(self, data: str) -> str:
        """Decompress (cannot restore spaces)."""
        return data  # Lossy compression


class CompressionContext:
    """Context for compression."""
    
    def __init__(self, strategy: CompressionStrategy) -> None:
        """
        Initialize compression context.
        
        Args:
            strategy: Initial compression strategy
        """
        self._strategy = strategy
    
    def set_compression_method(self, strategy: CompressionStrategy) -> None:
        """
        Change compression method.
        
        Args:
            strategy: New compression strategy
        """
        self._strategy = strategy
    
    def compress(self, data: str) -> str:
        """Compress data."""
        return self._strategy.compress(data)
    
    def decompress(self, data: str) -> str:
        """Decompress data."""
        return self._strategy.decompress(data)


def main() -> None:
    """Demonstrate strategy pattern."""
    
    print("=== Sorting Strategies ===")
    data = [64, 34, 25, 12, 22, 11, 90]
    
    print(f"Original: {data}")
    
    # Bubble sort
    context = SortContext(BubbleSort())
    sorted_bubble = context.sort(data)
    print(f"Bubble sort: {sorted_bubble}")
    
    # Quick sort
    context.set_strategy(QuickSort())
    sorted_quick = context.sort(data)
    print(f"Quick sort: {sorted_quick}")
    
    # Merge sort
    context.set_strategy(MergeSort())
    sorted_merge = context.sort(data)
    print(f"Merge sort: {sorted_merge}")
    
    print("\n=== Payment Strategies ===")
    
    # Credit card
    payment_context = PaymentContext(
        CreditCardPayment("1234567890123456", "12/25")
    )
    print(payment_context.process_payment(100.50))
    
    # PayPal
    payment_context.set_payment_method(PayPalPayment("user@example.com"))
    print(payment_context.process_payment(75.25))
    
    # Bank transfer
    payment_context.set_payment_method(
        BankTransferPayment("9876543210", "Chase Bank")
    )
    print(payment_context.process_payment(250.00))
    
    print("\n=== Compression Strategies ===")
    
    text = "AAAABBBCCDAA"
    
    # RLE
    compression_context = CompressionContext(RunLengthEncoding())
    compressed = compression_context.compress(text)
    decompressed = compression_context.decompress(compressed)
    
    print(f"Original: {text}")
    print(f"Compressed (RLE): {compressed}")
    print(f"Decompressed: {decompressed}")
    
    # Simple compression
    compression_context.set_compression_method(SimpleCompression())
    text_with_spaces = "Hello World from Python"
    compressed = compression_context.compress(text_with_spaces)
    decompressed = compression_context.decompress(compressed)
    
    print(f"\nOriginal: {text_with_spaces}")
    print(f"Compressed (Simple): {compressed}")
    print(f"Decompressed: {depressed}")
    
    print("\n=== Runtime Strategy Selection ===")
    
    def select_sort_strategy(data_size: int) -> SortStrategy:
        """Select strategy based on data size."""
        if data_size < 10:
            return BubbleSort()
        elif data_size < 100:
            return QuickSort()
        else:
            return MergeSort()
    
    small_data = [3, 1, 4, 1, 5]
    large_data = list(range(100, 0, -1))
    
    context.set_strategy(select_sort_strategy(len(small_data)))
    print(f"Small data sorted: {context.sort(small_data)}")
    
    context.set_strategy(select_sort_strategy(len(large_data)))
    print(f"Large data sorted (first 10): {context.sort(large_data)[:10]}")


if __name__ == "__main__":
    main()
