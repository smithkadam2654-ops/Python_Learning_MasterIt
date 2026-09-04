"""
Iterator Pattern - Iterator pattern for traversing collections.
Features: Custom iterators, aggregate collections, and traversal control.
"""

from typing import Iterator, Iterable, List, Any, Optional
from abc import ABC, abstractmethod


class Iterator(ABC):
    """Iterator interface."""
    
    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements."""
        pass
    
    @abstractmethod
    def next(self) -> Any:
        """Get next element."""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset iterator to beginning."""
        pass


class Aggregate(ABC):
    """Aggregate interface."""
    
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Create iterator for this aggregate."""
        pass


class Book:
    """Book item."""
    
    def __init__(self, title: str, author: str) -> None:
        """
        Initialize book.
        
        Args:
            title: Book title
            author: Book author
        """
        self.title = title
        self.author = author
    
    def __str__(self) -> str:
        """String representation."""
        return f"'{self.title}' by {self.author}"


class BookCollection(Aggregate):
    """Collection of books."""
    
    def __init__(self) -> None:
        """Initialize book collection."""
        self._books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        """Add book to collection."""
        self._books.append(book)
    
    def remove_book(self, book: Book) -> None:
        """Remove book from collection."""
        if book in self._books:
            self._books.remove(book)
    
    def create_iterator(self) -> Iterator:
        """Create iterator for books."""
        return BookIterator(self._books)
    
    def get_book_count(self) -> int:
        """Get number of books."""
        return len(self._books)


class BookIterator(Iterator):
    """Iterator for book collection."""
    
    def __init__(self, books: List[Book]) -> None:
        """
        Initialize iterator.
        
        Args:
            books: List of books to iterate
        """
        self._books = books
        self._position = 0
    
    def has_next(self) -> bool:
        """Check if there are more books."""
        return self._position < len(self._books)
    
    def next(self) -> Book:
        """Get next book."""
        if not self.has_next():
            raise StopIteration("No more books")
        
        book = self._books[self._position]
        self._position += 1
        return book
    
    def reset(self) -> None:
        """Reset iterator to beginning."""
        self._position = 0


class ReverseBookIterator(Iterator):
    """Reverse iterator for book collection."""
    
    def __init__(self, books: List[Book]) -> None:
        """
        Initialize reverse iterator.
        
        Args:
            books: List of books to iterate
        """
        self._books = books
        self._position = len(books) - 1
    
    def has_next(self) -> bool:
        """Check if there are more books."""
        return self._position >= 0
    
    def next(self) -> Book:
        """Get next book."""
        if not self.has_next():
            raise StopIteration("No more books")
        
        book = self._books[self._position]
        self._position -= 1
        return book
    
    def reset(self) -> None:
        """Reset iterator to end."""
        self._position = len(self._books) - 1


class FilteredBookIterator(Iterator):
    """Iterator that filters books by author."""
    
    def __init__(self, books: List[Book], author: str) -> None:
        """
        Initialize filtered iterator.
        
        Args:
            books: List of books to iterate
            author: Author to filter by
        """
        self._books = books
        self._author = author
        self._position = 0
        self._find_next()
    
    def _find_next(self) -> None:
        """Find next book matching author."""
        while self._position < len(self._books):
            if self._books[self._position].author == self._author:
                break
            self._position += 1
    
    def has_next(self) -> bool:
        """Check if there are more books."""
        return self._position < len(self._books)
    
    def next(self) -> Book:
        """Get next book."""
        if not self.has_next():
            raise StopIteration("No more books")
        
        book = self._books[self._position]
        self._position += 1
        self._find_next()
        return book
    
    def reset(self) -> None:
        """Reset iterator to beginning."""
        self._position = 0
        self._find_next()


class TreeNode:
    """Tree node for binary tree."""
    
    def __init__(self, value: int) -> None:
        """
        Initialize tree node.
        
        Args:
            value: Node value
        """
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinaryTree:
    """Binary tree with iterator support."""
    
    def __init__(self) -> None:
        """Initialize binary tree."""
        self.root: Optional[TreeNode] = None
    
    def insert(self, value: int) -> None:
        """Insert value into tree."""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """Recursively insert value."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def create_inorder_iterator(self) -> Iterator:
        """Create in-order traversal iterator."""
        return InOrderIterator(self.root)
    
    def create_preorder_iterator(self) -> Iterator:
        """Create pre-order traversal iterator."""
        return PreOrderIterator(self.root)
    
    def create_postorder_iterator(self) -> Iterator:
        """Create post-order traversal iterator."""
        return PostOrderIterator(self.root)


class InOrderIterator(Iterator):
    """In-order traversal iterator."""
    
    def __init__(self, root: Optional[TreeNode]) -> None:
        """Initialize in-order iterator."""
        self._stack: List[TreeNode] = []
        self._current = root
        self._push_left()
    
    def _push_left(self) -> None:
        """Push all left nodes to stack."""
        while self._current:
            self._stack.append(self._current)
            self._current = self._current.left
    
    def has_next(self) -> bool:
        """Check if there are more nodes."""
        return len(self._stack) > 0
    
    def next(self) -> int:
        """Get next node value."""
        if not self.has_next():
            raise StopIteration("No more nodes")
        
        node = self._stack.pop()
        self._current = node.right
        self._push_left()
        return node.value
    
    def reset(self) -> None:
        """Reset iterator."""
        self._stack.clear()
        self._current = None


class PreOrderIterator(Iterator):
    """Pre-order traversal iterator."""
    
    def __init__(self, root: Optional[TreeNode]) -> None:
        """Initialize pre-order iterator."""
        self._stack: List[TreeNode] = []
        if root:
            self._stack.append(root)
    
    def has_next(self) -> bool:
        """Check if there are more nodes."""
        return len(self._stack) > 0
    
    def next(self) -> int:
        """Get next node value."""
        if not self.has_next():
            raise StopIteration("No more nodes")
        
        node = self._stack.pop()
        
        if node.right:
            self._stack.append(node.right)
        if node.left:
            self._stack.append(node.left)
        
        return node.value
    
    def reset(self) -> None:
        """Reset iterator."""
        self._stack.clear()


class PostOrderIterator(Iterator):
    """Post-order traversal iterator."""
    
    def __init__(self, root: Optional[TreeNode]) -> None:
        """Initialize post-order iterator."""
        self._stack1: List[TreeNode] = []
        self._stack2: List[TreeNode] = []
        
        if root:
            self._stack1.append(root)
            while self._stack1:
                node = self._stack1.pop()
                self._stack2.append(node)
                
                if node.left:
                    self._stack1.append(node.left)
                if node.right:
                    self._stack1.append(node.right)
    
    def has_next(self) -> bool:
        """Check if there are more nodes."""
        return len(self._stack2) > 0
    
    def next(self) -> int:
        """Get next node value."""
        if not self.has_next():
            raise StopIteration("No more nodes")
        
        return self._stack2.pop().value
    
    def reset(self) -> None:
        """Reset iterator."""
        self._stack1.clear()
        self._stack2.clear()


class Page:
    """Page in a document."""
    
    def __init__(self, content: str) -> None:
        """Initialize page."""
        self.content = content
    
    def __str__(self) -> str:
        """String representation."""
        return f"Page: {self.content[:30]}..."


class Document(Aggregate):
    """Document with pages."""
    
    def __init__(self) -> None:
        """Initialize document."""
        self._pages: List[Page] = []
    
    def add_page(self, page: Page) -> None:
        """Add page to document."""
        self._pages.append(page)
    
    def create_iterator(self) -> Iterator:
        """Create iterator for pages."""
        return PageIterator(self._pages)
    
    def create_reverse_iterator(self) -> Iterator:
        """Create reverse iterator for pages."""
        return ReversePageIterator(self._pages)


class PageIterator(Iterator):
    """Iterator for document pages."""
    
    def __init__(self, pages: List[Page]) -> None:
        """Initialize page iterator."""
        self._pages = pages
        self._position = 0
    
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return self._position < len(self._pages)
    
    def next(self) -> Page:
        """Get next page."""
        if not self.has_next():
            raise StopIteration("No more pages")
        
        page = self._pages[self._position]
        self._position += 1
        return page
    
    def reset(self) -> None:
        """Reset iterator."""
        self._position = 0


class ReversePageIterator(Iterator):
    """Reverse iterator for document pages."""
    
    def __init__(self, pages: List[Page]) -> None:
        """Initialize reverse page iterator."""
        self._pages = pages
        self._position = len(pages) - 1
    
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return self._position >= 0
    
    def next(self) -> Page:
        """Get next page."""
        if not self.has_next():
            raise StopIteration("No more pages")
        
        page = self._pages[self._position]
        self._position -= 1
        return page
    
    def reset(self) -> None:
        """Reset iterator."""
        self._position = len(self._pages) - 1


def main() -> None:
    """Demonstrate iterator pattern."""
    
    print("=== Book Collection Iterator ===")
    
    collection = BookCollection()
    
    # Add books
    collection.add_book(Book("Python 101", "John Smith"))
    collection.add_book(Book("Design Patterns", "Jane Doe"))
    collection.add_book(Book("Clean Code", "Bob Johnson"))
    collection.add_book(Book("Refactoring", "Jane Doe"))
    collection.add_book(Book("The Pragmatic Programmer", "Alice Brown"))
    
    # Forward iteration
    print("\nForward iteration:")
    iterator = collection.create_iterator()
    while iterator.has_next():
        print(f"  {iterator.next()}")
    
    # Reverse iteration
    print("\nReverse iteration:")
    reverse_iterator = ReverseBookIterator(collection._books)
    while reverse_iterator.has_next():
        print(f"  {reverse_iterator.next()}")
    
    # Filtered iteration
    print("\nFiltered by author 'Jane Doe':")
    filtered_iterator = FilteredBookIterator(collection._books, "Jane Doe")
    while filtered_iterator.has_next():
        print(f"  {filtered_iterator.next()}")
    
    print("\n=== Binary Tree Iterators ===")
    
    tree = BinaryTree()
    
    # Build tree
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree.insert(value)
    
    # In-order traversal
    print("\nIn-order traversal:")
    inorder = tree.create_inorder_iterator()
    while inorder.has_next():
        print(f"  {inorder.next()}", end=" ")
    print()
    
    # Pre-order traversal
    print("\nPre-order traversal:")
    preorder = tree.create_preorder_iterator()
    while preorder.has_next():
        print(f"  {preorder.next()}", end=" ")
    print()
    
    # Post-order traversal
    print("\nPost-order traversal:")
    postorder = tree.create_postorder_iterator()
    while postorder.has_next():
        print(f"  {postorder.next()}", end=" ")
    print()
    
    print("\n=== Document Page Iterators ===")
    
    document = Document()
    
    # Add pages
    document.add_page(Page("Chapter 1: Introduction"))
    document.add_page(Page("Chapter 2: Getting Started"))
    document.add_page(Page("Chapter 3: Advanced Topics"))
    document.add_page(Page("Chapter 4: Conclusion"))
    
    # Forward iteration
    print("\nForward iteration:")
    page_iterator = document.create_iterator()
    while page_iterator.has_next():
        print(f"  {page_iterator.next()}")
    
    # Reverse iteration
    print("\nReverse iteration:")
    reverse_page_iterator = document.create_reverse_iterator()
    while reverse_page_iterator.has_next():
        print(f"  {reverse_page_iterator.next()}")
    
    print("\n=== Iterator Benefits ===")
    print("1. Provides a uniform interface for traversing different collections")
    print("2. Hides the internal structure of the collection")
    print("3. Allows multiple traversals simultaneously")
    print("4. Easy to add new traversal types without changing the collection")


if __name__ == "__main__":
    main()
