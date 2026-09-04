"""
Mediator Pattern - Mediator pattern for coordinating objects.
Features: Centralized communication, loose coupling, and flexible interaction.
"""

from typing import List, Optional
from abc import ABC, abstractmethod


class Mediator(ABC):
    """Mediator interface for coordinating components."""
    
    @abstractmethod
    def notify(self, sender: 'Component', event: str) -> None:
        """Notify mediator of an event."""
        pass


class Component:
    """Base component class."""
    
    def __init__(self, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize component.
        
        Args:
            mediator: Mediator for communication
        """
        self._mediator = mediator
    
    def set_mediator(self, mediator: Mediator) -> None:
        """Set the mediator."""
        self._mediator = mediator
    
    def send(self, event: str) -> None:
        """Send event through mediator."""
        if self._mediator:
            self._mediator.notify(self, event)


class Button(Component):
    """Button component."""
    
    def __init__(self, name: str, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize button.
        
        Args:
            name: Button name
            mediator: Mediator
        """
        super().__init__(mediator)
        self.name = name
        self.enabled = True
    
    def click(self) -> None:
        """Simulate button click."""
        if self.enabled:
            print(f"Button '{self.name}' clicked")
            self.send("click")
        else:
            print(f"Button '{self.name}' is disabled")
    
    def enable(self) -> None:
        """Enable button."""
        self.enabled = True
        print(f"Button '{self.name}' enabled")
    
    def disable(self) -> None:
        """Disable button."""
        self.enabled = False
        print(f"Button '{self.name}' disabled")


class TextBox(Component):
    """Text box component."""
    
    def __init__(self, name: str, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize text box.
        
        Args:
            name: Text box name
            mediator: Mediator
        """
        super().__init__(mediator)
        self.name = name
        self.text = ""
    
    def set_text(self, text: str) -> None:
        """Set text content."""
        self.text = text
        print(f"TextBox '{self.name}' text set to: '{text}'")
        self.send("text_changed")
    
    def get_text(self) -> str:
        """Get text content."""
        return self.text
    
    def clear(self) -> None:
        """Clear text."""
        self.text = ""
        print(f"TextBox '{self.name}' cleared")
        self.send("text_cleared")


class Checkbox(Component):
    """Checkbox component."""
    
    def __init__(self, name: str, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize checkbox.
        
        Args:
            name: Checkbox name
            mediator: Mediator
        """
        super().__init__(mediator)
        self.name = name
        self.checked = False
    
    def check(self) -> None:
        """Check the checkbox."""
        self.checked = True
        print(f"Checkbox '{self.name}' checked")
        self.send("checked")
    
    def uncheck(self) -> None:
        """Uncheck the checkbox."""
        self.checked = False
        print(f"Checkbox '{self.name}' unchecked")
        self.send("unchecked")
    
    def is_checked(self) -> bool:
        """Check if checked."""
        return self.checked


class LoginDialogMediator(Mediator):
    """Mediator for login dialog components."""
    
    def __init__(self) -> None:
        """Initialize mediator."""
        self.username_box: Optional[TextBox] = None
        self.password_box: Optional[TextBox] = None
        self.login_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None
        self.remember_checkbox: Optional[Checkbox] = None
    
    def set_username_box(self, box: TextBox) -> None:
        """Set username text box."""
        self.username_box = box
        box.set_mediator(self)
    
    def set_password_box(self, box: TextBox) -> None:
        """Set password text box."""
        self.password_box = box
        box.set_mediator(self)
    
    def set_login_button(self, button: Button) -> None:
        """Set login button."""
        self.login_button = button
        button.set_mediator(self)
    
    def set_cancel_button(self, button: Button) -> None:
        """Set cancel button."""
        self.cancel_button = button
        button.set_mediator(self)
    
    def set_remember_checkbox(self, checkbox: Checkbox) -> None:
        """Set remember checkbox."""
        self.remember_checkbox = checkbox
        checkbox.set_mediator(self)
    
    def notify(self, sender: Component, event: str) -> None:
        """Handle component events."""
        if sender == self.username_box and event == "text_changed":
            self._validate_login_button()
        
        elif sender == self.password_box and event == "text_changed":
            self._validate_login_button()
        
        elif sender == self.login_button and event == "click":
            self._handle_login()
        
        elif sender == self.cancel_button and event == "click":
            self._handle_cancel()
        
        elif sender == self.remember_checkbox:
            if event == "checked":
                print("Remember me enabled")
            elif event == "unchecked":
                print("Remember me disabled")
    
    def _validate_login_button(self) -> None:
        """Enable/disable login button based on input."""
        if self.username_box and self.password_box and self.login_button:
            has_username = len(self.username_box.get_text()) > 0
            has_password = len(self.password_box.get_text()) > 0
            
            if has_username and has_password:
                self.login_button.enable()
            else:
                self.login_button.disable()
    
    def _handle_login(self) -> None:
        """Handle login button click."""
        if self.username_box and self.password_box:
            username = self.username_box.get_text()
            password = self.password_box.get_text()
            print(f"Login attempt: username='{username}', password='{'*' * len(password)}'")
            
            if self.remember_checkbox and self.remember_checkbox.is_checked():
                print("Saving credentials (remember me enabled)")
    
    def _handle_cancel(self) -> None:
        """Handle cancel button click."""
        print("Login cancelled")
        if self.username_box:
            self.username_box.clear()
        if self.password_box:
            self.password_box.clear()
        if self.remember_checkbox:
            self.remember_checkbox.uncheck()


class ChatRoomMediator(Mediator):
    """Mediator for chat room participants."""
    
    def __init__(self) -> None:
        """Initialize chat room mediator."""
        self.participants: List['User'] = []
    
    def add_participant(self, participant: 'User') -> None:
        """Add participant to chat room."""
        self.participants.append(participant)
        participant.set_mediator(self)
        print(f"{participant.name} joined the chat")
    
    def remove_participant(self, participant: 'User') -> None:
        """Remove participant from chat room."""
        if participant in self.participants:
            self.participants.remove(participant)
            print(f"{participant.name} left the chat")
    
    def notify(self, sender: Component, event: str) -> None:
        """Handle chat events."""
        if isinstance(sender, User) and event == "message":
            self._broadcast_message(sender, sender.last_message)
    
    def _broadcast_message(self, sender: 'User', message: str) -> None:
        """Broadcast message to all participants except sender."""
        for participant in self.participants:
            if participant != sender:
                participant.receive_message(sender.name, message)


class User(Component):
    """Chat user component."""
    
    def __init__(self, name: str, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize user.
        
        Args:
            name: User name
            mediator: Mediator
        """
        super().__init__(mediator)
        self.name = name
        self.last_message = ""
    
    def send_message(self, message: str) -> None:
        """Send message."""
        self.last_message = message
        print(f"{self.name}: {message}")
        self.send("message")
    
    def receive_message(self, sender_name: str, message: str) -> None:
        """Receive message."""
        print(f"{self.name} received from {sender_name}: {message}")


class AirTrafficControlMediator(Mediator):
    """Mediator for air traffic control."""
    
    def __init__(self) -> None:
        """Initialize ATC mediator."""
        self.aircrafts: List['Aircraft'] = []
        self.runways: List['Runway'] = []
    
    def register_aircraft(self, aircraft: 'Aircraft') -> None:
        """Register aircraft."""
        self.aircrafts.append(aircraft)
        aircraft.set_mediator(self)
        print(f"ATC: Aircraft {aircraft.callsign} registered")
    
    def register_runway(self, runway: 'Runway') -> None:
        """Register runway."""
        self.runways.append(runway)
        runway.set_mediator(self)
        print(f"ATC: Runway {runway.number} registered")
    
    def notify(self, sender: Component, event: str) -> None:
        """Handle ATC events."""
        if isinstance(sender, Aircraft) and event == "request_landing":
            self._handle_landing_request(sender)
        elif isinstance(sender, Aircraft) and event == "request_takeoff":
            self._handle_takeoff_request(sender)
        elif isinstance(sender, Runway) and event == "runway_free":
            self._handle_runway_free(sender)
    
    def _handle_landing_request(self, aircraft: 'Aircraft') -> None:
        """Handle landing request."""
        for runway in self.runways:
            if not runway.occupied:
                runway.occupy(aircraft)
                aircraft.receive_clearance(f"cleared to land on runway {runway.number}")
                return
        
        aircraft.receive_clearance("hold pattern - no runways available")
    
    def _handle_takeoff_request(self, aircraft: 'Aircraft') -> None:
        """Handle takeoff request."""
        for runway in self.runways:
            if runway.occupied_by == aircraft:
                runway.release()
                aircraft.receive_clearance(f"cleared for takeoff from runway {runway.number}")
                return
        
        aircraft.receive_clearance("cannot take off - not on a runway")
    
    def _handle_runway_free(self, runway: 'Runway') -> None:
        """Handle runway becoming free."""
        print(f"ATC: Runway {runway.number} is now free")


class Aircraft(Component):
    """Aircraft component."""
    
    def __init__(self, callsign: str, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize aircraft.
        
        Args:
            callsign: Aircraft callsign
            mediator: Mediator
        """
        super().__init__(mediator)
        self.callsign = callsign
    
    def request_landing(self) -> None:
        """Request landing clearance."""
        print(f"{self.callsign}: Requesting landing clearance")
        self.send("request_landing")
    
    def request_takeoff(self) -> None:
        """Request takeoff clearance."""
        print(f"{self.callsign}: Requesting takeoff clearance")
        self.send("request_takeoff")
    
    def receive_clearance(self, message: str) -> None:
        """Receive ATC clearance."""
        print(f"{self.callsign}: {message}")


class Runway(Component):
    """Runway component."""
    
    def __init__(self, number: int, mediator: Optional[Mediator] = None) -> None:
        """
        Initialize runway.
        
        Args:
            number: Runway number
            mediator: Mediator
        """
        super().__init__(mediator)
        self.number = number
        self.occupied = False
        self.occupied_by: Optional[Aircraft] = None
    
    def occupy(self, aircraft: Aircraft) -> None:
        """Occupy runway."""
        self.occupied = True
        self.occupied_by = aircraft
        print(f"Runway {self.number} occupied by {aircraft.callsign}")
    
    def release(self) -> None:
        """Release runway."""
        self.occupied = False
        self.occupied_by = None
        print(f"Runway {self.number} released")
        self.send("runway_free")


def main() -> None:
    """Demonstrate mediator pattern."""
    
    print("=== Login Dialog Mediator ===")
    
    login_mediator = LoginDialogMediator()
    
    username_box = TextBox("Username")
    password_box = TextBox("Password")
    login_button = Button("Login")
    cancel_button = Button("Cancel")
    remember_checkbox = Checkbox("Remember me")
    
    login_mediator.set_username_box(username_box)
    login_mediator.set_password_box(password_box)
    login_mediator.set_login_button(login_button)
    login_mediator.set_cancel_button(cancel_button)
    login_mediator.set_remember_checkbox(remember_checkbox)
    
    # Initial state - login button disabled
    print("\n--- Initial state ---")
    login_button.click()
    
    # Enter username
    print("\n--- Enter username ---")
    username_box.set_text("alice")
    
    # Enter password
    print("\n--- Enter password ---")
    password_box.set_text("password123")
    
    # Now login button should be enabled
    print("\n--- Click login ---")
    login_button.click()
    
    # Test remember me
    print("\n--- Toggle remember me ---")
    remember_checkbox.check()
    
    # Test cancel
    print("\n--- Click cancel ---")
    cancel_button.click()
    
    print("\n=== Chat Room Mediator ===")
    
    chat_mediator = ChatRoomMediator()
    
    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie")
    
    chat_mediator.add_participant(alice)
    chat_mediator.add_participant(bob)
    chat_mediator.add_participant(charlie)
    
    print("\n--- Alice sends message ---")
    alice.send_message("Hello everyone!")
    
    print("\n--- Bob sends message ---")
    bob.send_message("Hi Alice!")
    
    print("\n--- Charlie leaves ---")
    chat_mediator.remove_participant(charlie)
    
    print("\n--- Alice sends message ---")
    alice.send_message("Is anyone there?")
    
    print("\n=== Air Traffic Control Mediator ===")
    
    atc_mediator = AirTrafficControlMediator()
    
    runway1 = Runway(1)
    runway2 = Runway(2)
    
    atc_mediator.register_runway(runway1)
    atc_mediator.register_runway(runway2)
    
    flight1 = Aircraft("FL123")
    flight2 = Aircraft("FL456")
    flight3 = Aircraft("FL789")
    
    atc_mediator.register_aircraft(flight1)
    atc_mediator.register_aircraft(flight2)
    atc_mediator.register_aircraft(flight3)
    
    print("\n--- Flight 1 requests landing ---")
    flight1.request_landing()
    
    print("\n--- Flight 2 requests landing ---")
    flight2.request_landing()
    
    print("\n--- Flight 3 requests landing ---")
    flight3.request_landing()
    
    print("\n--- Flight 1 requests takeoff ---")
    flight1.request_takeoff()
    
    print("\n--- Flight 3 requests landing (runway now free) ---")
    flight3.request_landing()


if __name__ == "__main__":
    main()
