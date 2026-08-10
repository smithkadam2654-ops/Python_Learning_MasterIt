# A list of fruits
fruits = ["Apple", "Banana", "Cherry", "Mango"]

# Print each fruit with a number
for index, fruit in enumerate(fruits):
    print(f"{index + 1}. {fruit}")

# Adding a new fruit to the list
fruits.append("Orange")
print(f"Updated list: {fruits}")
