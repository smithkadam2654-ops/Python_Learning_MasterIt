class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
    def make_sound(self):
        # A generic sound, to be overridden by subclasses
        return "Some generic animal sound"
        
    def description(self):
        return f"{self.name} is a {self.species}."

class Dog(Animal):
    def __init__(self, name, breed):
        # Call the __init__ of the parent class
        super().__init__(name, species="Dog")
        self.breed = breed
        
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, species="Cat")
        self.color = color
        
    def make_sound(self):
        return "Meow!"

def main():
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers", "Black")
    
    animals = [dog, cat]
    
    for animal in animals:
        print(animal.description())
        if hasattr(animal, 'breed'):
            print(f"Breed: {animal.breed}")
        elif hasattr(animal, 'color'):
            print(f"Color: {animal.color}")
        print(f"Sound: {animal.make_sound()}\n")

if __name__ == "__main__":
    main()
