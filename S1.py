# Check if a person is old enough to vote
age = int(input("Enter your age: ")) # We use int() because input() always returns text

if age >= 18:
    print("You are eligible to vote!")
elif age > 0:
    print("You are too young to vote yet.")
else:
    print("Please enter a valid age.")
