class Dog:
    """A simple class representing a dog."""
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        
    def bark(self):
        return f"{self.name} says Woof!"
        
def main():
    # Creating objects (instances) of the Dog class
    my_dog = Dog("Buddy", "Golden Retriever")
    neighbor_dog = Dog("Max", "Bulldog")
    
    print(my_dog.bark())
    print(neighbor_dog.bark())

if __name__ == "__main__":
    main()
