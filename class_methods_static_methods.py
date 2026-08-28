class Employee:
    # Class variable
    raise_amount = 1.05
    num_of_emps = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        Employee.num_of_emps += 1

    def fullname(self):
        """Regular instance method. Automatically takes the instance ('self') as the first argument."""
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        """Class method. Automatically takes the class ('cls') as the first argument."""
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):
        """Alternative constructor using a class method."""
        first, last, pay = emp_str.split('-')
        return cls(first, last, float(pay))

    @staticmethod
    def is_workday(day):
        """Static method. Doesn't take 'self' or 'cls'. Just a regular function bound to the class namespace."""
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

def demonstrate_methods():
    import datetime
    
    emp_1 = Employee('Corey', 'Schafer', 50000)
    emp_2 = Employee('Test', 'User', 60000)

    print("--- Class Methods ---")
    # Using class method to change class variable for all instances
    Employee.set_raise_amt(1.10)
    print(f"Raise amount set to {Employee.raise_amount}")
    print(f"Emp 1 raise amount: {emp_1.raise_amount}")
    
    print("\n--- Alternative Constructor (Class Method) ---")
    emp_str_3 = 'John-Doe-70000'
    new_emp_3 = Employee.from_string(emp_str_3)
    print(f"Created new employee from string: {new_emp_3.fullname()} - ${new_emp_3.pay}")

    print("\n--- Static Methods ---")
    my_date = datetime.date(2023, 10, 14) # A Saturday
    print(f"Is {my_date} a workday? {Employee.is_workday(my_date)}")

if __name__ == "__main__":
    demonstrate_methods()
