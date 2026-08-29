import struct

def demonstrate_struct():
    """Demonstrate packing and unpacking binary data using the struct module."""
    
    print("--- 1. Packing Data into Binary ---")
    # Let's say we want to pack an integer, a float, and a boolean
    # Format string:
    # 'i' = integer (4 bytes)
    # 'f' = float (4 bytes)
    # '?' = boolean (1 byte)
    format_string = 'if?'
    
    original_data = (42, 3.14159, True)
    print(f"Original Data: {original_data}")
    
    # Pack the data into a binary bytes object
    packed_data = struct.pack(format_string, *original_data)
    
    print(f"Packed Binary Data: {packed_data}")
    print(f"Size of packed data: {len(packed_data)} bytes")
    print(f"Calculated size from format: {struct.calcsize(format_string)} bytes")
    
    print("\n--- 2. Unpacking Binary Data ---")
    # Now let's unpack that binary data back into Python objects
    unpacked_data = struct.unpack(format_string, packed_data)
    
    print(f"Unpacked Data: {unpacked_data}")
    
    # Notice that the float might lose a tiny bit of precision due to how floats are stored in binary!
    # 3.14159 might become 3.141590118408203
    print(f"Is the integer the same? {unpacked_data[0] == 42}")

if __name__ == "__main__":
    demonstrate_struct()
