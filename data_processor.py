import csv
import statistics
from collections import defaultdict
from typing import Iterator, Dict, List, Any

def process_data(file_path: str) -> Dict[str, float]:
    """Reads a CSV, groups by a column, and calculates the mean of another column."""
    grouped_data = defaultdict(list)
    
    # Simulating data reading and processing with a generator
    def read_records() -> Iterator[Dict[str, str]]:
        # In a real scenario, this would be:
        # with open(file_path, mode='r') as f:
        #     reader = csv.DictReader(f)
        #     yield from reader
        
        # Dummy data for demonstration
        dummy_data = [
            {"category": "A", "value": "10.5"},
            {"category": "B", "value": "20.1"},
            {"category": "A", "value": "15.2"},
            {"category": "C", "value": "5.5"},
            {"category": "B", "value": "22.0"},
            {"category": "A", "value": "12.8"}
        ]
        yield from dummy_data

    for record in read_records():
        try:
            category = record["category"]
            value = float(record["value"])
            grouped_data[category].append(value)
        except (KeyError, ValueError) as e:
            print(f"Error processing record {record}: {e}")
            
    results = {}
    for category, values in grouped_data.items():
        results[category] = statistics.mean(values)
        
    return results

if __name__ == "__main__":
    print("Processing Data...")
    means = process_data("dummy.csv")
    for cat, mean_val in means.items():
        print(f"Category {cat}: Mean = {mean_val:.2f}")
