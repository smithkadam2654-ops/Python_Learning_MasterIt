"""
Advanced Python - Lesson 17: Command & State Behavioral Patterns
=================================================================
Behavioral design patterns deal with algorithms and the
assignment of responsibilities between objects.

Patterns Covered:
- Command Pattern: encapsulate requests as objects
- State Pattern: allow object to change behavior with state
- Chain of Responsibility: pass requests along a chain
- Iterator Pattern: custom iteration protocols
- Memento Pattern: save and restore object state
- Visitor Pattern: add operations without modifying classes
"""

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
import copy


# ============================================================
# 1. COMMAND PATTERN
# ============================================================
class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


class TextEditor:
    """Receiver: the object that commands operate on."""
    
    def __init__(self):
        self.content: str = ""
        self.cursor: int = 0

    def insert(self, text: str, position: int | None = None):
        pos = position if position is not None else self.cursor
        self.content = self.content[:pos] + text + self.content[pos:]
        self.cursor = pos + len(text)

    def delete(self, count: int, position: int | None = None):
        pos = position if position is not None else self.cursor
        deleted = self.content[pos:pos + count]
        self.content = self.content[:pos] + self.content[pos + count:]
        self.cursor = pos
        return deleted

    def get_content(self) -> str:
        return self.content

    def __repr__(self):
        marker = "|"
        text = self.content[:self.cursor] + marker + self.content[self.cursor:]
        return f"Editor('{text}')"


class InsertCommand(Command):
    """Command to insert text."""
    
    def __init__(self, editor: TextEditor, text: str, position: int | None = None):
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self):
        self.editor.insert(self.text, self.position)

    def undo(self):
        pos = self.position if self.position is not None else (self.editor.cursor - len(self.text))
        self.editor.delete(len(self.text), pos)

    @property
    def description(self) -> str:
        return f"Insert '{self.text}'"


class DeleteCommand(Command):
    """Command to delete text."""
    
    def __init__(self, editor: TextEditor, count: int, position: int | None = None):
        self.editor = editor
        self.count = count
        self.position = position
        self.deleted_text: str = ""

    def execute(self):
        self.deleted_text = self.editor.delete(self.count, self.position)

    def undo(self):
        pos = self.position if self.position is not None else self.editor.cursor
        self.editor.insert(self.deleted_text, pos)

    @property
    def description(self) -> str:
        return f"Delete {self.count} chars"


class CommandHistory:
    """Invoker: manages command execution and undo history."""
    
    def __init__(self):
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # New action invalidates redo
        print(f"  Executed: {command.description}")

    def undo(self):
        if not self._history:
            print("  Nothing to undo")
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        print(f"  Undone: {command.description}")

    def redo(self):
        if not self._redo_stack:
            print("  Nothing to redo")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        print(f"  Redone: {command.description}")

    @property
    def history_size(self) -> int:
        return len(self._history)


def demonstrate_command():
    """Command pattern encapsulates operations as objects."""
    editor = TextEditor()
    history = CommandHistory()
    
    print("Building text with commands:")
    history.execute(InsertCommand(editor, "Hello, World!"))
    print(f"  {editor}")
    
    history.execute(InsertCommand(editor, " Beautiful", 6))
    print(f"  {editor}")
    
    history.execute(DeleteCommand(editor, 1))  # Delete '!'
    print(f"  {editor}")
    
    history.execute(InsertCommand(editor, "!!!"))
    print(f"  {editor}")
    
    print(f"\nUndoing operations:")
    history.undo()  # Undo '!!!'
    print(f"  {editor}")
    history.undo()  # Undo delete
    print(f"  {editor}")
    history.undo()  # Undo 'Beautiful'
    print(f"  {editor}")
    
    print(f"\nRedoing:")
    history.redo()
    print(f"  {editor}")
    
    print(f"\nHistory size: {history.history_size}")


# ============================================================
# 2. STATE PATTERN
# ============================================================
class State(ABC):
    """Abstract state interface."""
    
    @abstractmethod
    def play(self, player: "MediaPlayer") -> str:
        pass

    @abstractmethod
    def pause(self, player: "MediaPlayer") -> str:
        pass

    @abstractmethod
    def stop(self, player: "MediaPlayer") -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class PlayingState(State):
    def play(self, player: "MediaPlayer") -> str:
        return f"Already playing '{player.current_track}'"

    def pause(self, player: "MediaPlayer") -> str:
        player.state = PausedState()
        return f"Paused '{player.current_track}'"

    def stop(self, player: "MediaPlayer") -> str:
        player.state = StoppedState()
        player.current_track = None
        return "Stopped"

    def name(self) -> str:
        return "Playing"


class PausedState(State):
    def play(self, player: "MediaPlayer") -> str:
        player.state = PlayingState()
        return f"Resumed '{player.current_track}'"

    def pause(self, player: "MediaPlayer") -> str:
        return "Already paused"

    def stop(self, player: "MediaPlayer") -> str:
        player.state = StoppedState()
        player.current_track = None
        return "Stopped"

    def name(self) -> str:
        return "Paused"


class StoppedState(State):
    def play(self, player: "MediaPlayer") -> str:
        if player.playlist:
            player.current_track = player.playlist.pop(0)
            player.state = PlayingState()
            return f"Playing '{player.current_track}'"
        return "Playlist is empty"

    def pause(self, player: "MediaPlayer") -> str:
        return "Cannot pause — nothing is playing"

    def stop(self, player: "MediaPlayer") -> str:
        return "Already stopped"

    def name(self) -> str:
        return "Stopped"


class MediaPlayer:
    """Context: behavior changes based on internal state."""
    
    def __init__(self, playlist: list[str] | None = None):
        self.playlist = list(playlist or [])
        self.current_track: str | None = None
        self.state: State = StoppedState()

    def play(self) -> str:
        return self.state.play(self)

    def pause(self) -> str:
        return self.state.pause(self)

    def stop(self) -> str:
        return self.state.stop(self)

    def status(self) -> str:
        track = self.current_track or "None"
        return f"[{self.state.name()}] Track: {track} | Queue: {len(self.playlist)}"


def demonstrate_state():
    """State pattern changes behavior based on internal state."""
    player = MediaPlayer(["Song A", "Song B", "Song C"])
    
    actions = [
        ("play", player.play),
        ("pause", player.pause),
        ("play", player.play),
        ("play", player.play),  # Already playing
        ("stop", player.stop),
        ("play", player.play),
        ("play", player.play),
        ("stop", player.stop),
        ("pause", player.pause),  # Can't pause when stopped
    ]
    
    for action_name, action_func in actions:
        result = action_func()
        print(f"  {action_name:6} -> {result}")
        print(f"         Status: {player.status()}")


# ============================================================
# 3. CHAIN OF RESPONSIBILITY
# ============================================================
class Handler(ABC):
    """Abstract handler in the chain."""
    
    def __init__(self):
        self._next: Handler | None = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler  # Allow chaining

    @abstractmethod
    def handle(self, request: dict) -> str | None:
        pass

    def pass_to_next(self, request: dict) -> str | None:
        if self._next:
            return self._next.handle(request)
        return f"No handler could process: {request}"


class AuthHandler(Handler):
    """First handler: check authentication."""
    
    def handle(self, request: dict) -> str | None:
        if not request.get("token"):
            return "401 Unauthorized: Missing token"
        if request["token"] == "invalid":
            return "401 Unauthorized: Invalid token"
        print("  [Auth] Token verified ✓")
        return self.pass_to_next(request)


class RateLimitHandler(Handler):
    """Second handler: check rate limits."""
    
    def __init__(self, max_requests: int = 100):
        super().__init__()
        self.request_count = 0
        self.max_requests = max_requests

    def handle(self, request: dict) -> str | None:
        self.request_count += 1
        if self.request_count > self.max_requests:
            return "429 Too Many Requests"
        print(f"  [RateLimit] Request #{self.request_count}/{self.max_requests} ✓")
        return self.pass_to_next(request)


class ValidationHandler(Handler):
    """Third handler: validate request data."""
    
    def handle(self, request: dict) -> str | None:
        if not request.get("data"):
            return "400 Bad Request: Missing data"
        if not isinstance(request["data"], dict):
            return "400 Bad Request: Data must be a dict"
        print("  [Validation] Data valid ✓")
        return self.pass_to_next(request)


class BusinessHandler(Handler):
    """Final handler: process the business logic."""
    
    def handle(self, request: dict) -> str | None:
        data = request["data"]
        return f"200 OK: Processed {data}"


def demonstrate_chain():
    """Chain of Responsibility passes requests through handlers."""
    
    # Build the chain
    auth = AuthHandler()
    rate_limit = RateLimitHandler(max_requests=5)
    validation = ValidationHandler()
    business = BusinessHandler()
    
    auth.set_next(rate_limit).set_next(validation).set_next(business)
    
    # Test requests
    requests = [
        {"token": "abc123", "data": {"action": "create_user", "name": "Alice"}},
        {"token": None, "data": {"action": "test"}},
        {"token": "abc123", "data": None},
        {"token": "invalid", "data": {"action": "test"}},
        {"token": "abc123", "data": {"action": "update", "id": 42}},
    ]
    
    for req in requests:
        print(f"\n  Request: {req}")
        result = auth.handle(req)
        print(f"  Result:  {result}")


# ============================================================
# 4. MEMENTO PATTERN (Save/Restore State)
# ============================================================
class Memento:
    """Stores a snapshot of an object's state."""
    
    def __init__(self, state: dict, timestamp: datetime, label: str = ""):
        self._state = state
        self.timestamp = timestamp
        self.label = label

    def get_state(self) -> dict:
        return self._state

    def __repr__(self):
        return f"Memento('{self.label}', {self.timestamp:%H:%M:%S})"


class GameCharacter:
    """Originator: creates and restores mementos."""
    
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.mana = 50
        self.level = 1
        self.position = (0, 0)
        self.inventory: list[str] = []

    def save(self, label: str = "") -> Memento:
        """Create a memento (snapshot) of current state."""
        state = {
            "health": self.health,
            "mana": self.mana,
            "level": self.level,
            "position": self.position,
            "inventory": list(self.inventory),  # Deep copy
        }
        return Memento(state, datetime.now(), label)

    def restore(self, memento: Memento):
        """Restore state from a memento."""
        state = memento.get_state()
        self.health = state["health"]
        self.mana = state["mana"]
        self.level = state["level"]
        self.position = state["position"]
        self.inventory = list(state["inventory"])
        print(f"  Restored to: {memento}")

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def heal(self, amount: int):
        self.health = min(100, self.health + amount)

    def add_item(self, item: str):
        self.inventory.append(item)

    def __repr__(self):
        return (
            f"{self.name} [HP:{self.health} MP:{self.mana} "
            f"Lv:{self.level} Items:{self.inventory}]"
        )


class SaveManager:
    """Caretaker: manages mementos without inspecting them."""
    
    def __init__(self):
        self._saves: list[Memento] = []

    def save(self, character: GameCharacter, label: str):
        memento = character.save(label)
        self._saves.append(memento)
        print(f"  Saved: {memento}")

    def undo(self, character: GameCharacter):
        if not self._saves:
            print("  No saves to restore")
            return
        memento = self._saves.pop()
        character.restore(memento)

    def list_saves(self) -> list[Memento]:
        return list(self._saves)


def demonstrate_memento():
    """Memento pattern saves and restores object state."""
    
    hero = GameCharacter("Hero")
    saves = SaveManager()
    
    print("Game progression:")
    saves.save(hero, "Start")
    print(f"  {hero}")
    
    hero.add_item("Sword")
    hero.level = 2
    hero.take_damage(20)
    saves.save(hero, "After first battle")
    print(f"  {hero}")
    
    hero.add_item("Shield")
    hero.add_item("Potion")
    hero.take_damage(50)
    hero.mana = 10
    saves.save(hero, "Before boss")
    print(f"  {hero}")
    
    # Boss fight goes badly
    hero.take_damage(100)
    print(f"  {hero} — DEAD!")
    
    # Restore last save
    print("\nLoading last save...")
    saves.undo(hero)
    print(f"  {hero}")
    
    # Go back further
    print("\nLoading earlier save...")
    saves.undo(hero)
    print(f"  {hero}")


# ============================================================
# 5. VISITOR PATTERN
# ============================================================
class Visitor(ABC):
    """Abstract visitor."""
    
    @abstractmethod
    def visit_circle(self, circle: "VisitorCircle") -> Any:
        pass

    @abstractmethod
    def visit_rectangle(self, rect: "VisitorRectangle") -> Any:
        pass

    @abstractmethod
    def visit_triangle(self, tri: "VisitorTriangle") -> Any:
        pass


class Acceptable(ABC):
    """Interface for objects that accept visitors."""
    
    @abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        pass


class VisitorCircle(Acceptable):
    def __init__(self, radius: float):
        self.radius = radius

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_circle(self)


class VisitorRectangle(Acceptable):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_rectangle(self)


class VisitorTriangle(Acceptable):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_triangle(self)


class AreaCalculator(Visitor):
    """Visitor that calculates areas."""
    def visit_circle(self, circle: VisitorCircle) -> float:
        import math
        return math.pi * circle.radius ** 2

    def visit_rectangle(self, rect: VisitorRectangle) -> float:
        return rect.width * rect.height

    def visit_triangle(self, tri: VisitorTriangle) -> float:
        return 0.5 * tri.base * tri.height


class JsonExporter(Visitor):
    """Visitor that exports shapes to JSON."""
    def visit_circle(self, circle: VisitorCircle) -> dict:
        return {"type": "circle", "radius": circle.radius}

    def visit_rectangle(self, rect: VisitorRectangle) -> dict:
        return {"type": "rectangle", "width": rect.width, "height": rect.height}

    def visit_triangle(self, tri: VisitorTriangle) -> dict:
        return {"type": "triangle", "base": tri.base, "height": tri.height}


class PerimeterCalculator(Visitor):
    """Visitor that calculates perimeters."""
    def visit_circle(self, circle: VisitorCircle) -> float:
        import math
        return 2 * math.pi * circle.radius

    def visit_rectangle(self, rect: VisitorRectangle) -> float:
        return 2 * (rect.width + rect.height)

    def visit_triangle(self, tri: VisitorTriangle) -> float:
        import math
        a = tri.base
        b = math.sqrt((tri.base/2)**2 + tri.height**2)
        return a + 2 * b  # Isosceles triangle


def demonstrate_visitor():
    """Visitor adds operations without modifying shape classes."""
    import json
    
    shapes: list[Acceptable] = [
        VisitorCircle(5),
        VisitorRectangle(4, 6),
        VisitorTriangle(8, 3),
    ]
    
    # Calculate areas
    area_calc = AreaCalculator()
    print("Areas:")
    for shape in shapes:
        area = shape.accept(area_calc)
        print(f"  {type(shape).__name__}: {area:.2f}")
    
    # Calculate perimeters
    peri_calc = PerimeterCalculator()
    print("\nPerimeters:")
    for shape in shapes:
        peri = shape.accept(peri_calc)
        print(f"  {type(shape).__name__}: {peri:.2f}")
    
    # Export to JSON
    exporter = JsonExporter()
    print("\nJSON export:")
    for shape in shapes:
        data = shape.accept(exporter)
        print(f"  {json.dumps(data)}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Command Pattern (Text Editor)")
    demonstrate_command()

    separator("2. State Pattern (Media Player)")
    demonstrate_state()

    separator("3. Chain of Responsibility")
    demonstrate_chain()

    separator("4. Memento Pattern (Game Save/Load)")
    demonstrate_memento()

    separator("5. Visitor Pattern")
    demonstrate_visitor()


if __name__ == "__main__":
    main()
