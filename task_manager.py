"""
Task Manager - A simple task management system demonstrating OOP principles.
Features: Task creation, prioritization, completion tracking, and filtering.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional
from datetime import datetime


class Priority(Enum):
    """Task priority levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Status(Enum):
    """Task status options."""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()


@dataclass
class Task:
    """Represents a single task with metadata."""
    title: str
    description: str
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def mark_completed(self) -> None:
        """Mark task as completed with timestamp."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()

    def __str__(self) -> str:
        """String representation of task."""
        return f"[{self.priority.name}] {self.title} - {self.status.name}"


class TaskManager:
    """Manages a collection of tasks with filtering and operations."""

    def __init__(self) -> None:
        """Initialize an empty task manager."""
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a new task to the manager."""
        self.tasks.append(task)

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """Filter tasks by their status."""
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Filter tasks by their priority."""
        return [task for task in self.tasks if task.priority == priority]

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Filter tasks that contain a specific tag."""
        return [task for task in self.tasks if tag in task.tags]

    def complete_task(self, task_title: str) -> bool:
        """Mark a task as completed by title. Returns True if found."""
        for task in self.tasks:
            if task.title == task_title and task.status != Status.COMPLETED:
                task.mark_completed()
                return True
        return False

    def get_pending_count(self) -> int:
        """Return count of pending tasks."""
        return len(self.get_tasks_by_status(Status.PENDING))

    def get_completion_rate(self) -> float:
        """Calculate and return the completion rate as percentage."""
        if not self.tasks:
            return 0.0
        completed = len(self.get_tasks_by_status(Status.COMPLETED))
        return (completed / len(self.tasks)) * 100


def main() -> None:
    """Demonstrate the TaskManager functionality."""
    manager = TaskManager()

    # Create sample tasks
    task1 = Task("Learn Python", "Study Python fundamentals", Priority.HIGH)
    task1.tags = ["learning", "python"]
    
    task2 = Task("Build Project", "Create a portfolio project", Priority.MEDIUM)
    task2.tags = ["project", "coding"]
    
    task3 = Task("Read Documentation", "Read official docs", Priority.LOW)
    task3.tags = ["reading"]

    # Add tasks to manager
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)

    # Complete a task
    manager.complete_task("Learn Python")

    # Display statistics
    print(f"Total tasks: {len(manager.tasks)}")
    print(f"Pending tasks: {manager.get_pending_count()}")
    print(f"Completion rate: {manager.get_completion_rate():.1f}%")
    print("\nHigh priority tasks:")
    for task in manager.get_tasks_by_priority(Priority.HIGH):
        print(f"  - {task}")


if __name__ == "__main__":
    main()
