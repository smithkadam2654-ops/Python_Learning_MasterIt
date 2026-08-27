import csv
import os

def demonstrate_csv_handling():
    """Demonstrate reading and writing CSV files."""
    filename = 'employees.csv'
    
    # 1. Writing to a CSV file
    print("Writing data to CSV...")
    employees = [
        ['Name', 'Department', 'Salary'],
        ['John Doe', 'Engineering', '75000'],
        ['Jane Smith', 'Marketing', '65000'],
        ['Emily Davis', 'HR', '55000']
    ]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(employees)
        
    # 2. Reading from a CSV file
    print("\nReading data from CSV:")
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Skip the header row
        header = next(reader)
        print(f"Columns: {', '.join(header)}")
        
        for row in reader:
            print(f"- {row[0]} works in {row[1]} and makes ${row[2]}")
            
    # 3. Using DictReader and DictWriter (often more convenient)
    print("\nReading data using DictReader:")
    with open(filename, mode='r') as file:
        dict_reader = csv.DictReader(file)
        for row in dict_reader:
            # We can now access columns by their header names!
            print(f"{row['Name']} -> {row['Department']}")
            
    # Clean up
    os.remove(filename)
    print("\nCleaned up the CSV file.")

if __name__ == "__main__":
    demonstrate_csv_handling()
