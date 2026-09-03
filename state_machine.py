"""
State Machine - Finite state machine implementation.
Features: State transitions, event handling, and state management.
"""

from typing import Dict, Callable, Optional, Any, List
from dataclasses import dataclass
from enum import Enum
import threading


class State(Enum):
    """Base state enum."""
    pass


@dataclass
class Transition:
    """State transition definition."""
    from_state: str
    to_state: str
    event: str
    action: Optional[Callable] = None
    guard: Optional[Callable] = None


class StateMachine:
    """Finite state machine implementation."""
    
    def __init__(self, initial_state: str) -> None:
        """
        Initialize state machine.
        
        Args:
            initial_state: Initial state name
        """
        self.current_state = initial_state
        self.transitions: Dict[str, List[Transition]] = {}
        self.state_callbacks: Dict[str, List[Callable]] = {}
        self._lock = threading.RLock()
    
    def add_transition(self, transition: Transition) -> None:
        """
        Add a state transition.
        
        Args:
            transition: Transition to add
        """
        if transition.from_state not in self.transitions:
            self.transitions[transition.from_state] = []
        self.transitions[transition.from_state].append(transition)
    
    def add_state_callback(self, state: str, callback: Callable) -> None:
        """
        Add callback for entering a state.
        
        Args:
            state: State name
            callback: Function to call when entering state
        """
        if state not in self.state_callbacks:
            self.state_callbacks[state] = []
        self.state_callbacks[state].append(callback)
    
    def handle_event(self, event: str, data: Any = None) -> bool:
        """
        Handle an event and perform state transition if valid.
        
        Args:
            event: Event name
            data: Optional data to pass to action
            
        Returns:
            True if transition occurred, False otherwise
        """
        with self._lock:
            if self.current_state not in self.transitions:
                return False
            
            for transition in self.transitions[self.current_state]:
                if transition.event == event:
                    # Check guard condition
                    if transition.guard and not transition.guard(data):
                        continue
                    
                    # Perform action
                    if transition.action:
                        transition.action(data)
                    
                    # Change state
                    old_state = self.current_state
                    self.current_state = transition.to_state
                    
                    # Call state callbacks
                    if self.current_state in self.state_callbacks:
                        for callback in self.state_callbacks[self.current_state]:
                            callback(old_state, self.current_state, data)
                    
                    return True
            
            return False
    
    def get_state(self) -> str:
        """Get current state."""
        return self.current_state
    
    def can_transition(self, event: str) -> bool:
        """
        Check if event can trigger a transition from current state.
        
        Args:
            event: Event name
            
        Returns:
            True if transition is possible
        """
        if self.current_state not in self.transitions:
            return False
        
        return any(t.event == event for t in self.transitions[self.current_state])
    
    def reset(self, state: str) -> None:
        """
        Reset state machine to specific state.
        
        Args:
            state: State to reset to
        """
        with self._lock:
            self.current_state = state


class TrafficLightController(StateMachine):
    """Traffic light controller using state machine."""
    
    def __init__(self) -> None:
        """Initialize traffic light controller."""
        super().__init__("red")
        self._setup_transitions()
    
    def _setup_transitions(self) -> None:
        """Set up traffic light transitions."""
        self.add_transition(Transition("red", "green", "timer"))
        self.add_transition(Transition("green", "yellow", "timer"))
        self.add_transition(Transition("yellow", "red", "timer"))
        
        self.add_state_callback("green", self._on_green)
        self.add_state_callback("yellow", self._on_yellow)
        self.add_state_callback("red", self._on_red)
    
    def _on_green(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when entering green state."""
        print(f"🟢 Green light (from {old_state})")
    
    def _on_yellow(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when entering yellow state."""
        print(f"🟡 Yellow light (from {old_state})")
    
    def _on_red(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when entering red state."""
        print(f"🔴 Red light (from {old_state})")
    
    def next_light(self) -> None:
        """Advance to next light."""
        self.handle_event("timer")


class OrderProcessor(StateMachine):
    """Order processing state machine."""
    
    def __init__(self) -> None:
        """Initialize order processor."""
        super().__init__("pending")
        self.order_data = {}
        self._setup_transitions()
    
    def _setup_transitions(self) -> None:
        """Set up order transitions."""
        self.add_transition(Transition("pending", "confirmed", "confirm", self._confirm_order))
        self.add_transition(Transition("confirmed", "processing", "process", self._process_order))
        self.add_transition(Transition("processing", "shipped", "ship", self._ship_order))
        self.add_transition(Transition("shipped", "delivered", "deliver", self._deliver_order))
        self.add_transition(Transition("pending", "cancelled", "cancel"))
        self.add_transition(Transition("confirmed", "cancelled", "cancel"))
        
        self.add_state_callback("confirmed", self._on_confirmed)
        self.add_state_callback("shipped", self._on_shipped)
        self.add_state_callback("delivered", self._on_delivered)
        self.add_state_callback("cancelled", self._on_cancelled)
    
    def _confirm_order(self, data: Any) -> None:
        """Confirm order action."""
        self.order_data.update(data or {})
        print(f"Order confirmed: {self.order_data.get('order_id')}")
    
    def _process_order(self, data: Any) -> None:
        """Process order action."""
        print(f"Processing order...")
    
    def _ship_order(self, data: Any) -> None:
        """Ship order action."""
        tracking = data.get("tracking") if data else "TRACK123"
        self.order_data["tracking"] = tracking
        print(f"Order shipped with tracking: {tracking}")
    
    def _deliver_order(self, data: Any) -> None:
        """Deliver order action."""
        print(f"Order delivered")
    
    def _on_confirmed(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when order confirmed."""
        print(f"✓ Order moved to confirmed state")
    
    def _on_shipped(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when order shipped."""
        print(f"✓ Order shipped")
    
    def _on_delivered(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when order delivered."""
        print(f"✓ Order delivered successfully")
    
    def _on_cancelled(self, old_state: str, new_state: str, data: Any) -> None:
        """Callback when order cancelled."""
        print(f"✗ Order cancelled")


class VendingMachine(StateMachine):
    """Vending machine state machine."""
    
    def __init__(self) -> None:
        """Initialize vending machine."""
        super().__init__("idle")
        self.balance = 0
        self.price = 2.0
        self._setup_transitions()
    
    def _setup_transitions(self) -> None:
        """Set up vending machine transitions."""
        self.add_transition(Transition("idle", "waiting", "insert_money", self._add_money))
        self.add_transition(Transition("waiting", "waiting", "insert_money", self._add_money))
        self.add_transition(Transition("waiting", "idle", "cancel", self._refund))
        self.add_transition(Transition("waiting", "dispensing", "select_item", guard=self._check_balance))
        self.add_transition(Transition("dispensing", "idle", "complete", self._dispense))
    
    def _add_money(self, data: Any) -> None:
        """Add money to balance."""
        amount = data if isinstance(data, (int, float)) else 0
        self.balance += amount
        print(f"Balance: ${self.balance:.2f}")
    
    def _check_balance(self, data: Any) -> bool:
        """Check if balance is sufficient."""
        return self.balance >= self.price
    
    def _refund(self, data: Any) -> None:
        """Refund money."""
        print(f"Refunding ${self.balance:.2f}")
        self.balance = 0
    
    def _dispense(self, data: Any) -> None:
        """Dispense item."""
        print(f"Dispensing item...")
        print(f"Change: ${self.balance - self.price:.2f}")
        self.balance = 0
    
    def insert_coin(self, amount: float) -> None:
        """Insert coin."""
        self.handle_event("insert_money", amount)
    
    def select_item(self) -> None:
        """Select item."""
        self.handle_event("select_item")
    
    def cancel(self) -> None:
        """Cancel transaction."""
        self.handle_event("cancel")
    
    def complete(self) -> None:
        """Complete transaction."""
        self.handle_event("complete")


def main() -> None:
    """Demonstrate state machine implementations."""
    
    print("=== Traffic Light Controller ===")
    traffic_light = TrafficLightController()
    
    for _ in range(6):
        traffic_light.next_light()
    
    print("\n=== Order Processor ===")
    order = OrderProcessor()
    
    order.handle_event("confirm", {"order_id": "ORD-123", "customer": "Alice"})
    order.handle_event("process")
    order.handle_event("ship", {"tracking": "TRK-456"})
    order.handle_event("deliver")
    
    print(f"\nFinal state: {order.get_state()}")
    
    print("\n=== Cancelled Order ===")
    order2 = OrderProcessor()
    order2.handle_event("confirm", {"order_id": "ORD-789"})
    order2.handle_event("cancel")
    print(f"Final state: {order2.get_state()}")
    
    print("\n=== Vending Machine ===")
    vending = VendingMachine()
    
    print(f"Initial state: {vending.get_state()}")
    vending.insert_coin(1.0)
    vending.insert_coin(0.5)
    print(f"Current state: {vending.get_state()}")
    
    # Try to select with insufficient balance
    vending.select_item()
    print(f"State after insufficient funds: {vending.get_state()}")
    
    # Add more money
    vending.insert_coin(1.0)
    vending.select_item()
    print(f"State after selection: {vending.get_state()}")
    
    vending.complete()
    print(f"Final state: {vending.get_state()}")
    
    print("\n=== Vending Machine - Cancel ===")
    vending2 = VendingMachine()
    vending2.insert_coin(2.0)
    vending2.cancel()
    print(f"Final state: {vending2.get_state()}")


if __name__ == "__main__":
    main()
