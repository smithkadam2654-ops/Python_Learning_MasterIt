class Animal:
    """A base class representing an animal."""
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        """Generic sound method to be overridden by subclasses."""
        return "Some generic animal sound"

    def describe(self):
        return f"{self.name} is a {self.species}."

class Dog(Animal):
    """A derived class representing a dog."""
    def __init__(self, name, breed):
        super().__init__(name, species="Dog")
        self.breed = breed

    def make_sound(self):
        return "Woof! Woof!"

    def describe(self):
        return f"{self.name} is a {self.breed} (Dog)."

class Cat(Animal):
    """A derived class representing a cat."""
    def __init__(self, name, color):
        super().__init__(name, species="Cat")
        self.color = color

    def make_sound(self):
        return "Meow!"

# Example usage
if __name__ == "__main__":
    # Create instances of our classes
    generic_animal = Animal("Creature", "Unknown")
    my_dog = Dog("Buddy", "Golden Retriever")
    my_cat = Cat("Whiskers", "Black")

    # Put them in a list and demonstrate polymorphism
    animals = [generic_animal, my_dog, my_cat]

    for animal in animals:
        print(animal.describe())
        print(f"Sound: {animal.make_sound()}\n")
