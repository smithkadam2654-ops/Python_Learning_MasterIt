"""
Compression Utilities Module

This module provides comprehensive compression utilities including:
- Run-Length Encoding (RLE)
- Huffman coding
- LZW compression
- Delta encoding
- Dictionary-based compression
- Lossless compression
- Compression ratio calculation
- Binary data handling
- Text compression
- File compression utilities

All functions include comprehensive docstrings and type hints.
"""

import heapq
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import struct


class CompressionMethod(Enum):
    """Compression method types."""
    RLE = "rle"
    HUFFMAN = "huffman"
    LZW = "lzw"
    DELTA = "delta"
    DICTIONARY = "dictionary"


@dataclass
class CompressionResult:
    """Container for compression results."""
    original_size: int
    compressed_size: int
    compression_ratio: float
    method: CompressionMethod
    time_ms: float


class RunLengthEncoding:
    """Run-Length Encoding compression."""
    
    @staticmethod
    def encode(data: Union[str, List[int]]) -> List[Tuple]:
        """Encode data using RLE."""
        if not data:
            return []
        
        encoded = []
        
        if isinstance(data, str):
            # RLE for strings
            current_char = data[0]
            count = 1
            
            for char in data[1:]:
                if char == current_char:
                    count += 1
                else:
                    encoded.append((current_char, count))
                    current_char = char
                    count = 1
            
            encoded.append((current_char, count))
        else:
            # RLE for integers
            current_val = data[0]
            count = 1
            
            for val in data[1:]:
                if val == current_val:
                    count += 1
                else:
                    encoded.append((current_val, count))
                    current_val = val
                    count = 1
            
            encoded.append((current_val, count))
        
        return encoded
    
    @staticmethod
    def decode(encoded: List[Tuple]) -> Union[str, List[int]]:
        """Decode RLE encoded data."""
        if not encoded:
            return "" if encoded and isinstance(encoded[0][0], str) else []
        
        decoded = []
        
        for item, count in encoded:
            decoded.extend([item] * count)
        
        if decoded and isinstance(decoded[0], str):
            return "".join(decoded)
        return decoded


class HuffmanCoding:
    """Huffman coding compression."""
    
    @staticmethod
    def build_frequency_table(data: str) -> Dict[str, int]:
        """Build character frequency table."""
        frequency = {}
        for char in data:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency
    
    @staticmethod
    def build_huffman_tree(frequency: Dict[str, int]) -> Optional:
        """Build Huffman tree from frequency table."""
        if not frequency:
            return None
        
        # Create leaf nodes
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            # Pop two smallest
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            
            # Combine
            combined = [a[0] + b[0], a[1], b[1]]
            heapq.heappush(heap, combined)
        
        return heap[0] if heap else None
    
    @staticmethod
    def build_codes(tree, prefix: str = "") -> Dict[str, str]:
        """Build Huffman codes from tree."""
        codes = {}
        
        def traverse(node, code):
            if len(node) == 2:
                codes[node[0]] = code
            else:
                traverse(node[1], code + "0")
                traverse(node[2], code + "1")
        
        if tree:
            traverse(tree, "")
        
        return codes
    
    @staticmethod
    def encode(data: str, codes: Dict[str, str]) -> str:
        """Encode data using Huffman codes."""
        encoded = ""
        for char in data:
            encoded += codes.get(char, char)
        return encoded
    
    @staticmethod
    def decode(encoded: str, codes: Dict[str, str]) -> str:
        """Decode Huffman encoded data."""
        # Build reverse lookup
        reverse_codes = {v: k for k, v in codes.items()}
        
        decoded = ""
        current_code = ""
        
        for bit in encoded:
            current_code += bit
            if current_code in reverse_codes:
                decoded += reverse_codes[current_code]
                current_code = ""
        
        return decoded


class LZWCompression:
    """LZW compression algorithm."""
    
    @staticmethod
    def compress(data: str) -> List[int]:
        """Compress data using LZW algorithm."""
        if not data:
            return []
        
        # Initialize dictionary with single characters
        dictionary = {chr(i): i for i in range(256)}
        next_code = 256
        
        compressed = []
        current = ""
        
        for char in data:
            current += char
            
            if current in dictionary:
                continue
            else:
                compressed.append(dictionary[current[:-1]])
                dictionary[current] = next_code
                next_code += 1
                current = char[-1]
        
        if current:
            compressed.append(dictionary[current])
        
        return compressed
    
    @staticmethod
    def decompress(compressed: List[int]) -> str:
        """Decompress LZW compressed data."""
        if not compressed:
            return ""
        
        # Initialize dictionary
        dictionary = {i: chr(i) for i in range(256)}
        next_code = 256
        
        decompressed = ""
        current = dictionary[compressed[0]]
        
        for code in compressed[1:]:
            if code in dictionary:
                string = dictionary[code]
            else:
                string = current + current[0]
                dictionary[next_code] = string
                next_code += 1
            
            decompressed += current
            current = string
        
        decompressed += current
        return decompressed


class DeltaEncoding:
    """Delta encoding for numerical data."""
    
    @staticmethod
    def encode(data: List[int]) -> List[int]:
        """Encode data using delta encoding."""
        if not data:
            return []
        
        encoded = [data[0]]
        
        for i in range(1, len(data)):
            encoded.append(data[i] - data[i - 1])
        
        return encoded
    
    @staticmethod
    def decode(encoded: List[int]) -> List[int]:
        """Decode delta encoded data."""
        if not encoded:
            return []
        
        decoded = [encoded[0]]
        
        for i in range(1, len(encoded)):
            decoded.append(decoded[i - 1] + encoded[i])
        
        return decoded


class DictionaryCompression:
    """Dictionary-based compression."""
    
    @staticmethod
    def compress(data: List[int]) -> Tuple[List[int], Dict[int, int]]:
        """Compress using dictionary substitution."""
        if not data:
            return [], {}
        
        # Build frequency table
        frequency = {}
        for item in data:
            frequency[item] = frequency.get(item, 0) + 1
        
        # Sort by frequency and create dictionary
        sorted_items = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        dictionary = {item: idx for idx, (item, _) in enumerate(sorted_items)}
        
        # Encode using dictionary indices
        encoded = [dictionary[item] for item in data]
        
        return encoded, dictionary
    
    @staticmethod
    def decode(encoded: List[int], dictionary: Dict[int, int]) -> List[int]:
        """Decode dictionary compressed data."""
        reverse_dict = {v: k for k, v in dictionary.items()}
        return [reverse_dict[idx] for idx in encoded]


class BinaryDataHandler:
    """Binary data handling utilities."""
    
    @staticmethod
    def pack_bits(data: List[int], bits_per_value: int = 8) -> bytes:
        """Pack integer values into bytes."""
        result = bytearray()
        current_byte = 0
        bits_used = 0
        
        for value in data:
            value = value & ((1 << bits_per_value) - 1)
            
            for bit in range(bits_per_value):
                if (value >> bit) & 1:
                    current_byte |= (1 << bits_used)
                
                bits_used += 1
                
                if bits_used == 8:
                    result.append(current_byte)
                    current_byte = 0
                    bits_used = 0
        
        if bits_used > 0:
            result.append(current_byte)
        
        return bytes(result)
    
    @staticmethod
    def unpack_bits(data: bytes, bits_per_value: int = 8) -> List[int]:
        """Unpack bytes into integer values."""
        result = []
        current_value = 0
        bits_used = 0
        
        for byte in data:
            for bit in range(8):
                if (byte >> bit) & 1:
                    current_value |= (1 << bits_used)
                
                bits_used += 1
                
                if bits_used == bits_per_value:
                    result.append(current_value)
                    current_value = 0
                    bits_used = 0
        
        if bits_used > 0:
            result.append(current_value)
        
        return result
    
    @staticmethod
    def bytes_to_hex(data: bytes) -> str:
        """Convert bytes to hex string."""
        return data.hex()
    
    @staticmethod
    def hex_to_bytes(hex_string: str) -> bytes:
        """Convert hex string to bytes."""
        return bytes.fromhex(hex_string)


class TextCompression:
    """Text-specific compression utilities."""
    
    @staticmethod
    def remove_whitespace(text: str) -> str:
        """Remove unnecessary whitespace."""
        return " ".join(text.split())
    
    @staticmethod
    def remove_duplicates(text: str) -> str:
        """Remove duplicate words."""
        words = text.split()
        seen = set()
        result = []
        
        for word in words:
            if word not in seen:
                seen.add(word)
                result.append(word)
        
        return " ".join(result)
    
    @staticmethod
    def replace_common_words(text: str, common_words: List[str],
                            replacement: str = "_") -> str:
        """Replace common words with placeholder."""
        words = text.split()
        common_set = set(common_words)
        
        result = [replacement if word.lower() in common_set else word for word in words]
        return " ".join(result)


class CompressionAnalyzer:
    """Compression analysis utilities."""
    
    @staticmethod
    def calculate_ratio(original_size: int, compressed_size: int) -> float:
        """Calculate compression ratio."""
        if original_size == 0:
            return 0.0
        return (1 - compressed_size / original_size) * 100
    
    @staticmethod
    def calculate_entropy(data: str) -> float:
        """Calculate Shannon entropy of data."""
        if not data:
            return 0.0
        
        frequency = HuffmanCoding.build_frequency_table(data)
        total = len(data)
        entropy = 0.0
        
        for count in frequency.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def analyze_data_type(data: Union[str, List[int]]) -> Dict:
        """Analyze data characteristics."""
        if isinstance(data, str):
            unique_chars = len(set(data))
            frequency = HuffmanCoding.build_frequency_table(data)
            
            return {
                "type": "string",
                "length": len(data),
                "unique_chars": unique_chars,
                "entropy": CompressionAnalyzer.calculate_entropy(data),
                "avg_char_frequency": len(data) / unique_chars if unique_chars > 0 else 0
            }
        else:
            unique_values = len(set(data))
            data_range = max(data) - min(data) if data else 0
            
            return {
                "type": "integer",
                "length": len(data),
                "unique_values": unique_values,
                "range": data_range,
                "min": min(data) if data else 0,
                "max": max(data) if data else 0
            }


class FileCompressor:
    """File compression utilities."""
    
    @staticmethod
    def compress_file(input_path: str, output_path: str,
                      method: CompressionMethod = CompressionMethod.RLE) -> CompressionResult:
        """Compress file using specified method."""
        import time
        start_time = time.time()
        
        with open(input_path, 'rb') as f:
            data = f.read()
        
        original_size = len(data)
        
        if method == CompressionMethod.RLE:
            if isinstance(data, str):
                encoded = RunLengthEncoding.encode(data)
                compressed_data = str(encoded).encode()
            else:
                # Convert to list of bytes for RLE
                byte_list = list(data)
                encoded = RunLengthEncoding.encode(byte_list)
                compressed_data = str(encoded).encode()
        else:
            # Default to storing original for other methods
            compressed_data = data
        
        compressed_size = len(compressed_data)
        compression_ratio = CompressionAnalyzer.calculate_ratio(original_size, compressed_size)
        
        with open(output_path, 'wb') as f:
            f.write(compressed_data)
        
        elapsed = (time.time() - start_time) * 1000
        
        return CompressionResult(
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            method=method,
            time_ms=elapsed
        )
    
    @staticmethod
    def decompress_file(input_path: str, output_path: str,
                        method: CompressionMethod = CompressionMethod.RLE) -> bool:
        """Decompress file."""
        try:
            with open(input_path, 'rb') as f:
                data = f.read().decode()
            
            if method == CompressionMethod.RLE:
                encoded = eval(data)
                decompressed = RunLengthEncoding.decode(encoded)
                if isinstance(decompressed, str):
                    output_data = decompressed
                else:
                    output_data = bytes(decompressed)
            else:
                output_data = data.encode()
            
            with open(output_path, 'wb') as f:
                f.write(output_data)
            
            return True
        except Exception as e:
            print(f"Decompression error: {e}")
            return False


class AdaptiveCompression:
    """Adaptive compression based on data characteristics."""
    
    @staticmethod
    def choose_method(data: Union[str, List[int]]) -> CompressionMethod:
        """Choose best compression method based on data."""
        analysis = CompressionAnalyzer.analyze_data_type(data)
        
        if analysis["type"] == "string":
            # For text, use RLE if many repeated characters
            if analysis["avg_char_frequency"] > 3:
                return CompressionMethod.RLE
            return CompressionMethod.HUFFMAN
        else:
            # For integers, use delta encoding
            return CompressionMethod.DELTA
    
    @staticmethod
    def compress_adaptive(data: Union[str, List[int]]) -> Tuple:
        """Compress using best method."""
        method = AdaptiveCompression.choose_method(data)
        
        if method == CompressionMethod.RLE:
            encoded = RunLengthEncoding.encode(data)
            return encoded, method
        elif method == CompressionMethod.HUFFMAN:
            frequency = HuffmanCoding.build_frequency_table(data)
            tree = HuffmanCoding.build_huffman_tree(frequency)
            codes = HuffmanCoding.build_codes(tree)
            encoded = HuffmanCoding.encode(data, codes)
            return encoded, method
        elif method == CompressionMethod.DELTA:
            encoded = DeltaEncoding.encode(data)
            return encoded, method
        else:
            return data, method


def demonstrate_compression():
    """Demonstrate compression utilities functionality."""
    print("=== Compression Utilities Demonstration ===\n")
    
    # Run-Length Encoding
    print("1. Run-Length Encoding:")
    text = "AAAABBBCCDDEEEE"
    rle_encoded = RunLengthEncoding.encode(text)
    rle_decoded = RunLengthEncoding.decode(rle_encoded)
    
    print(f"   Original: {text}")
    print(f"   Encoded: {rle_encoded}")
    print(f"   Decoded: {rle_decoded}")
    
    numbers = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    rle_numbers = RunLengthEncoding.encode(numbers)
    print(f"   Numbers: {numbers}")
    print(f"   Encoded: {rle_numbers}")
    
    # Huffman Coding
    print("\n2. Huffman Coding:")
    text = "hello world"
    frequency = HuffmanCoding.build_frequency_table(text)
    print(f"   Frequency: {frequency}")
    
    tree = HuffmanCoding.build_huffman_tree(frequency)
    codes = HuffmanCoding.build_codes(tree)
    print(f"   Codes: {codes}")
    
    huffman_encoded = HuffmanCoding.encode(text, codes)
    print(f"   Encoded: {huffman_encoded}")
    
    # LZW Compression
    print("\n3. LZW Compression:")
    lzw_data = "TOBEORNOTTOBEORNOTTOBE"
    lzw_compressed = LZWCompression.compress(lzw_data)
    lzw_decompressed = LZWCompression.decompress(lzw_compressed)
    
    print(f"   Original: {lzw_data}")
    print(f"   Compressed: {lzw_compressed}")
    print(f"   Decompressed: {lzw_decompressed}")
    
    # Delta Encoding
    print("\n4. Delta Encoding:")
    delta_data = [100, 105, 110, 115, 120]
    delta_encoded = DeltaEncoding.encode(delta_data)
    delta_decoded = DeltaEncoding.decode(delta_encoded)
    
    print(f"   Original: {delta_data}")
    print(f"   Encoded: {delta_encoded}")
    print(f"   Decoded: {delta_decoded}")
    
    # Dictionary Compression
    print("\n5. Dictionary Compression:")
    dict_data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    dict_encoded, dictionary = DictionaryCompression.compress(dict_data)
    dict_decoded = DictionaryCompression.decode(dict_encoded, dictionary)
    
    print(f"   Original: {dict_data}")
    print(f"   Encoded: {dict_encoded}")
    print(f"   Dictionary size: {len(dictionary)}")
    print(f"   Decoded: {dict_decoded}")
    
    # Binary Data
    print("\n6. Binary Data Handling:")
    bit_data = [1, 2, 3, 4, 5]
    packed = BinaryDataHandler.pack_bits(bit_data, 3)
    unpacked = BinaryDataHandler.unpack_bits(packed, 3)
    
    print(f"   Original: {bit_data}")
    print(f"   Packed: {BinaryDataHandler.bytes_to_hex(packed)}")
    print(f"   Unpacked: {unpacked}")
    
    # Text Compression
    print("\n7. Text Compression:")
    text_with_spaces = "  This   is  a  test  string  "
    no_whitespace = TextCompression.remove_whitespace(text_with_spaces)
    print(f"   No whitespace: {no_whitespace}")
    
    with_duplicates = "test test this test this is"
    no_duplicates = TextCompression.remove_duplicates(with_duplicates)
    print(f"   No duplicates: {no_duplicates}")
    
    # Compression Analysis
    print("\n8. Compression Analysis:")
    original = "AAAAABBBCCCC"
    compressed = RunLengthEncoding.encode(original)
    
    ratio = CompressionAnalyzer.calculate_ratio(len(original), len(str(compressed)))
    print(f"   Compression ratio: {ratio:.2f}%")
    
    entropy = CompressionAnalyzer.calculate_entropy(original)
    print(f"   Entropy: {entropy:.4f}")
    
    data_analysis = CompressionAnalyzer.analyze_data_type(original)
    print(f"   Data analysis: {data_analysis}")
    
    # Adaptive Compression
    print("\n9. Adaptive Compression:")
    adaptive_data = "AAAAABBBCCCC"
    adaptive_encoded, method = AdaptiveCompression.compress_adaptive(adaptive_data)
    print(f"   Chosen method: {method.value}")
    print(f"   Encoded: {adaptive_encoded}")
    
    # Combined Compression
    print("\n10. Combined Compression:")
    # Delta + RLE
    delta_compressed = DeltaEncoding.encode([10, 12, 12, 12, 15, 15, 15])
    rle_delta = RunLengthEncoding.encode(delta_compressed)
    print(f"   Delta + RLE: {rle_delta}")
    
    print("\n=== Demonstration Complete ===")
    print("\nCompression Best Practices:")
    print("- Choose compression method based on data characteristics")
    print("- RLE is best for repeated consecutive values")
    print("- Huffman is optimal for variable-length symbols")
    print("- LZW is good for repetitive patterns")
    print("- Delta encoding works well for slowly changing values")
    print("- Dictionary compression for repeated sequences")
    print("- Combine methods for better compression ratios")
    print("- Consider decompression speed vs compression ratio")
    print("- Use binary packing for integer data")
    print("- Remove metadata when possible")
    print("- Test compression on representative data")


if __name__ == "__main__":
    import math
    demonstrate_compression()
