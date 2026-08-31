import csv

def csv_operations():
    filename = 'employees.csv'
    
    # 1. Writing to a CSV file
    print(f"--- Writing to {filename} ---")
    headers = ['ID', 'Name', 'Department', 'Salary']
    employees = [
        [101, 'Alice Smith', 'Engineering', 85000],
        [102, 'Bob Jones', 'HR', 60000],
        [103, 'Charlie Brown', 'Marketing', 72000]
    ]
    
    # Use 'w' to write, and newline='' to prevent blank lines on Windows
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers) # Write the header row
        writer.writerows(employees) # Write the data rows
        
    print("CSV file created successfully.\n")
    
    # 2. Reading from a CSV file
    print(f"--- Reading from {filename} ---")
    with open(filename, mode='r') as file:
        # DictReader is fantastic because it reads each row as a dictionary where the keys are the headers!
        reader = csv.DictReader(file)
        
        total_salary = 0
        count = 0
        
        for row in reader:
            print(f"Name: {row['Name']} | Dept: {row['Department']}")
            total_salary += int(row['Salary'])
            count += 1
            
        print(f"\nAverage Salary: ${total_salary / count:.2f}")

if __name__ == "__main__":
    csv_operations()
