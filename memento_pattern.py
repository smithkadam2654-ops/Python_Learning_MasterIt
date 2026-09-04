"""
Memento Pattern - Memento pattern for object state restoration.
Features: State snapshots, undo functionality, and encapsulation.
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import copy


@dataclass
class TextEditorMemento:
    """Memento for text editor state."""
    content: str
    cursor_position: int
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class TextEditor:
    """Text editor with memento support."""
    
    def __init__(self) -> None:
        """Initialize text editor."""
        self._content = ""
        self._cursor_position = 0
    
    def write(self, text: str) -> None:
        """Write text at cursor position."""
        self._content = self._content[:self._cursor_position] + text + self._content[self._cursor_position:]
        self._cursor_position += len(text)
    
    def move_cursor(self, position: int) -> None:
        """Move cursor to position."""
        self._cursor_position = max(0, min(position, len(self._content)))
    
    def delete(self, count: int = 1) -> None:
        """Delete characters at cursor."""
        end = min(self._cursor_position + count, len(self._content))
        self._content = self._content[:self._cursor_position] + self._content[end:]
    
    def get_content(self) -> str:
        """Get current content."""
        return self._content
    
    def get_cursor_position(self) -> int:
        """Get cursor position."""
        return self._cursor_position
    
    def save(self) -> TextEditorMemento:
        """Save current state to memento."""
        return TextEditorMemento(
            content=self._content,
            cursor_position=self._cursor_position
        )
    
    def restore(self, memento: TextEditorMemento) -> None:
        """Restore state from memento."""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
    
    def __str__(self) -> str:
        """String representation."""
        cursor = "^"
        content_with_cursor = self._content[:self._cursor_position] + cursor + self._content[self._cursor_position:]
        return f"Content: '{self._content}'\nCursor:  {content_with_cursor}"


class Caretaker:
    """Caretaker for managing mementos."""
    
    def __init__(self) -> None:
        """Initialize caretaker."""
        self._mementos: List[TextEditorMemento] = []
        self._current_index = -1
    
    def save(self, memento: TextEditorMemento) -> None:
        """Save memento."""
        # Remove any mementos after current index (redo history)
        self._mementos = self._mementos[:self._current_index + 1]
        self._mementos.append(memento)
        self._current_index += 1
    
    def undo(self) -> Optional[TextEditorMemento]:
        """Get previous memento."""
        if self._current_index > 0:
            self._current_index -= 1
            return self._mementos[self._current_index]
        return None
    
    def redo(self) -> Optional[TextEditorMemento]:
        """Get next memento."""
        if self._current_index < len(self._mementos) - 1:
            self._current_index += 1
            return self._mementos[self._current_index]
        return None
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._current_index < len(self._mementos) - 1
    
    def clear(self) -> None:
        """Clear all mementos."""
        self._mementos.clear()
        self._current_index = -1


@dataclass
class BankAccountMemento:
    """Memento for bank account state."""
    balance: float
    transaction_history: List[str]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BankAccount:
    """Bank account with memento support."""
    
    def __init__(self, initial_balance: float = 0.0) -> None:
        """
        Initialize bank account.
        
        Args:
            initial_balance: Initial balance
        """
        self._balance = initial_balance
        self._transaction_history: List[str] = []
    
    def deposit(self, amount: float) -> None:
        """Deposit money."""
        self._balance += amount
        self._transaction_history.append(f"Deposit: +${amount:.2f}")
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful
        """
        if amount > self._balance:
            return False
        
        self._balance -= amount
        self._transaction_history.append(f"Withdrawal: -${amount:.2f}")
        return True
    
    def get_balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    def get_transaction_history(self) -> List[str]:
        """Get transaction history."""
        return self._transaction_history.copy()
    
    def save(self) -> BankAccountMemento:
        """Save current state to memento."""
        return BankAccountMemento(
            balance=self._balance,
            transaction_history=self._transaction_history.copy()
        )
    
    def restore(self, memento: BankAccountMemento) -> None:
        """Restore state from memento."""
        self._balance = memento.balance
        self._transaction_history = memento.transaction_history.copy()
    
    def __str__(self) -> str:
        """String representation."""
        return f"Balance: ${self._balance:.2f}\nTransactions: {len(self._transaction_history)}"


class GameState:
    """Game state with memento support."""
    
    def __init__(self) -> None:
        """Initialize game state."""
        self._level = 1
        self._score = 0
        self._lives = 3
        self._inventory: List[str] = []
    
    def advance_level(self) -> None:
        """Advance to next level."""
        self._level += 1
        self._score += 100
    
    def add_score(self, points: int) -> None:
        """Add score points."""
        self._score += points
    
    def lose_life(self) -> None:
        """Lose a life."""
        self._lives -= 1
    
    def add_item(self, item: str) -> None:
        """Add item to inventory."""
        self._inventory.append(item)
    
    def get_level(self) -> int:
        """Get current level."""
        return self._level
    
    def get_score(self) -> int:
        """Get current score."""
        return self._score
    
    def get_lives(self) -> int:
        """Get remaining lives."""
        return self._lives
    
    def get_inventory(self) -> List[str]:
        """Get inventory."""
        return self._inventory.copy()
    
    def save(self) -> dict:
        """Save current state."""
        return {
            "level": self._level,
            "score": self._score,
            "lives": self._lives,
            "inventory": self._inventory.copy()
        }
    
    def restore(self, state: dict) -> None:
        """Restore state."""
        self._level = state["level"]
        self._score = state["score"]
        self._lives = state["lives"]
        self._inventory = state["inventory"].copy()
    
    def __str__(self) -> str:
        """String representation."""
        return f"Level: {self._level}, Score: {self._score}, Lives: {self._lives}, Items: {self._inventory}"


class GameSaveManager:
    """Manager for game saves."""
    
    def __init__(self, max_saves: int = 5) -> None:
        """
        Initialize save manager.
        
        Args:
            max_saves: Maximum number of saves to keep
        """
        self._saves: List[dict] = []
        self._max_saves = max_saves
    
    def save_game(self, state: GameState, slot: int = 0) -> bool:
        """
        Save game state.
        
        Args:
            state: Game state to save
            slot: Save slot number
            
        Returns:
            True if saved successfully
        """
        if slot < 0 or slot >= self._max_saves:
            return False
        
        save_data = state.save()
        save_data["timestamp"] = datetime.now().isoformat()
        
        # Ensure saves list is large enough
        while len(self._saves) <= slot:
            self._saves.append(None)
        
        self._saves[slot] = save_data
        return True
    
    def load_game(self, state: GameState, slot: int = 0) -> bool:
        """
        Load game state.
        
        Args:
            state: Game state to restore to
            slot: Save slot number
            
        Returns:
            True if loaded successfully
        """
        if slot < 0 or slot >= len(self._saves):
            return False
        
        save_data = self._saves[slot]
        if save_data is None:
            return False
        
        state.restore(save_data)
        return True
    
    def delete_save(self, slot: int) -> bool:
        """
        Delete save.
        
        Args:
            slot: Save slot number
            
        Returns:
            True if deleted successfully
        """
        if slot < 0 or slot >= len(self._saves):
            return False
        
        self._saves[slot] = None
        return True
    
    def get_save_info(self, slot: int) -> Optional[dict]:
        """
        Get save information.
        
        Args:
            slot: Save slot number
            
        Returns:
            Save information or None
        """
        if slot < 0 or slot >= len(self._saves):
            return None
        
        return self._saves[slot]


def main() -> None:
    """Demonstrate memento pattern."""
    
    print("=== Text Editor with Undo/Redo ===")
    
    editor = TextEditor()
    caretaker = Caretaker()
    
    # Initial save
    caretaker.save(editor.save())
    
    # Write some text
    editor.write("Hello")
    print(f"\nAfter writing 'Hello':\n{editor}")
    caretaker.save(editor.save())
    
    # Write more text
    editor.write(" World")
    print(f"\nAfter writing ' World':\n{editor}")
    caretaker.save(editor.save())
    
    # Write more
    editor.write("!")
    print(f"\nAfter writing '!':\n{editor}")
    caretaker.save(editor.save())
    
    # Undo
    print("\n--- Undo ---")
    memento = caretaker.undo()
    if memento:
        editor.restore(memento)
        print(f"After undo:\n{editor}")
    
    # Undo again
    print("\n--- Undo ---")
    memento = caretaker.undo()
    if memento:
        editor.restore(memento)
        print(f"After undo:\n{editor}")
    
    # Redo
    print("\n--- Redo ---")
    memento = caretaker.redo()
    if memento:
        editor.restore(memento)
        print(f"After redo:\n{editor}")
    
    print(f"\nCan undo: {caretaker.can_undo()}")
    print(f"Can redo: {caretaker.can_redo()}")
    
    print("\n=== Bank Account with Transaction History ===")
    
    account = BankAccount(1000.0)
    account_caretaker = Caretaker()
    
    # Initial state
    print(f"\nInitial state:\n{account}")
    account_caretaker.save(account.save())
    
    # Deposit
    account.deposit(500.0)
    print(f"\nAfter deposit:\n{account}")
    account_caretaker.save(account.save())
    
    # Withdraw
    account.withdraw(200.0)
    print(f"\nAfter withdrawal:\n{account}")
    account_caretaker.save(account.save())
    
    # Failed withdrawal
    account.withdraw(2000.0)
    print(f"\nAfter failed withdrawal:\n{account}")
    
    # Undo to before failed withdrawal
    print("\n--- Undo failed withdrawal ---")
    memento = account_caretaker.undo()
    if memento:
        account.restore(memento)
        print(f"After undo:\n{account}")
    
    # Show transaction history
    print(f"\nTransaction history:")
    for transaction in account.get_transaction_history():
        print(f"  {transaction}")
    
    print("\n=== Game Save System ===")
    
    game = GameState()
    save_manager = GameSaveManager(max_saves=3)
    
    # Play game
    print(f"\nInitial state: {game}")
    game.advance_level()
    game.add_score(50)
    game.add_item("sword")
    print(f"After playing: {game}")
    
    # Save to slot 0
    save_manager.save_game(game, 0)
    print(f"\nSaved to slot 0")
    
    # Continue playing
    game.advance_level()
    game.lose_life()
    game.add_item("shield")
    print(f"After more playing: {game}")
    
    # Save to slot 1
    save_manager.save_game(game, 1)
    print(f"Saved to slot 1")
    
    # Continue playing
    game.add_score(100)
    game.lose_life()
    print(f"After even more playing: {game}")
    
    # Load from slot 0
    print("\n--- Loading from slot 0 ---")
    save_manager.load_game(game, 0)
    print(f"Loaded state: {game}")
    
    # Load from slot 1
    print("\n--- Loading from slot 1 ---")
    save_manager.load_game(game, 1)
    print(f"Loaded state: {game}")
    
    # Show save info
    print("\n--- Save slots info ---")
    for i in range(3):
        info = save_manager.get_save_info(i)
        if info:
            print(f"Slot {i}: Level {info['level']}, Score {info['score']}, Saved at {info['timestamp']}")
        else:
            print(f"Slot {i}: Empty")


if __name__ == "__main__":
    main()
