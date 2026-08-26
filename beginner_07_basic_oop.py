class Dog:
    # The __init__ method initializes the object's attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # A method that belongs to the Dog class
    def bark(self):
        print(f"{self.name} says Woof!")

    def introduce(self):
        print(f"This is {self.name}, and they are {self.age} years old.")

if __name__ == "__main__":
    # Creating an instance of the Dog class
    my_dog = Dog("Buddy", 3)
    
    # Accessing methods
    my_dog.introduce()
    my_dog.bark()
