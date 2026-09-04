"""
Command Pattern - Command pattern for encapsulating requests.
Features: Command execution, undo/redo, and command queuing.
"""

from typing import List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import threading


class CommandStatus(Enum):
    """Command execution status."""
    PENDING = "pending"
    EXECUTED = "executed"
    UNDONE = "undone"
    FAILED = "failed"


class Command:
    """Base command class."""
    
    def execute(self) -> Any:
        """Execute the command."""
        raise NotImplementedError
    
    def undo(self) -> Any:
        """Undo the command."""
        raise NotImplementedError
    
    def can_undo(self) -> bool:
        """Check if command can be undone."""
        return True


class SimpleCommand(Command):
    """Simple command with execute and undo functions."""
    
    def __init__(self, execute_func: Callable, undo_func: Optional[Callable] = None) -> None:
        """
        Initialize simple command.
        
        Args:
            execute_func: Function to execute
            undo_func: Optional function to undo
        """
        self.execute_func = execute_func
        self.undo_func = undo_func
        self.status = CommandStatus.PENDING
    
    def execute(self) -> Any:
        """Execute the command."""
        try:
            result = self.execute_func()
            self.status = CommandStatus.EXECUTED
            return result
        except Exception as e:
            self.status = CommandStatus.FAILED
            raise e
    
    def undo(self) -> Any:
        """Undo the command."""
        if self.undo_func:
            result = self.undo_func()
            self.status = CommandStatus.UNDONE
            return result
        raise NotImplementedError("Undo not implemented for this command")


class MacroCommand(Command):
    """Macro command that executes multiple commands."""
    
    def __init__(self, commands: List[Command]) -> None:
        """
        Initialize macro command.
        
        Args:
            commands: List of commands to execute
        """
        self.commands = commands
        self.status = CommandStatus.PENDING
    
    def execute(self) -> List[Any]:
        """Execute all commands in sequence."""
        results = []
        for command in self.commands:
            result = command.execute()
            results.append(result)
        self.status = CommandStatus.EXECUTED
        return results
    
    def undo(self) -> List[Any]:
        """Undo all commands in reverse order."""
        results = []
        for command in reversed(self.commands):
            if command.can_undo():
                result = command.undo()
                results.append(result)
        self.status = CommandStatus.UNDONE
        return results


class CommandInvoker:
    """Command invoker with undo/redo support."""
    
    def __init__(self) -> None:
        """Initialize command invoker."""
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []
        self._lock = threading.RLock()
    
    def execute(self, command: Command) -> Any:
        """
        Execute a command.
        
        Args:
            command: Command to execute
            
        Returns:
            Command result
        """
        with self._lock:
            result = command.execute()
            self._history.append(command)
            self._redo_stack.clear()
            return result
    
    def undo(self) -> Optional[Any]:
        """
        Undo the last command.
        
        Returns:
            Undo result
        """
        with self._lock:
            if not self._history:
                return None
            
            command = self._history.pop()
            result = command.undo()
            self._redo_stack.append(command)
            return result
    
    def redo(self) -> Optional[Any]:
        """
        Redo the last undone command.
        
        Returns:
            Redo result
        """
        with self._lock:
            if not self._redo_stack:
                return None
            
            command = self._redo_stack.pop()
            result = command.execute()
            self._history.append(command)
            return result
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._history) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def clear_history(self) -> None:
        """Clear command history."""
        with self._lock:
            self._history.clear()
            self._redo_stack.clear()


class CommandQueue:
    """Queue for executing commands asynchronously."""
    
    def __init__(self) -> None:
        """Initialize command queue."""
        self._queue: List[Command] = []
        self._running = False
        self._thread = None
        self._lock = threading.RLock()
    
    def enqueue(self, command: Command) -> None:
        """
        Add command to queue.
        
        Args:
            command: Command to enqueue
        """
        with self._lock:
            self._queue.append(command)
    
    def start(self) -> None:
        """Start processing the queue."""
        with self._lock:
            if not self._running:
                self._running = True
                self._thread = threading.Thread(target=self._process_queue, daemon=True)
                self._thread.start()
    
    def stop(self) -> None:
        """Stop processing the queue."""
        with self._lock:
            self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def _process_queue(self) -> None:
        """Process commands from queue."""
        while self._running:
            with self._lock:
                if self._queue:
                    command = self._queue.pop(0)
                else:
                    command = None
            
            if command:
                try:
                    command.execute()
                except Exception as e:
                    print(f"Command execution failed: {e}")
            
            import time
            time.sleep(0.1)


# Example commands
class Light:
    """Light device."""
    
    def __init__(self) -> None:
        """Initialize light."""
        self.on = False
    
    def turn_on(self) -> None:
        """Turn light on."""
        self.on = True
        print("Light is ON")
    
    def turn_off(self) -> None:
        """Turn light off."""
        self.on = False
        print("Light is OFF")


class LightOnCommand(Command):
    """Command to turn on light."""
    
    def __init__(self, light: Light) -> None:
        """Initialize command."""
        self.light = light
    
    def execute(self) -> None:
        """Execute command."""
        self.light.turn_on()
    
    def undo(self) -> None:
        """Undo command."""
        self.light.turn_off()


class LightOffCommand(Command):
    """Command to turn off light."""
    
    def __init__(self, light: Light) -> None:
        """Initialize command."""
        self.light = light
    
    def execute(self) -> None:
        """Execute command."""
        self.light.turn_off()
    
    def undo(self) -> None:
        """Undo command."""
        self.light.turn_on()


class Thermostat:
    """Thermostat device."""
    
    def __init__(self) -> None:
        """Initialize thermostat."""
        self.temperature = 20
        self.previous_temperature = 20
    
    def set_temperature(self, temp: int) -> None:
        """Set temperature."""
        self.previous_temperature = self.temperature
        self.temperature = temp
        print(f"Temperature set to {temp}°C")
    
    def undo(self) -> None:
        """Undo temperature change."""
        self.temperature = self.previous_temperature
        print(f"Temperature reverted to {self.temperature}°C")


class SetTemperatureCommand(Command):
    """Command to set temperature."""
    
    def __init__(self, thermostat: Thermostat, temperature: int) -> None:
        """Initialize command."""
        self.thermostat = thermostat
        self.temperature = temperature
    
    def execute(self) -> None:
        """Execute command."""
        self.thermostat.set_temperature(self.temperature)
    
    def undo(self) -> None:
        """Undo command."""
        self.thermostat.undo()


def main() -> None:
    """Demonstrate command pattern."""
    
    print("=== Simple Command ===")
    counter = [0]
    
    def increment():
        counter[0] += 1
        print(f"Counter: {counter[0]}")
    
    def decrement():
        counter[0] -= 1
        print(f"Counter: {counter[0]}")
    
    inc_command = SimpleCommand(increment, decrement)
    
    inc_command.execute()
    inc_command.execute()
    inc_command.undo()
    
    print("\n=== Light Commands ===")
    light = Light()
    
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)
    
    invoker = CommandInvoker()
    
    invoker.execute(light_on)
    invoker.execute(light_off)
    invoker.execute(light_on)
    
    print("\n--- Undo ---")
    invoker.undo()
    invoker.undo()
    
    print("\n--- Redo ---")
    invoker.redo()
    
    print(f"\nCan undo: {invoker.can_undo()}")
    print(f"Can redo: {invoker.can_redo()}")
    
    print("\n=== Macro Command ===")
    thermostat = Thermostat()
    
    temp_commands = [
        SetTemperatureCommand(thermostat, 22),
        SetTemperatureCommand(thermostat, 24),
        SetTemperatureCommand(thermostat, 26)
    ]
    
    macro = MacroCommand(temp_commands)
    
    print("Executing macro:")
    macro.execute()
    
    print("\nUndoing macro:")
    macro.undo()
    
    print("\n=== Command Queue ===")
    queue = CommandQueue()
    
    queue.enqueue(light_on)
    queue.enqueue(light_off)
    queue.enqueue(light_on)
    
    queue.start()
    
    import time
    time.sleep(1.0)
    
    queue.stop()
    
    print("\n=== Complex Scenario ===")
    invoker2 = CommandInvoker()
    
    # Create a complex sequence
    living_room_light = Light()
    bedroom_light = Light()
    thermostat = Thermostat()
    
    commands = [
        LightOnCommand(living_room_light),
        SetTemperatureCommand(thermostat, 22),
        LightOnCommand(bedroom_light),
        SetTemperatureCommand(thermostat, 24),
    ]
    
    print("Morning routine:")
    for cmd in commands:
        invoker2.execute(cmd)
    
    print("\nUndo morning routine:")
    for _ in range(4):
        invoker2.undo()


if __name__ == "__main__":
    main()
