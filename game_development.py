"""
Game Development Module

This module provides comprehensive game development utilities including:
- Game loop implementation
- Sprite and texture management
- Collision detection
- Input handling
- Game state management
- Pathfinding algorithms
- AI behavior trees
- Particle systems
- Game physics basics
- Level/scene management

All functions include comprehensive docstrings and type hints.
"""

import math
import random
import time
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from collections import deque


class GameState(Enum):
    """Game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"


class CollisionType(Enum):
    """Collision detection types."""
    AABB = "aabb"  # Axis-Aligned Bounding Box
    CIRCLE = "circle"
    PIXEL = "pixel"
    TILE = "tile"


@dataclass
class Vector2:
    """2D vector for game mathematics."""
    x: float
    y: float
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        """Add two vectors."""
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        """Subtract two vectors."""
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2':
        """Multiply vector by scalar."""
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        """Divide vector by scalar."""
        return Vector2(self.x / scalar, self.y / scalar)
    
    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2':
        """Normalize vector to unit length."""
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)
    
    def distance_to(self, other: 'Vector2') -> float:
        """Calculate distance to another vector."""
        return (self - other).magnitude()
    
    def dot(self, other: 'Vector2') -> float:
        """Calculate dot product."""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Vector2') -> float:
        """Calculate 2D cross product (returns scalar)."""
        return self.x * other.y - self.y * other.x


@dataclass
class Rect:
    """Rectangle for collision detection."""
    x: float
    y: float
    width: float
    height: float
    
    @property
    def left(self) -> float:
        """Get left edge."""
        return self.x
    
    @property
    def right(self) -> float:
        """Get right edge."""
        return self.x + self.width
    
    @property
    def top(self) -> float:
        """Get top edge."""
        return self.y
    
    @property
    def bottom(self) float:
        """Get bottom edge."""
        return self.y + self.height
    
    @property
    def center(self) -> Vector2:
        """Get center point."""
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)
    
    def intersects(self, other: 'Rect') -> bool:
        """Check if rectangle intersects with another."""
        return (self.left < other.right and self.right > other.left and
                self.top < other.bottom and self.bottom > other.top)
    
    def contains(self, point: Vector2) -> bool:
        """Check if rectangle contains a point."""
        return (self.left <= point.x <= self.right and
                self.top <= point.y <= self.bottom)


@dataclass
class Circle:
    """Circle for collision detection."""
    x: float
    y: float
    radius: float
    
    @property
    def center(self) -> Vector2:
        """Get center point."""
        return Vector2(self.x, self.y)
    
    def intersects(self, other: 'Circle') -> bool:
        """Check if circle intersects with another circle."""
        distance = self.center.distance_to(other.center)
        return distance < (self.radius + other.radius)
    
    def contains(self, point: Vector2) -> bool:
        """Check if circle contains a point."""
        return self.center.distance_to(point) <= self.radius


class InputHandler:
    """Input handling for games."""
    
    def __init__(self):
        """Initialize input handler."""
        self.keys_down: set = set()
        self.keys_pressed: set = set()
        self.keys_released: set = set()
        self.mouse_position: Vector2 = Vector2(0, 0)
        self.mouse_buttons: Dict[int, bool] = {}
        self.mouse_wheel: int = 0
    
    def key_down(self, key: str) -> None:
        """Handle key down event."""
        self.keys_down.add(key)
        self.keys_pressed.add(key)
    
    def key_up(self, key: str) -> None:
        """Handle key up event."""
        if key in self.keys_down:
            self.keys_down.remove(key)
        self.keys_released.add(key)
    
    def is_key_down(self, key: str) -> bool:
        """Check if key is currently down."""
        return key in self.keys_down
    
    def is_key_pressed(self, key: str) -> bool:
        """Check if key was pressed this frame."""
        return key in self.keys_pressed
    
    def is_key_released(self, key: str) -> bool:
        """Check if key was released this frame."""
        return key in self.keys_released
    
    def clear_frame(self) -> None:
        """Clear frame-specific input states."""
        self.keys_pressed.clear()
        self.keys_released.clear()
    
    def set_mouse_position(self, x: float, y: float) -> None:
        """Set mouse position."""
        self.mouse_position = Vector2(x, y)
    
    def get_mouse_position(self) -> Vector2:
        """Get current mouse position."""
        return self.mouse_position
    
    def mouse_button_down(self, button: int) -> None:
        """Handle mouse button down event."""
        self.mouse_buttons[button] = True
    
    def mouse_button_up(self, button: int) -> None:
        """Handle mouse button up event."""
        self.mouse_buttons[button] = False
    
    def is_mouse_button_down(self, button: int) -> bool:
        """Check if mouse button is down."""
        return self.mouse_buttons.get(button, False)
    
    def set_mouse_wheel(self, delta: int) -> None:
        """Handle mouse wheel event."""
        self.mouse_wheel = delta


class CollisionDetector:
    """Collision detection utilities."""
    
    @staticmethod
    def check_aabb_collision(rect1: Rect, rect2: Rect) -> bool:
        """Check AABB (Axis-Aligned Bounding Box) collision."""
        return rect1.intersects(rect2)
    
    @staticmethod
    def check_circle_collision(circle1: Circle, circle2: Circle) -> bool:
        """Check circle-circle collision."""
        return circle1.intersects(circle2)
    
    @staticmethod
    def check_circle_rect_collision(circle: Circle, rect: Rect) -> bool:
        """Check circle-rectangle collision."""
        # Find closest point on rectangle to circle center
        closest_x = max(rect.left, min(circle.x, rect.right))
        closest_y = max(rect.top, min(circle.y, rect.bottom))
        
        closest_point = Vector2(closest_x, closest_y)
        distance = circle.center.distance_to(closest_point)
        
        return distance <= circle.radius
    
    @staticmethod
    def check_point_in_rect(point: Vector2, rect: Rect) -> bool:
        """Check if point is inside rectangle."""
        return rect.contains(point)
    
    @staticmethod
    def check_point_in_circle(point: Vector2, circle: Circle) -> bool:
        """Check if point is inside circle."""
        return circle.contains(point)
    
    @staticmethod
    def resolve_aabb_collision(rect1: Rect, rect2: Rect) -> Vector2:
        """Resolve AABB collision by pushing objects apart."""
        overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
        overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, top)
        
        if overlap_x < overlap_y:
            # Push horizontally
            if rect1.center.x < rect2.center.x:
                return Vector2(-overlap_x, 0)
            else:
                return Vector2(overlap_x, 0)
        else:
            # Push vertically
            if rect1.center.y < rect2.center.y:
                return Vector2(0, -overlap_y)
            else:
                return Vector2(0, overlap_y)
    
    @staticmethod
    def resolve_circle_collision(circle1: Circle, circle2: Circle) -> Vector2:
        """Resolve circle collision by pushing apart."""
        direction = (circle2.center - circle1.center).normalize()
        overlap = (circle1.radius + circle2.radius) - circle1.center.distance_to(circle2.center)
        
        return direction * overlap


class Pathfinding:
    """Pathfinding algorithms for games."""
    
    @staticmethod
    def find_path_a_star(start: Tuple[int, int], 
                         goal: Tuple[int, int],
                         grid: List[List[int]],
                         blocked_values: List[int] = None) -> List[Tuple[int, int]]:
        """A* pathfinding algorithm."""
        if blocked_values is None:
            blocked_values = [1]  # Default blocked value
        
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            return []
        
        if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
            return []
        
        if grid[start[0]][start[1]] in blocked_values or grid[goal[0]][goal[1]] in blocked_values:
            return []
        
        # Priority queue: (f, g, path)
        open_set = [(0, 0, [start])]
        closed_set = set()
        came_from = {}
        
        g_score = {start: 0}
        f_score = {start: Pathfinding._heuristic(start, goal)}
        
        while open_set:
            current = min(open_set, key=lambda x: x[2])
            open_set.remove(current)
            closed_set.add(current[2])
            
            if current[2] == goal:
                path = []
                while current[2] in came_from:
                    path.append(current[2])
                    current = came_from[current[2]]
                path.reverse()
                return path
            
            # Get neighbors
            neighbors = Pathfinding._get_neighbors(current[2], grid, blocked_values, rows, cols)
            
            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue
                
                tentative_g = g_score[current[2]] + 1
                tentative_f = tentative_g + Pathfinding._heuristic(neighbor, goal)
                
                if neighbor not in g_score or tentative_f < f_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current[2]
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_f
                    open_set.append((tentative_f, tentative_g, neighbor))
        
        return []
    
    @staticmethod
    def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Heuristic function for A* (Manhattan distance)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    @staticmethod
    def _get_neighbors(pos: Tuple[int, int], grid: List[List[int]],
                    blocked_values: List[int], rows: int, cols: int) -> List[Tuple[int, int]]:
        """Get valid neighboring positions."""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            
            if 0 <= new_x < rows and 0 <= new_y < cols:
                if grid[new_x][new_y] not in blocked_values:
                    neighbors.append((new_x, new_y))
        
        return neighbors
    
    @staticmethod
    def find_path_bfs(start: Tuple[int, int],
                       goal: Tuple[int, int],
                       grid: List[List[int]],
                       blocked_values: List[int] = None) -> List[Tuple[int, int]]:
        """BFS pathfinding algorithm (shortest path)."""
        if blocked_values is None:
            blocked_values = [1]
        
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            return []
        
        if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
            return []
        
        if grid[start[0]][start[1]] in blocked_values or grid[goal[0]][goal[1]] in blocked_values:
            return []
        
        queue = deque([start])
        visited = {start}
        came_from = {}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for neighbor in Pathfinding._get_neighbors(current, grid, blocked_values, rows, cols):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return []


class ParticleSystem:
    """Particle system for visual effects."""
    
    def __init__(self, max_particles: int = 100):
        """Initialize particle system."""
        self.max_particles = max_particles
        self.particles: List[Dict[str, Any]] = []
        self.emitters: List[Dict[str, Any]] = []
    
    def add_emitter(self, position: Vector2, 
                   emission_rate: float = 1.0,
                   particle_life: float = 5.0,
                   spread: float = 1.0) -> None:
        """Add a particle emitter."""
        self.emitters.append({
            "position": position,
            "emission_rate": emission_rate,
            "particle_life": particle_life,
            "spread": spread
        })
    
    def emit(self, delta_time: float) -> None:
        """Emit particles from all emitters."""
        for emitter in self.emitters:
            num_to_emit = int(emitter["emission_rate"] * delta_time)
            
            for _ in range(num_to_emit):
                if len(self.particles) < self.max_particles:
                    # Random velocity based on spread
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(0.5, 2.0)
                    velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
                    
                    self.particles.append({
                        "position": Vector2(emitter["position"].x, emitter["position"].y),
                        "velocity": velocity,
                        "life": emitter["particle_life"],
                        "max_life": emitter["particle_life"],
                        "color": (random.random(), random.random(), random.random()),
                        "size": random.uniform(2.0, 5.0)
                    })
    
    def update(self, delta_time: float) -> None:
        """Update all particles."""
        alive_particles = []
        
        for particle in self.particles:
            # Update position
            particle["position"] = particle["position"] + particle["velocity"] * delta_time
            
            # Update life
            particle["life"] -= delta_time
            
            # Apply gravity
            particle["velocity"] = particle["velocity"] + Vector2(0, 9.8) * delta_time
            
            # Apply friction
            particle["velocity"] = particle["velocity"] * 0.99
            
            # Shrink over time
            particle["size"] *= 0.98
            
            if particle["life"] > 0 and particle["size"] > 0.1:
                alive_particles.append(particle)
        
        self.particles = alive_particles
    
    def get_particles(self) -> List[Dict[str, Any]]:
        """Get all current particles."""
        return self.particles
    
    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()


class BehaviorTree:
    """Behavior tree for AI decision making."""
    
    def __init__(self):
        """Initialize behavior tree."""
        self.root: Optional['Node'] = None
    
    def create_node(self, name: str, condition: Callable = None,
                    action: Callable = None) -> 'Node':
        """Create a behavior tree node."""
        node = BehaviorTree.Node(name, condition, action)
        return node
    
    def set_root(self, node: 'Node') -> None:
        """Set the root node of the behavior tree."""
        self.root = node
    
    def execute(self, context: Dict[str, Any]) -> str:
        """Execute behavior tree and return result."""
        if not self.root:
            return "no_root"
        
        return self.root.execute(context)
    
    class Node:
        """Behavior tree node."""
        
        def __init__(self, name: str, condition: Callable = None,
                     action: Callable = None):
            """Initialize node."""
            self.name = name
            self.condition = condition
            self.action = action
            self.children: List['BehaviorTree.Node'] = []
        
        def add_child(self, child: 'Node') -> None:
            """Add child node."""
            self.children.append(child)
        
        def execute(self, context: Dict[str, Any]) -> str:
            """Execute node and children."""
            # Check condition if exists
            if self.condition and not self.condition(context):
                return f"{self.name}_failed"
            
            # Execute action if exists
            if self.action:
                self.action(context)
                return f"{self.name}_success"
            
            # Execute children
            for child in self.state:
                result = child.execute(context)
                if result.endswith("_success"):
                    return f"{self.name}_success"
            
            return f"{self.name}_failed"


class GameLoop:
    """Game loop implementation."""
    
    def __init__(self, target_fps: int = 60):
        """Initialize game loop."""
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.running = False
        self.current_time = 0.0
        self.accumulator = 0.0
        self.update_functions: List[Callable] = []
        self.render_functions: List[Callable] = []
    
    def add_update(self, update_func: Callable) -> None:
        """Add update function."""
        self.update_functions.append(update_func)
    
    def add_render(self, render_func: Callable) -> None:
        """Add render function."""
        self.render_functions.append(render_func)
    
    def start(self) -> None:
        """Start the game loop."""
        self.running = True
        self.current_time = time.time()
        self.accumulator = 0.0
        
        while self.running:
            new_time = time.time()
            frame_time = new_time - self.current_time
            self.current_time = new_time
            self.accumulator += frame_time
            
            # Process multiple frames if needed
            while self.accumulator >= self.frame_time:
                self.accumulator -= self.frame_time
                
                # Update
                for update_func in self.update_functions:
                    update_func(self.frame_time)
                
                # Render
                for render_func in self.render_functions:
                    render_func()
    
    def stop(self) -> None:
        """Stop the game loop."""
        self.running = False


class GamePhysics:
    """Simple physics simulation for games."""
    
    @staticmethod
    def apply_gravity(entity: Dict[str, Any], delta_time: float,
                       gravity: float = 9.8) -> None:
        """Apply gravity to entity."""
        entity["velocity_y"] += gravity * delta_time
        entity["y"] += entity["velocity_y"] * delta_time
    
    @staticmethod
 def apply_friction(entity: Dict[str, Any], delta_time: float,
                       friction: float = 0.98) -> None:
        """Apply friction to entity velocity."""
        entity["velocity_x"] *= friction
        entity["velocity_y"] *= friction
    
    @staticmethod
    def check_ground_collision(entity: Dict[str, Any], ground_y: float) -> bool:
        """Check if entity is on the ground."""
        return entity["y"] >= ground_y - entity["height"]
    
    @staticmethod
    def resolve_ground_collision(entity: Dict[str, Any], ground_y: float) -> None:
        """Resolve ground collision."""
        entity["y"] = ground_y - entity["height"]
        entity["velocity_y"] = 0
        entity["on_ground"] = True


class LevelManager:
    """Level and scene management."""
    
    def __init__(self):
        """Initialize level manager."""
        self.current_level: Optional[str] = None
        self.levels: Dict[str, Dict] = {}
    
    def create_level(self, level_id: str, level_data: Dict) -> None:
        """Create a new level."""
        self.levels[level_id] = level_data
    
    def load_level(self, level_id: str) -> bool:
        """Load a level."""
        if level_id in self.levels:
            self.current_level = level_id
            return True
        return False
    
    def get_current_level(self) -> Optional[Dict]:
        """Get current level data."""
        if self.current_level:
            return self.levels.get(self.current_level)
        return None
    
    def get_level_list(self) -> List[str]:
        """Get list of available levels."""
        return list(self.levels.keys())


class Sprite:
    """Sprite management for 2D games."""
    
    def __init__(self, image_path: str, position: Vector2,
                 scale: float = 1.0, rotation: float = 0.0):
        """Initialize sprite."""
        self.image_path = image_path
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.visible = True
        self.loaded = False
        self.texture: Any = None
    
    def load(self) -> bool:
        """Load sprite image (simplified)."""
        # In real implementation, this would load using pygame or similar
        self.loaded = True
        return True
    
    def draw(self, position: Vector2 = None) -> None:
        """Draw sprite at position."""
        if position:
            self.position = position
        
        # In real implementation, this would render the texture
        pass
    
    def set_position(self, position: Vector2) -> None:
        """Set sprite position."""
        self.position = position
    
    def get_position(self) -> Vector2:
        """Get sprite position."""
        return self.position
    
    def set_scale(self, scale: float) -> None:
        """Set sprite scale."""
        self.scale = scale
    
    def set_rotation(self, rotation: float) -> None:
        """Set sprite rotation."""
        self.rotation = rotation
    
    def show(self) -> None:
        """Show sprite."""
        self.visible = True
    
    def hide(self) -> None:
        """Hide sprite."""
        self.visible = False


class DataManager:
    """Game data management."""
    
    def __init__(self):
        """Initialize data manager."""
        self.game_data: Dict[str, Any] = {}
        self.player_data: Dict[str, Any] = {}
        self.level_data: Dict[str, Any] = {}
    
    def save_game(self, save_file: str) -> bool:
        """Save game state to file."""
        try:
            import json
            save_data = {
                "game_data": self.game_data,
                "player_data": self.player_data,
                "level_data": self.level_data,
                "timestamp": time.time()
            }
            
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load_game(self, save_file: str) -> bool:
        """Load game state from file."""
        try:
            import json
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            self.game_data = save_data.get("game_data", {})
            self.player_data = save_data.get("player_data", {})
            self.level_data = save_data.get("level_data", {})
            
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False
    
    def set_value(self, key: str, value: Any) -> None:
        """Set a value in game data."""
        self.game_data[key] = value
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """Get a value from game data."""
        return self.game_data.get(key, default)


def demonstrate_game_development():
    """Demonstrate game development functionality."""
    print("=== Game Development Demonstration ===\n")
    
    # Vector Mathematics
    print("1. Vector Mathematics:")
    vec1 = Vector2(3, 4)
    vec2 = Vector2(1, 2)
    
    print(f"   Vector1: ({vec1.x}, {vec1.y})")
    print(f"   Vector2: ({vec2.x}, {vec2.y})")
    print(f"   Addition: {vec1 + vec2}")
    print(f"   Subtraction: {vec1 - vec2}")
    print(f"   Magnitude: {vec1.magnitude():.2f}")
    print(f"   Normalize: ({vec1.normalize().x:.2f}, {vec1.normalize().y:.2f})")
    print(f"   Distance: {vec1.distance_to(vec2):.2f}")
    print(f"   Dot product: {vec1.dot(vec2)}")
    
    # Collision Detection
    print("\n2. Collision Detection:")
    rect1 = Rect(0, 0, 10, 10)
    rect2 = Rect(5, 5, 10, 10)
    
    print(f"   Rect1: ({rect1.x}, {rect1.y}, {rect1.width}, {rect1.height})")
    print(f"   Rect2: ({rect2.x}, {rect2.y}, {rect2.width}, {rect2.height})")
    print(f"   AABB collision: {CollisionDetector.check_aabb_collision(rect1, rect2)}")
    
    circle1 = Circle(5, 5, 3)
    circle2 = Circle(12, 12, 4)
    
    print(f"   Circle1: center=({circle1.x}, {circle1.y}), radius={circle1.radius}")
    print(f"   Circle2: center=({circle2.x}, {circle2.y}), radius={circle2.radius}")
    print(f"   Circle collision: {CollisionDetector.check_circle_collision(circle1, circle2)}")
    
    # Input Handling
    print("\n3. Input Handling:")
    input_handler = InputHandler()
    
    input_handler.key_down("W")
    input_handler.key_down("A")
    input_handler.key_up("W")
    
    print(f"   W is down: {input_handler.is_key_down('W')}")
    print(f"   A was pressed: {input_handler.is_key_pressed('A')}")
    print(f"   W was released: {input_handler.is_key_released('W')}")
    
    input_handler.set_mouse_position(100, 200)
    print(f"   Mouse position: {input_handler.get_mouse_position()}")
    
    # Pathfinding
    print("\n4. Pathfinding:")
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    bfs_path = Pathfinding.find_path_bfs(start, goal, grid)
    astar_path = Pathfinding.find_path_a_star(start, goal, grid)
    
    print(f"   Start: {start}, Goal: {goal}")
    print(f"   BFS path: {bfs_path}")
    print(f"   A* path: {astar_path}")
    
    # Particle System
    print("\n5. Particle System:")
    particle_system = ParticleSystem(max_particles=50)
    particle_system.add_emitter(Vector2(400, 300), emission_rate=5.0)
    
    print("   Emitting particles...")
    particle_system.emit(0.1)
    print(f"   Particles: {len(particle_system.get_particles())}")
    
    particle_system.update(0.1)
    print(f"   After update: {len(particle_system.get_particles())}")
    
    # Behavior Tree
    print("\n6. Behavior Tree:")
    behavior_tree = BehaviorTree()
    
    def should_attack(context):
        return context.get("health", 100) < 50
    
    def attack_action(context):
        context["attacking"] = True
    
    def should_patrol(context):
        return context.get("distance", 10) < 5
    
    def patrol_action(context):
        context["patrolling"] = True
    
    root = behavior_tree.create_node("root")
    attack_node = behavior_tree.create_node("attack", should_attack, attack_action)
    patrol_node = behavior_tree.create_node("patrol", should_patrol, patrol_action)
    
    root.add_child(attack_node)
    root.add_child(patrol)
    behavior_tree.set_root(root)
    
    context = {"health": 30, "distance": 3}
    result = behavior_tree.execute(context)
    print(f"   AI decision: {result}")
    
    # Game Loop
    print("\n7. Game Loop:")
    game_loop = GameLoop(target_fps=60)
    
    def update_logic(delta_time):
        pass
    
    def render_logic():
        pass
    
    game_loop.add_update(update_logic)
    game_loop.add_render(render_logic)
    
    print("   Game loop configured with 60 FPS")
    print(f"   Frame time: {game_loop.frame_time:.4f}s")
    
    # Physics
    print("\n8. Game Physics:")
    entity = {
        "x": 100.0,
        "y": 200.0,
        "velocity_x": 5.0,
        "velocity_y": 0.0,
        "height": 50.0
    }
    
    print(f"   Initial position: ({entity['x']}, {entity['y']})")
    
    GamePhysics.apply_gravity(entity, 0.1)
    print(f"   After gravity: y={entity['y']:.2f}")
    
    GamePhysics.apply_friction(entity, 0.1)
    print(f"   After friction: vx={entity['velocity_x']:.2f}")
    
    is_grounded = GamePhysics.check_ground_collision(entity, 400)
    print(f"   On ground: {is_grounded}")
    
    # Sprite Management
    print("\n9. Sprite Management:")
    sprite = Sprite("player.png", Vector2(0, 0))
    print(f"   Sprite position: {sprite.get_position()}")
    
    sprite.set_position(Vector2(100, 200))
    print(f"   New position: {sprite.get_position()}")
    
    sprite.set_scale(1.5)
    print(f"   Scale: {sprite.scale}")
    
    # Data Management
    print("\n10. Data Management:")
    data_manager = DataManager()
    
    data_manager.set_value("player_name", "Hero")
    data_manager.set_value("score", 1000)
    data_manager.set_value("level", 5)
    
    print(f"   Player name: {data_manager.get_value('player_name')}")
    print(f"   Score: {data_manager.get_value('score')}")
    print(f"   Level: {data_manager.get_value('level')}")
    
    print("\n=== Demonstration Complete ===")
    print("\nGame Development Best Practices:")
    print("- Use fixed time steps for consistent physics")
    "- Implement proper collision detection and resolution")
    "- Use efficient pathfinding algorithms")
    "- Handle input consistently across different frame rates")
    "- Organize game logic into clear systems")
    "- Use object pooling for frequently created objects")
    "- Separate game logic from rendering")
    "- Test game mechanics thoroughly")
    "- Optimize for target platform performance")
    "- Implement save/load functionality")


if __name__ == "__main__":
    demonstrate_game_development()