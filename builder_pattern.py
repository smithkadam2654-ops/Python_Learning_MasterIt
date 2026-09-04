"""
Builder Pattern - Builder pattern for complex object construction.
Features: Step-by-step construction, fluent interface, and immutable objects.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class House:
    """House product."""
    walls: int = 4
    doors: int = 1
    windows: int = 2
    has_garage: bool = False
    has_garden: bool = False
    has_pool: bool = False
    color: str = "white"
    roof_type: str = "flat"
    
    def __str__(self) -> str:
        """String representation."""
        features = []
        features.append(f"{self.walls} walls")
        features.append(f"{self.doors} doors")
        features.append(f"{self.windows} windows")
        if self.has_garage:
            features.append("garage")
        if self.has_garden:
            features.append("garden")
        if self.has_pool:
            features.append("pool")
        features.append(f"{self.color} color")
        features.append(f"{self.roof_type} roof")
        return f"House with {', '.join(features)}"


class HouseBuilder:
    """Builder for constructing houses."""
    
    def __init__(self) -> None:
        """Initialize builder."""
        self._walls = 4
        self._doors = 1
        self._windows = 2
        self._has_garage = False
        self._has_garden = False
        self._has_pool = False
        self._color = "white"
        self._roof_type = "flat"
    
    def set_walls(self, count: int) -> 'HouseBuilder':
        """Set number of walls."""
        self._walls = count
        return self
    
    def set_doors(self, count: int) -> 'HouseBuilder':
        """Set number of doors."""
        self._doors = count
        return self
    
    def set_windows(self, count: int) -> 'HouseBuilder':
        """Set number of windows."""
        self._windows = count
        return self
    
    def add_garage(self) -> 'HouseBuilder':
        """Add garage."""
        self._has_garage = True
        return self
    
    def add_garden(self) -> 'HouseBuilder':
        """Add garden."""
        self._has_garden = True
        return self
    
    def add_pool(self) -> 'HouseBuilder':
        """Add pool."""
        self._has_pool = True
        return self
    
    def set_color(self, color: str) -> 'HouseBuilder':
        """Set house color."""
        self._color = color
        return self
    
    def set_roof_type(self, roof_type: str) -> 'HouseBuilder':
        """Set roof type."""
        self._roof_type = roof_type
        return self
    
    def build(self) -> House:
        """Build the house."""
        return House(
            walls=self._walls,
            doors=self._doors,
            windows=self._windows,
            has_garage=self._has_garage,
            has_garden=self._has_garden,
            has_pool=self._has_pool,
            color=self._color,
            roof_type=self._roof_type
        )


class HouseDirector:
    """Director for constructing predefined house types."""
    
    def __init__(self, builder: HouseBuilder) -> None:
        """
        Initialize director.
        
        Args:
            builder: House builder to use
        """
        self._builder = builder
    
    def build_simple_house(self) -> House:
        """Build a simple house."""
        return self._builder.set_walls(4).set_doors(1).set_windows(2).build()
    
    def build_luxury_house(self) -> House:
        """Build a luxury house."""
        return (self._builder
                .set_walls(6)
                .set_doors(3)
                .set_windows(8)
                .add_garage()
                .add_garden()
                .add_pool()
                .set_color("gold")
                .set_roof_type("slanted")
                .build())
    
    def build_cottage(self) -> House:
        """Build a cottage."""
        return (self._builder
                .set_walls(4)
                .set_doors(1)
                .set_windows(4)
                .add_garden()
                .set_color("brown")
                .set_roof_type("thatched")
                .build())


@dataclass
class Computer:
    """Computer product."""
    cpu: str = "Intel i3"
    ram: int = 8
    storage: int = 256
    gpu: Optional[str] = None
    has_wifi: bool = False
    has_bluetooth: bool = False
    os: str = "Windows"
    
    def __str__(self) -> str:
        """String representation."""
        specs = [f"CPU: {self.cpu}", f"RAM: {self.ram}GB", f"Storage: {self.storage}GB"]
        if self.gpu:
            specs.append(f"GPU: {self.gpu}")
        if self.has_wifi:
            specs.append("WiFi")
        if self.has_bluetooth:
            specs.append("Bluetooth")
        specs.append(f"OS: {self.os}")
        return f"Computer [{', '.join(specs)}]"


class ComputerBuilder:
    """Builder for constructing computers."""
    
    def __init__(self) -> None:
        """Initialize builder."""
        self._cpu = "Intel i3"
        self._ram = 8
        self._storage = 256
        self._gpu = None
        self._has_wifi = False
        self._has_bluetooth = False
        self._os = "Windows"
    
    def set_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Set CPU."""
        self._cpu = cpu
        return self
    
    def set_ram(self, ram: int) -> 'ComputerBuilder':
        """Set RAM."""
        self._ram = ram
        return self
    
    def set_storage(self, storage: int) -> 'ComputerBuilder':
        """Set storage."""
        self._storage = storage
        return self
    
    def set_gpu(self, gpu: str) -> 'ComputerBuilder':
        """Set GPU."""
        self._gpu = gpu
        return self
    
    def add_wifi(self) -> 'ComputerBuilder':
        """Add WiFi."""
        self._has_wifi = True
        return self
    
    def add_bluetooth(self) -> 'ComputerBuilder':
        """Add Bluetooth."""
        self._has_bluetooth = True
        return self
    
    def set_os(self, os: str) -> 'ComputerBuilder':
        """Set operating system."""
        self._os = os
        return self
    
    def build(self) -> Computer:
        """Build the computer."""
        return Computer(
            cpu=self._cpu,
            ram=self._ram,
            storage=self._storage,
            gpu=self._gpu,
            has_wifi=self._has_wifi,
            has_bluetooth=self._has_bluetooth,
            os=self._os
        )


@dataclass
class Pizza:
    """Pizza product."""
    size: str = "medium"
    crust: str = "thin"
    sauce: str = "tomato"
    cheese: str = "mozzarella"
    toppings: List[str] = None
    
    def __post_init__(self):
        if self.toppings is None:
            self.toppings = []
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.size} {self.crust} crust pizza with {self.sauce} sauce, {self.cheese} cheese, and {', '.join(self.toppings) if self.toppings else 'no toppings'}"


class PizzaBuilder:
    """Builder for constructing pizzas."""
    
    def __init__(self) -> None:
        """Initialize builder."""
        self._size = "medium"
        self._crust = "thin"
        self._sauce = "tomato"
        self._cheese = "mozzarella"
        self._toppings: List[str] = []
    
    def set_size(self, size: str) -> 'PizzaBuilder':
        """Set pizza size."""
        self._size = size
        return self
    
    def set_crust(self, crust: str) -> 'PizzaBuilder':
        """Set crust type."""
        self._crust = crust
        return self
    
    def set_sauce(self, sauce: str) -> 'PizzaBuilder':
        """Set sauce type."""
        self._sauce = sauce
        return self
    
    def set_cheese(self, cheese: str) -> 'PizzaBuilder':
        """Set cheese type."""
        self._cheese = cheese
        return self
    
    def add_topping(self, topping: str) -> 'PizzaBuilder':
        """Add topping."""
        self._toppings.append(topping)
        return self
    
    def add_toppings(self, toppings: List[str]) -> 'PizzaBuilder':
        """Add multiple toppings."""
        self._toppings.extend(toppings)
        return self
    
    def build(self) -> Pizza:
        """Build the pizza."""
        return Pizza(
            size=self._size,
            crust=self._crust,
            sauce=self._sauce,
            cheese=self._cheese,
            toppings=self._toppings.copy()
        )


def main() -> None:
    """Demonstrate builder pattern."""
    
    print("=== House Builder ===")
    builder = HouseBuilder()
    
    # Build custom house
    custom_house = (builder
                    .set_walls(5)
                    .set_doors(2)
                    .set_windows(6)
                    .add_garage()
                    .set_color("blue")
                    .build())
    
    print(f"Custom house: {custom_house}")
    
    # Use director for predefined houses
    director = HouseDirector(HouseBuilder())
    
    simple_house = director.build_simple_house()
    print(f"\nSimple house: {simple_house}")
    
    luxury_house = director.build_luxury_house()
    print(f"Luxury house: {luxury_house}")
    
    cottage = director.build_cottage()
    print(f"Cottage: {cottage}")
    
    print("\n=== Computer Builder ===")
    comp_builder = ComputerBuilder()
    
    # Build gaming PC
    gaming_pc = (comp_builder
                 .set_cpu("Intel i9")
                 .set_ram(32)
                 .set_storage(1000)
                 .set_gpu("NVIDIA RTX 4090")
                 .add_wifi()
                 .add_bluetooth()
                 .build())
    
    print(f"Gaming PC: {gaming_pc}")
    
    # Build office PC
    office_pc = (ComputerBuilder()
                .set_cpu("Intel i5")
                .set_ram(16)
                .set_storage(512)
                .add_wifi()
                .build())
    
    print(f"Office PC: {office_pc}")
    
    # Build budget PC
    budget_pc = (ComputerBuilder()
               .set_cpu("AMD Ryzen 3")
               .set_ram(8)
               .set_storage(256)
               .build())
    
    print(f"Budget PC: {budget_pc}")
    
    print("\n=== Pizza Builder ===")
    pizza_builder = PizzaBuilder()
    
    # Build custom pizza
    custom_pizza = (pizza_builder
                   .set_size("large")
                   .set_crust("thick")
                   .set_sauce("bbq")
                   .set_cheese("cheddar")
                   .add_toppings(["pepperoni", "mushrooms", "olives"])
                   .build())
    
    print(f"Custom pizza: {custom_pizza}")
    
    # Build margherita
    margherita = (PizzaBuilder()
                 .set_size("medium")
                 .set_crust("thin")
                 .set_sauce("tomato")
                 .set_cheese("mozzarella")
                 .add_toppings(["basil"])
                 .build())
    
    print(f"Margherita: {margherita}")
    
    # Build meat lovers
    meat_lovers = (PizzaBuilder()
                  .set_size("large")
                  .set_crust("thick")
                  .add_toppings(["pepperoni", "sausage", "bacon", "ham"])
                  .build())
    
    print(f"Meat lovers: {meat_lovers}")
    
    print("\n=== Fluent Interface Benefits ===")
    # Compare with non-builder approach
    print("\nWithout builder (many parameters):")
    house_no_builder = House(walls=4, doors=2, windows=4, has_garage=True, 
                            has_garden=False, has_pool=False, color="red", roof_type="gabled")
    print(house_no_builder)
    
    print("\nWith builder (clear and flexible):")
    house_with_builder = (HouseBuilder()
                         .set_walls(4)
                         .set_doors(2)
                         .set_windows(4)
                         .add_garage()
                         .set_color("red")
                         .set_roof_type("gabled")
                         .build())
    print(house_with_builder)


if __name__ == "__main__":
    main()
