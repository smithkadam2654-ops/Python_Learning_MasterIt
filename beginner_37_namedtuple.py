from collections import namedtuple

def main():
    # Tuples are great, but accessing items by index (e.g., pt[0]) can be confusing.
    # A namedtuple lets you access tuple elements by name as well as by index.
    
    # Define a namedtuple called 'Point' with fields 'x' and 'y'
    Point = namedtuple('Point', ['x', 'y'])
    
    # Create instances
    p1 = Point(10, 20)
    p2 = Point(x=30, y=40)
    
    print(f"Point 1: {p1}")
    
    # Accessing by name
    print(f"p1 X-coordinate: {p1.x}")
    print(f"p1 Y-coordinate: {p1.y}")
    
    # You can still access by index!
    print(f"p2 using index [0]: {p2[0]}")
    
    # Unpacking works too
    x_val, y_val = p1
    print(f"Unpacked p1: x={x_val}, y={y_val}")

if __name__ == "__main__":
    main()
