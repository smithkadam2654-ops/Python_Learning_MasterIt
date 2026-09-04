"""
Chain of Responsibility - Chain of responsibility pattern for request handling.
Features: Handler chain, request passing, and flexible responsibility assignment.
"""

from typing import Optional, Any
from abc import ABC, abstractmethod
from enum import Enum


class RequestType(Enum):
    """Types of requests."""
    PURCHASE = "purchase"
    REFUND = "refund"
    LEAVE = "leave"
    PROMOTION = "promotion"
    TECHNICAL = "technical"


class Request:
    """Request to be handled."""
    
    def __init__(self, request_type: RequestType, amount: float = 0, 
                 description: str = "") -> None:
        """
        Initialize request.
        
        Args:
            request_type: Type of request
            amount: Monetary amount (if applicable)
            description: Request description
        """
        self.request_type = request_type
        self.amount = amount
        self.description = description
        self.approved = False
        self.handled_by = None


class Handler(ABC):
    """Abstract handler in the chain."""
    
    def __init__(self) -> None:
        """Initialize handler."""
        self._next_handler: Optional['Handler'] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """
        Set the next handler in the chain.
        
        Args:
            handler: Next handler
            
        Returns:
            The handler that was set (for chaining)
        """
        self._next_handler = handler
        return handler
    
    def handle(self, request: Request) -> bool:
        """
        Handle request or pass to next handler.
        
        Args:
            request: Request to handle
            
        Returns:
            True if request was handled
        """
        if self.can_handle(request):
            self._handle_request(request)
            return True
        
        if self._next_handler:
            return self._next_handler.handle(request)
        
        return False
    
    @abstractmethod
    def can_handle(self, request: Request) -> bool:
        """Check if this handler can handle the request."""
        pass
    
    @abstractmethod
    def _handle_request(self, request: Request) -> None:
        """Actually handle the request."""
        pass


class Manager(Handler):
    """Manager handler for low-level approvals."""
    
    def can_handle(self, request: Request) -> bool:
        """Can handle purchases up to $1000."""
        if request.request_type == RequestType.PURCHASE:
            return request.amount <= 1000
        if request.request_type == RequestType.LEAVE:
            return True
        return False
    
    def _handle_request(self, request: Request) -> None:
        """Handle the request."""
        request.approved = True
        request.handled_by = "Manager"
        print(f"✓ Manager approved: {request.description}")


class Director(Handler):
    """Director handler for mid-level approvals."""
    
    def can_handle(self, request: Request) -> bool:
        """Can handle purchases up to $5000."""
        if request.request_type == RequestType.PURCHASE:
            return request.amount <= 5000
        if request.request_type == RequestType.REFUND:
            return request.amount <= 500
        return False
    
    def _handle_request(self, request: Request) -> None:
        """Handle the request."""
        request.approved = True
        request.handled_by = "Director"
        print(f"✓ Director approved: {request.description}")


class VicePresident(Handler):
    """Vice President handler for high-level approvals."""
    
    def can_handle(self, request: Request) -> bool:
        """Can handle purchases up to $20000."""
        if request.request_type == RequestType.PURCHASE:
            return request.amount <= 20000
        if request.request_type == RequestType.REFUND:
            return request.amount <= 2000
        if request.request_type == RequestType.PROMOTION:
            return True
        return False
    
    def _handle_request(self, request: Request) -> None:
        """Handle the request."""
        request.approved = True
        request.handled_by = "Vice President"
        print(f"✓ Vice President approved: {request.description}")


class CEO(Handler):
    """CEO handler for top-level approvals."""
    
    def can_handle(self, request: Request) -> bool:
        """Can handle any request."""
        return True
    
    def _handle_request(self, request: Request) -> None:
        """Handle the request."""
        request.approved = True
        request.handled_by = "CEO"
        print(f"✓ CEO approved: {request.description}")


class TechSupport(Handler):
    """Technical support handler."""
    
    def __init__(self, level: int) -> None:
        """
        Initialize tech support.
        
        Args:
            level: Support level (1=basic, 2=intermediate, 3=advanced)
        """
        super().__init__()
        self.level = level
    
    def can_handle(self, request: Request) -> bool:
        """Can handle technical requests based on level."""
        if request.request_type != RequestType.TECHNICAL:
            return False
        
        # Level 1: Basic issues
        if self.level == 1:
            return "basic" in request.description.lower()
        
        # Level 2: Intermediate issues
        if self.level == 2:
            return "intermediate" in request.description.lower() or "basic" in request.description.lower()
        
        # Level 3: Advanced issues
        return True
    
    def _handle_request(self, request: Request) -> None:
        """Handle the request."""
        request.approved = True
        request.handled_by = f"Tech Support Level {self.level}"
        print(f"✓ Tech Support Level {self.level} resolved: {request.description}")


class RequestChain:
    """Request chain manager."""
    
    def __init__(self) -> None:
        """Initialize request chain."""
        self.head: Optional[Handler] = None
    
    def add_handler(self, handler: Handler) -> 'RequestChain':
        """
        Add handler to chain.
        
        Args:
            handler: Handler to add
            
        Returns:
            Self for chaining
        """
        if self.head is None:
            self.head = handler
        else:
            current = self.head
            while current._next_handler:
                current = current._next_handler
            current.set_next(handler)
        return self
    
    def handle(self, request: Request) -> bool:
        """
        Handle request through chain.
        
        Args:
            request: Request to handle
            
        Returns:
            True if handled
        """
        if self.head:
            return self.head.handle(request)
        return False


def main() -> None:
    """Demonstrate chain of responsibility pattern."""
    
    print("=== Approval Chain ===")
    
    # Build approval chain
    chain = RequestChain()
    chain.add_handler(Manager())
    chain.add_handler(Director())
    chain.add_handler(VicePresident())
    chain.add_handler(CEO())
    
    # Test requests
    requests = [
        Request(RequestType.PURCHASE, 500, "Office supplies"),
        Request(RequestType.PURCHASE, 3000, "New laptops"),
        Request(RequestType.PURCHASE, 15000, "Server upgrade"),
        Request(RequestType.PURCHASE, 50000, "New building"),
        Request(RequestType.LEAVE, 0, "Vacation request"),
        Request(RequestType.REFUND, 300, "Customer refund"),
        Request(RequestType.PROMOTION, 0, "Employee promotion"),
    ]
    
    for request in requests:
        print(f"\nProcessing: {request.request_type.value} - {request.description}")
        handled = chain.handle(request)
        
        if not handled:
            print(f"✗ Request could not be handled")
        else:
            print(f"  Handled by: {request.handled_by}")
    
    print("\n=== Technical Support Chain ===")
    
    # Build tech support chain
    tech_chain = RequestChain()
    tech_chain.add_handler(TechSupport(1))
    tech_chain.add_handler(TechSupport(2))
    tech_chain.add_handler(TechSupport(3))
    
    tech_requests = [
        Request(RequestType.TECHNICAL, 0, "Basic password reset"),
        Request(RequestType.TECHNICAL, 0, "Intermediate software configuration"),
        Request(RequestType.TECHNICAL, 0, "Advanced system architecture issue"),
    ]
    
    for request in tech_requests:
        print(f"\nProcessing: {request.description}")
        handled = tech_chain.handle(request)
        
        if not handled:
            print(f"✗ Request could not be handled")
        else:
            print(f"  Handled by: {request.handled_by}")
    
    print("\n=== Dynamic Chain ===")
    
    # Build chain dynamically based on request type
    def build_chain_for_request(request_type: RequestType) -> RequestChain:
        """Build appropriate chain for request type."""
        chain = RequestChain()
        
        if request_type in (RequestType.PURCHASE, RequestType.REFUND):
            chain.add_handler(Manager())
            chain.add_handler(Director())
            chain.add_handler(CEO())
        elif request_type == RequestType.TECHNICAL:
            chain.add_handler(TechSupport(1))
            chain.add_handler(TechSupport(2))
            chain.add_handler(TechSupport(3))
        else:
            chain.add_handler(Manager())
            chain.add_handler(CEO())
        
        return chain
    
    # Test dynamic chains
    purchase_chain = build_chain_for_request(RequestType.PURCHASE)
    purchase_chain.handle(Request(RequestType.PURCHASE, 2000, "Office equipment"))
    
    tech_chain_dynamic = build_chain_for_request(RequestType.TECHNICAL)
    tech_chain_dynamic.handle(Request(RequestType.TECHNICAL, 0, "Basic issue"))
    
    print("\n=== Chain Modification ===")
    
    # Modify chain by removing a handler
    modified_chain = RequestChain()
    modified_chain.add_handler(Manager())
    # Skip Director
    modified_chain.add_handler(VicePresident())
    modified_chain.add_handler(CEO())
    
    print("Modified chain (Director skipped):")
    modified_chain.handle(Request(RequestType.PURCHASE, 3000, "Test purchase"))


if __name__ == "__main__":
    main()
