import math
import statistics

def math_and_stats():
    # --- Math Module ---
    print("--- Math Module Operations ---")
    radius = 5
    # Calculate area of a circle (pi * r^2)
    area = math.pi * math.pow(radius, 2)
    print(f"Area of circle with radius {radius}: {area:.2f}")
    
    # Trigonometry and logarithms
    print(f"Sine of 90 degrees: {math.sin(math.radians(90))}")
    print(f"Base-10 Logarithm of 100: {math.log10(100)}")
    
    # --- Statistics Module ---
    print("\n--- Statistics Module Operations ---")
    data = [15, 22, 14, 22, 35, 18, 22, 40, 15]
    print(f"Data Set: {data}")
    
    print(f"Mean (Average): {statistics.mean(data):.2f}")
    print(f"Median (Middle value): {statistics.median(data)}")
    print(f"Mode (Most common): {statistics.mode(data)}")
    print(f"Standard Deviation: {statistics.stdev(data):.2f}")

if __name__ == "__main__":
    math_and_stats()
