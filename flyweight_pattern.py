"""
Flyweight Pattern - Flyweight pattern for sharing objects.
Features: Intrinsic/extrinsic state, object sharing, and memory efficiency.
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class TreeType(Enum):
    """Tree types."""
    OAK = "oak"
    PINE = "pine"
    MAPLE = "maple"
    BIRCH = "birch"


@dataclass
class TreeProperties:
    """Intrinsic state of a tree (shared)."""
    tree_type: TreeType
    color: str
    texture: str
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.tree_type.value} tree ({self.color}, {self.texture})"


class TreeFactory:
    """Factory for creating and sharing tree objects."""
    
    def __init__(self) -> None:
        """Initialize tree factory."""
        self._tree_pool: Dict[str, TreeProperties] = {}
    
    def get_tree(self, tree_type: TreeType, color: str, texture: str) -> TreeProperties:
        """
        Get tree from pool or create new one.
        
        Args:
            tree_type: Type of tree
            color: Tree color
            texture: Tree texture
            
        Returns:
            Tree properties (shared)
        """
        key = f"{tree_type.value}_{color}_{texture}"
        
        if key not in self._tree_pool:
            self._tree_pool[key] = TreeProperties(tree_type, color, texture)
            print(f"Creating new tree: {key}")
        else:
            print(f"Reusing existing tree: {key}")
        
        return self._tree_pool[key]
    
    def get_pool_size(self) -> int:
        """Get number of unique trees in pool."""
        return len(self._tree_pool)


class Tree:
    """Tree with extrinsic state (position)."""
    
    def __init__(self, x: int, y: int, properties: TreeProperties) -> None:
        """
        Initialize tree.
        
        Args:
            x: X position
            y: Y position
            properties: Shared tree properties
        """
        self.x = x
        self.y = y
        self.properties = properties
    
    def display(self) -> str:
        """Display tree."""
        return f"Tree at ({self.x}, {self.y}): {self.properties}"


class Forest:
    """Forest containing many trees."""
    
    def __init__(self) -> None:
        """Initialize forest."""
        self._trees: List[Tree] = []
        self._factory = TreeFactory()
    
    def plant_tree(self, x: int, y: int, tree_type: TreeType, 
                   color: str, texture: str) -> None:
        """
        Plant a tree in the forest.
        
        Args:
            x: X position
            y: Y position
            tree_type: Type of tree
            color: Tree color
            texture: Tree texture
        """
        properties = self._factory.get_tree(tree_type, color, texture)
        tree = Tree(x, y, properties)
        self._trees.append(tree)
    
    def display(self) -> None:
        """Display all trees in forest."""
        for tree in self._trees:
            print(tree.display())
    
    def get_tree_count(self) -> int:
        """Get total number of trees."""
        return len(self._trees)
    
    def get_unique_tree_count(self) -> int:
        """Get number of unique tree types."""
        return self._factory.get_pool_size()


class CharacterStyle:
    """Character style (intrinsic state)."""
    
    def __init__(self, font: str, size: int, color: str) -> None:
        """
        Initialize character style.
        
        Args:
            font: Font family
            size: Font size
            color: Font color
        """
        self.font = font
        self.size = size
        self.color = color
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.font} {size}pt {self.color}"
    
    def __hash__(self) -> int:
        """Hash for dictionary key."""
        return hash((self.font, self.size, self.color))
    
    def __eq__(self, other) -> bool:
        """Equality check."""
        if not isinstance(other, CharacterStyle):
            return False
        return (self.font == other.font and 
                self.size == other.size and 
                self.color == other.color)


class CharacterStyleFactory:
    """Factory for character styles."""
    
    def __init__(self) -> None:
        """Initialize factory."""
        self._styles: Dict[tuple, CharacterStyle] = {}
    
    def get_style(self, font: str, size: int, color: str) -> CharacterStyle:
        """
        Get style from pool or create new one.
        
        Args:
            font: Font family
            size: Font size
            color: Font color
            
        Returns:
            Character style (shared)
        """
        key = (font, size, color)
        
        if key not in self._styles:
            self._styles[key] = CharacterStyle(font, size, color)
            print(f"Creating new style: {key}")
        else:
            print(f"Reusing existing style: {key}")
        
        return self._styles[key]
    
    def get_style_count(self) -> int:
        """Get number of unique styles."""
        return len(self._styles)


class Character:
    """Character with extrinsic state (position)."""
    
    def __init__(self, char: str, style: CharacterStyle) -> None:
        """
        Initialize character.
        
        Args:
            char: Character
            style: Shared character style
        """
        self.char = char
        self.style = style
    
    def display(self) -> str:
        """Display character."""
        return f"'{self.char}' ({self.style})"


class Document:
    """Document containing characters."""
    
    def __init__(self) -> None:
        """Initialize document."""
        self._characters: List[Character] = []
        self._style_factory = CharacterStyleFactory()
    
    def add_character(self, char: str, font: str, size: int, color: str) -> None:
        """
        Add character to document.
        
        Args:
            char: Character
            font: Font family
            size: Font size
            color: Font color
        """
        style = self._style_factory.get_style(font, size, color)
        character = Character(char, style)
        self._characters.append(character)
    
    def display(self) -> None:
        """Display document."""
        for character in self._characters:
            print(character.display())
    
    def get_character_count(self) -> int:
        """Get total character count."""
        return len(self._characters)
    
    def get_unique_style_count(self) -> int:
        """Get number of unique styles."""
        return self._style_factory.get_style_count()


class ParticleType:
    """Particle type (intrinsic state)."""
    
    def __init__(self, name: str, color: str, size: float) -> None:
        """
        Initialize particle type.
        
        Args:
            name: Particle name
            color: Particle color
            size: Particle size
        """
        self.name = name
        self.color = color
        self.size = size
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} ({self.color}, size={self.size})"


class ParticleTypeFactory:
    """Factory for particle types."""
    
    def __init__(self) -> None:
        """Initialize factory."""
        self._types: Dict[str, ParticleType] = {}
    
    def get_type(self, name: str, color: str, size: float) -> ParticleType:
        """
        Get particle type from pool or create new one.
        
        Args:
            name: Particle name
            color: Particle color
            size: Particle size
            
        Returns:
            Particle type (shared)
        """
        key = f"{name}_{color}_{size}"
        
        if key not in self._types:
            self._types[key] = ParticleType(name, color, size)
            print(f"Creating new particle type: {key}")
        else:
            print(f"Reusing existing particle type: {key}")
        
        return self._types[key]
    
    def get_type_count(self) -> int:
        """Get number of unique types."""
        return len(self._types)


class Particle:
    """Particle with extrinsic state (position, velocity)."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 particle_type: ParticleType) -> None:
        """
        Initialize particle.
        
        Args:
            x: X position
            y: Y position
            vx: X velocity
            vy: Y velocity
            particle_type: Shared particle type
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.particle_type = particle_type
    
    def update(self) -> None:
        """Update particle position."""
        self.x += self.vx
        self.y += self.vy
    
    def display(self) -> str:
        """Display particle."""
        return f"Particle at ({self.x:.1f}, {self.y:.1f}): {self.particle_type}"


class ParticleSystem:
    """Particle system for effects."""
    
    def __init__(self) -> None:
        """Initialize particle system."""
        self._particles: List[Particle] = []
        self._type_factory = ParticleTypeFactory()
    
    def emit_particle(self, x: float, y: float, vx: float, vy: float,
                     name: str, color: str, size: float) -> None:
        """
        Emit a particle.
        
        Args:
            x: X position
            y: Y position
            vx: X velocity
            vy: Y velocity
            name: Particle name
            color: Particle color
            size: Particle size
        """
        particle_type = self._type_factory.get_type(name, color, size)
        particle = Particle(x, y, vx, vy, particle_type)
        self._particles.append(particle)
    
    def update(self) -> None:
        """Update all particles."""
        for particle in self._particles:
            particle.update()
    
    def display(self) -> None:
        """Display all particles."""
        for particle in self._particles:
            print(particle.display())
    
    def get_particle_count(self) -> int:
        """Get total particle count."""
        return len(self._particles)
    
    def get_unique_type_count(self) -> int:
        """Get number of unique types."""
        return self._type_factory.get_type_count()


def main() -> None:
    """Demonstrate flyweight pattern."""
    
    print("=== Forest with Shared Trees ===")
    
    forest = Forest()
    
    # Plant many trees with few unique types
    forest.plant_tree(10, 10, TreeType.OAK, "green", "rough")
    forest.plant_tree(20, 20, TreeType.OAK, "green", "rough")
    forest.plant_tree(30, 30, TreeType.OAK, "green", "rough")
    forest.plant_tree(40, 40, TreeType.PINE, "dark green", "smooth")
    forest.plant_tree(50, 50, TreeType.PINE, "dark green", "smooth")
    forest.plant_tree(60, 60, TreeType.MAPLE, "orange", "medium")
    forest.plant_tree(70, 70, TreeType.OAK, "green", "rough")  # Reuse
    
    print(f"\nTotal trees: {forest.get_tree_count()}")
    print(f"Unique tree types: {forest.get_unique_tree_count()}")
    print("\nForest display:")
    forest.display()
    
    print("\n=== Document with Shared Styles ===")
    
    document = Document()
    
    # Add characters with shared styles
    text = "Hello World!"
    for char in text:
        if char.isupper():
            document.add_character(char, "Arial", 16, "black")
        elif char.islower():
            document.add_character(char, "Arial", 12, "black")
        else:
            document.add_character(char, "Arial", 12, "red")
    
    print(f"\nTotal characters: {document.get_character_count()}")
    print(f"Unique styles: {document.get_unique_style_count()}")
    print("\nDocument display:")
    document.display()
    
    print("\n=== Particle System ===")
    
    particle_system = ParticleSystem()
    
    # Emit many particles with few unique types
    for i in range(5):
        particle_system.emit_particle(
            x=i * 10, y=i * 10,
            vx=1.0, vy=0.5,
            name="spark", color="yellow", size=2.0
        )
    
    for i in range(3):
        particle_system.emit_particle(
            x=i * 15, y=i * 15,
            vx=0.5, vy=1.0,
            name="smoke", color="gray", size=3.0
        )
    
    particle_system.emit_particle(
        x=50, y=50,
        vx=1.0, vy=0.5,
        name="spark", color="yellow", size=2.0  # Reuse
    )
    
    print(f"\nTotal particles: {particle_system.get_particle_count()}")
    print(f"Unique types: {particle_system.get_unique_type_count()}")
    print("\nParticle system display:")
    particle_system.display()
    
    print("\n=== Flyweight Benefits ===")
    print("1. Reduces memory usage by sharing common objects")
    print("2. Separates intrinsic (shared) from extrinsic (unique) state")
    print("3. Enables large numbers of similar objects efficiently")
    print("4. Centralizes shared state management")


if __name__ == "__main__":
    main()
