# This script demonstrates control flow structures like if-else and loops.

# If-Else Statement
number = 15
if number % 2 == 0:
    print(f"{number} is an even number.")
else:
    print(f"{number} is an odd number.")

print("\n--- For Loop ---")
# For Loop
# Iterating over a list of fruits
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}s!")

print("\n--- While Loop ---")
# While Loop
count = 3
while count > 0:
    print(count)
    count -= 1
print("Blastoff!")
