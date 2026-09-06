"""
Priority Task Scheduler - Task scheduling with priority queue.
Features: Priority-based execution, task dependencies, and deadline management.
"""

import heapq
import time
from typing import Callable, Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    CRITICAL = 0


@dataclass
class Task:
    """Task to be scheduled."""
    id: str
    name: str
    func: Callable
    priority: TaskPriority = TaskPriority.MEDIUM
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    deadline: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __lt__(self, other: 'Task') -> bool:
        """Less than comparison for priority queue."""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at


class PriorityTaskScheduler:
    """Priority-based task scheduler."""
    
    def __init__(self) -> None:
        """Initialize scheduler."""
        self._tasks: Dict[str, Task] = {}
        self._task_queue: List[Task] = []
        self._completed_tasks: List[Task] = []
        self._running = False
    
    def add_task(self, task: Task) -> str:
        """
        Add task to scheduler.
        
        Args:
            task: Task to add
            
        Returns:
            Task ID
        """
        self._tasks[task.id] = task
        heapq.heappush(self._task_queue, task)
        return task.id
    
    def create_task(self, name: str, func: Callable, priority: TaskPriority = TaskPriority.MEDIUM,
                   args: tuple = (), kwargs: dict = None, dependencies: List[str] = None,
                   deadline: Optional[datetime] = None) -> str:
        """
        Create and add task.
        
        Args:
            name: Task name
            func: Function to execute
            priority: Task priority
            args: Function arguments
            kwargs: Function keyword arguments
            dependencies: Task IDs this task depends on
            deadline: Optional deadline
            
        Returns:
            Task ID
        """
        import uuid
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            name=name,
            func=func,
            priority=priority,
            args=args,
            kwargs=kwargs or {},
            dependencies=dependencies or [],
            deadline=deadline
        )
        
        return self.add_task(task)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if cancelled
        """
        if task_id in self._tasks:
            task = self._tasks[task_id]
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task or None
        """
        return self._tasks.get(task_id)
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [task for task in self._tasks.values() if task.status == TaskStatus.PENDING]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [task for task in self._tasks.values() if task.status == TaskStatus.COMPLETED]
    
    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks."""
        return [task for task in self._tasks.values() if task.status == TaskStatus.FAILED]
    
    def _check_dependencies(self, task: Task) -> bool:
        """
        Check if task dependencies are satisfied.
        
        Args:
            task: Task to check
            
        Returns:
            True if dependencies are satisfied
        """
        for dep_id in task.dependencies:
            dep_task = self._tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True
    
    def _check_deadline(self, task: Task) -> bool:
        """
        Check if task has passed deadline.
        
        Args:
            task: Task to check
            
        Returns:
            True if deadline not passed
        """
        if task.deadline:
            return datetime.now() < task.deadline
        return True
    
    def run_next(self) -> Optional[Task]:
        """
        Run the next available task.
        
        Returns:
            Task that was run or None
        """
        # Get next task that can run
        while self._task_queue:
            task = heapq.heappop(self._task_queue)
            
            # Skip if not pending
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check dependencies
            if not self._check_dependencies(task):
                # Put back in queue
                heapq.heappush(self._task_queue, task)
                continue
            
            # Check deadline
            if not self._check_deadline(task):
                task.status = TaskStatus.FAILED
                task.error = Exception("Deadline passed")
                self._completed_tasks.append(task)
                continue
            
            # Run task
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            try:
                result = task.func(*task.args, **task.kwargs)
                task.result = result
                task.status = TaskStatus.COMPLETED
            except Exception as e:
                task.error = e
                task.status = TaskStatus.FAILED
            
            task.completed_at = datetime.now()
            self._completed_tasks.append(task)
            
            return task
        
        return None
    
    def run_all(self) -> List[Task]:
        """
        Run all pending tasks.
        
        Returns:
            List of completed tasks
        """
        completed = []
        
        while self._task_queue:
            task = self.run_next()
            if task:
                completed.append(task)
        
        return completed
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get scheduler statistics.
        
        Returns:
            Statistics dictionary
        """
        total = len(self._tasks)
        pending = len(self.get_pending_tasks())
        completed = len(self.get_completed_tasks())
        failed = len(self.get_failed_tasks())
        cancelled = len([t for t in self._tasks.values() if t.status == TaskStatus.CANCELLED])
        
        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "success_rate": completed / total if total > 0 else 0
        }
    
    def clear_completed(self) -> None:
        """Clear completed tasks from memory."""
        for task in self._completed_tasks:
            if task.id in self._tasks:
                del self._tasks[task.id]
        self._completed_tasks.clear()
    
    def clear_all(self) -> None:
        """Clear all tasks."""
        self._tasks.clear()
        self._task_queue.clear()
        self._completed_tasks.clear()


def main() -> None:
    """Demonstrate priority task scheduler."""
    
    print("=== Priority Task Scheduler Demo ===")
    
    scheduler = PriorityTaskScheduler()
    
    # Define some tasks
    def task_a():
        print("Running Task A")
        time.sleep(0.1)
        return "A completed"
    
    def task_b():
        print("Running Task B")
        time.sleep(0.1)
        return "B completed"
    
    def task_c():
        print("Running Task C")
        time.sleep(0.1)
        return "C completed"
    
    def failing_task():
        print("Running failing task")
        raise Exception("Task failed!")
    
    # Add tasks with different priorities
    scheduler.create_task("Low Priority Task", task_a, TaskPriority.LOW)
    scheduler.create_task("Critical Task", task_b, TaskPriority.CRITICAL)
    scheduler.create_task("High Priority Task", task_c, TaskPriority.HIGH)
    scheduler.create_task("Failing Task", failing_task, TaskPriority.MEDIUM)
    
    # Add task with dependency
    dep_id = scheduler.create_task("Dependency Task", task_a, TaskPriority.MEDIUM)
    scheduler.create_task("Dependent Task", task_b, TaskPriority.HIGH, 
                        dependencies=[dep_id])
    
    print(f"\nTasks added: {len(scheduler._tasks)}")
    print(f"Pending tasks: {len(scheduler.get_pending_tasks())}")
    
    # Run all tasks
    print("\n--- Running tasks ---")
    completed = scheduler.run_all()
    
    print(f"\n--- Completed {len(completed)} tasks ---")
    
    # Show statistics
    stats = scheduler.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Pending: {stats['pending']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Cancelled: {stats['cancelled']}")
    print(f"  Success rate: {stats['success_rate']:.2%}")
    
    # Show task details
    print("\n--- Task Details ---")
    for task in scheduler._tasks.values():
        duration = None
        if task.started_at and task.completed_at:
            duration = (task.completed_at - task.started_at).total_seconds()
        
        print(f"\nTask: {task.name}")
        print(f"  Status: {task.status.value}")
        print(f"  Priority: {task.priority.name}")
        print(f"  Result: {task.result}")
        print(f"  Error: {task.error}")
        print(f"  Duration: {duration}s if duration else 'N/A'}")
    
    # Test deadline
    print("\n=== Deadline Test ===")
    scheduler2 = PriorityTaskScheduler()
    
    # Task with past deadline
    past_deadline = datetime.now() - timedelta(seconds=1)
    scheduler2.create_task("Past Deadline Task", task_a, 
                          TaskPriority.HIGH, deadline=past_deadline)
    
    # Task with future deadline
    future_deadline = datetime.now() + timedelta(seconds=10)
    scheduler2.create_task("Future Deadline Task", task_b, 
                          TaskPriority.HIGH, deadline=future_deadline)
    
    scheduler2.run_all()
    
    print(f"Past deadline task status: {scheduler2.get_task(scheduler2._tasks.keys().__iter__().__next__()).status.value}")


if __name__ == "__main__":
    main()
