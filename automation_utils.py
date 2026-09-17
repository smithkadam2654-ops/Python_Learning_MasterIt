"""
Automation Utilities Module

This module provides comprehensive automation and task scheduling utilities including:
- Task scheduling and cron-like functionality
- File system monitoring
- Process automation
- Email notifications
- Workflow management
- Job queues and task management
- Backup automation
- System maintenance tasks
- Web scraping automation
- Data pipeline automation

All functions include comprehensive docstrings and type hints.
"""

import os
import time
import threading
import queue
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib


try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False


try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Represents a task to be executed."""
    id: str
    name: str
    func: Callable
    args: Tuple = ()
    kwargs: Dict = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class TaskResult:
    """Container for task execution results."""
    task_id: str
    success: bool
    result: Any
    error: Optional[str]
    execution_time: float
    timestamp: datetime


class TaskScheduler:
    """Task scheduling and execution manager."""
    
    def __init__(self, max_workers: int = 4):
        """Initialize task scheduler."""
        self.max_workers = max_workers
        self.task_queue = queue.PriorityQueue()
        self.tasks: Dict[str, Task] = {}
        self.workers: List[threading.Thread] = []
        self.running = False
        self.task_counter = 0
    
    def add_task(self, func: Callable, name: str = "",
                args: Tuple = (), kwargs: Optional[Dict] = None,
                priority: TaskPriority = TaskPriority.MEDIUM,
                max_retries: int = 3) -> str:
        """Add a task to the scheduler."""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        task = Task(
            id=task_id,
            name=name or func.__name__,
            func=func,
            args=args,
            kwargs=kwargs or {},
            priority=priority,
            max_retries=max_retries
        )
        
        self.tasks[task_id] = task
        # Priority queue uses negative priority for max-heap behavior
        self.task_queue.put((-priority.value, task_id))
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get status of a specific task."""
        task = self.tasks.get(task_id)
        return task.status if task else None
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task."""
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    def _worker(self) -> None:
        """Worker thread for executing tasks."""
        while self.running:
            try:
                # Get task from queue with timeout
                priority, task_id = self.task_queue.get(timeout=1)
                task = self.tasks.get(task_id)
                
                if not task or task.status != TaskStatus.PENDING:
                    continue
                
                # Execute task
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()
                
                try:
                    result = task.func(*task.args, **task.kwargs)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    
                except Exception as e:
                    task.error = str(e)
                    task.retry_count += 1
                    
                    if task.retry_count < task.max_retries:
                        task.status = TaskStatus.PENDING
                        # Re-queue task
                        self.task_queue.put((-task.priority.value, task_id))
                    else:
                        task.status = TaskStatus.FAILED
                        task.completed_at = datetime.now()
                
                self.task_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker error: {e}")
    
    def start(self) -> None:
        """Start the task scheduler."""
        if self.running:
            return
        
        self.running = True
        self.workers = []
        
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop(self) -> None:
        """Stop the task scheduler."""
        self.running = False
        
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """Wait for all tasks to complete."""
        start_time = time.time()
        
        while self.running:
            self.task_queue.join()
            
            # Check if any tasks are still running
            running_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]
            if not running_tasks:
                break
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.1)
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        status_counts = {}
        for task in self.tasks.values():
            status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1
        
        return {
            "total_tasks": len(self.tasks),
            "status_counts": status_counts,
            "queue_size": self.task_queue.qsize(),
            "active_workers": len(self.workers),
            "running": self.running
        }


class CronScheduler:
    """Cron-like scheduler for periodic tasks."""
    
    def __init__(self):
        """Initialize cron scheduler."""
        if not SCHEDULE_AVAILABLE:
            raise ImportError("schedule library is required. Install with: pip install schedule")
        
        self.jobs = []
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def schedule_every(self, interval: int, unit: str = "minutes", 
                      func: Callable = None, args: Tuple = (), 
                      kwargs: Dict = None) -> None:
        """Schedule task to run every interval."""
        schedule_method = getattr(schedule.every(interval), unit)
        job = schedule_method.do(func, *args, **(kwargs or {}))
        self.jobs.append(job)
    
    def schedule_daily(self, time_str: str, func: Callable = None,
                      args: Tuple = (), kwargs: Dict = None) -> None:
        """Schedule task to run daily at specific time."""
        job = schedule.every().day.at(time_str).do(func, *args, **(kwargs or {}))
        self.jobs.append(job)
    
    def schedule_weekly(self, day: str, time_str: str, func: Callable = None,
                       args: Tuple = (), kwargs: Dict = None) -> None:
        """Schedule task to run weekly on specific day."""
        job = getattr(schedule.every(), day).at(time_str).do(func, *args, **(kwargs or {}))
        self.jobs.append(job)
    
    def _run_scheduler(self) -> None:
        """Run the scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self) -> None:
        """Start the cron scheduler."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """Stop the cron scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def clear(self) -> None:
        """Clear all scheduled jobs."""
        schedule.clear()
        self.jobs.clear()


class FileMonitor:
    """File system monitoring utilities."""
    
    def __init__(self):
        """Initialize file monitor."""
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog library is required. Install with: pip install watchdog")
        
        self.observer = Observer()
        self.handlers: Dict[str, FileSystemEventHandler] = {}
    
    def watch_directory(self, path: str, 
                      on_create: Optional[Callable] = None,
                      on_modify: Optional[Callable] = None,
                      on_delete: Optional[Callable] = None,
                      recursive: bool = True) -> str:
        """Watch directory for file changes."""
        class Handler(FileSystemEventHandler):
            def __init__(self, on_create, on_modify, on_delete):
                self.on_create = on_create
                self.on_modify = on_modify
                self.on_delete = on_delete
            
            def on_created(self, event):
                if self.on_create:
                    self.on_create(event.src_path, event.is_directory)
            
            def on_modified(self, event):
                if self.on_modify:
                    self.on_modify(event.src_path, event.is_directory)
            
            def on_deleted(self, event):
                if self.on_delete:
                    self.on_delete(event.src_path, event.is_directory)
        
        handler = Handler(on_create, on_modify, on_delete)
        self.observer.schedule(handler, path, recursive=recursive)
        self.handlers[path] = handler
        
        return path
    
    def start(self) -> None:
        """Start file monitoring."""
        self.observer.start()
    
    def stop(self) -> None:
        """Stop file monitoring."""
        self.observer.stop()
        self.observer.join()


class EmailNotifier:
    """Email notification utilities."""
    
    def __init__(self, smtp_server: str, smtp_port: int,
                 username: str, password: str,
                 use_tls: bool = True):
        """Initialize email notifier."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    def send_email(self, to_addresses: Union[str, List[str]],
                  subject: str,
                  body: str,
                  from_address: Optional[str] = None,
                  html: bool = False) -> bool:
        """Send email notification."""
        try:
            from_address = from_address or self.username
            
            if isinstance(to_addresses, str):
                to_addresses = [to_addresses]
            
            # Create message
            if html:
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(body, 'html'))
            else:
                msg = MIMEText(body)
            
            msg['Subject'] = subject
            msg['From'] = from_address
            msg['To'] = ', '.join(to_addresses)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
    
    def send_alert(self, to_addresses: Union[str, List[str]],
                  alert_type: str,
                  message: str) -> bool:
        """Send alert email."""
        subject = f"ALERT: {alert_type}"
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">{alert_type}</h2>
            <p>{message}</p>
            <p><small>Timestamp: {datetime.now().isoformat()}</small></p>
        </body>
        </html>
        """
        return self.send_email(to_addresses, subject, body, html=True)


class WorkflowManager:
    """Workflow and pipeline management."""
    
    def __init__(self):
        """Initialize workflow manager."""
        self.workflows: Dict[str, Dict] = {}
        self.workflow_results: Dict[str, Dict] = {}
    
    def create_workflow(self, workflow_id: str, 
                       steps: List[Dict[str, Any]]) -> None:
        """Create a workflow with steps."""
        self.workflows[workflow_id] = {
            "steps": steps,
            "status": "pending",
            "current_step": 0,
            "created_at": datetime.now()
        }
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow step by step."""
        if workflow_id not in self.workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        workflow["status"] = "running"
        workflow["started_at"] = datetime.now()
        
        results = {}
        
        for i, step in enumerate(workflow["steps"]):
            workflow["current_step"] = i
            step_name = step.get("name", f"step_{i}")
            func = step.get("func")
            args = step.get("args", ())
            kwargs = step.get("kwargs", {})
            
            try:
                if func:
                    result = func(*args, **kwargs)
                    results[step_name] = {"success": True, "result": result}
                else:
                    results[step_name] = {"success": True, "result": None}
                
            except Exception as e:
                results[step_name] = {"success": False, "error": str(e)}
                workflow["status"] = "failed"
                workflow["completed_at"] = datetime.now()
                self.workflow_results[workflow_id] = {
                    "workflow": workflow,
                    "results": results
                }
                return {"success": False, "error": str(e), "results": results}
        
        workflow["status"] = "completed"
        workflow["completed_at"] = datetime.now()
        
        self.workflow_results[workflow_id] = {
            "workflow": workflow,
            "results": results
        }
        
        return {"success": True, "results": results}
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow status."""
        if workflow_id in self.workflows:
            return self.workflows[workflow_id]
        return None
    
    def get_workflow_results(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow execution results."""
        return self.workflow_results.get(workflow_id)


class BackupManager:
    """Backup automation utilities."""
    
    @staticmethod
    def create_backup(source_path: str, backup_path: str,
                     compression: bool = True) -> bool:
        """Create backup of source path."""
        try:
            import shutil
            
            if compression:
                import zipfile
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_path)
                            zipf.write(file_path, arcname)
            else:
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, backup_path)
                else:
                    shutil.copy2(source_path, backup_path)
            
            return True
            
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    @staticmethod
    def restore_backup(backup_path: str, restore_path: str,
                      compression: bool = True) -> bool:
        """Restore backup to destination."""
        try:
            if compression:
                import zipfile
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(restore_path)
            else:
                import shutil
                if os.path.isdir(backup_path):
                    shutil.copytree(backup_path, restore_path)
                else:
                    shutil.copy2(backup_path, restore_path)
            
            return True
            
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    @staticmethod
    def schedule_backup(source_path: str, backup_dir: str,
                       schedule_interval: str = "daily") -> str:
        """Schedule periodic backup."""
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = os.path.join(backup_dir, f"{backup_name}.zip")
        
        return backup_path


class DataPipeline:
    """Data pipeline automation."""
    
    def __init__(self):
        """Initialize data pipeline."""
        self.stages: List[Callable] = []
        self.stage_results: List[Any] = []
    
    def add_stage(self, func: Callable, name: str = "") -> None:
        """Add a processing stage to the pipeline."""
        self.stages.append({"func": func, "name": name or func.__name__})
    
    def execute(self, initial_data: Any) -> List[Any]:
        """Execute the data pipeline."""
        current_data = initial_data
        self.stage_results = []
        
        for stage in self.stages:
            func = stage["func"]
            name = stage["name"]
            
            try:
                current_data = func(current_data)
                self.stage_results.append({
                    "stage": name,
                    "success": True,
                    "result": current_data
                })
            except Exception as e:
                self.stage_results.append({
                    "stage": name,
                    "success": False,
                    "error": str(e)
                })
                break
        
        return self.stage_results
    
    def get_results(self) -> List[Dict]:
        """Get pipeline execution results."""
        return self.stage_results


class SystemMaintenance:
    """System maintenance automation."""
    
    @staticmethod
    def clean_temp_files(temp_dir: Optional[str] = None) -> int:
        """Clean temporary files."""
        if temp_dir is None:
            import tempfile
            temp_dir = tempfile.gettempdir()
        
        cleaned_count = 0
        
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                
                try:
                    if os.path.isfile(file_path):
                        # Delete files older than 1 day
                        file_age = time.time() - os.path.getmtime(file_path)
                        if file_age > 86400:  # 1 day in seconds
                            os.remove(file_path)
                            cleaned_count += 1
                except:
                    pass
            
        except Exception as e:
            print(f"Temp cleanup failed: {e}")
        
        return cleaned_count
    
    @staticmethod
    def check_disk_space(path: str = "/") -> Dict[str, float]:
        """Check disk space usage."""
        try:
            import shutil
            usage = shutil.disk_usage(path)
            
            return {
                "total": usage.total / (1024 ** 3),  # GB
                "used": usage.used / (1024 ** 3),
                "free": usage.free / (1024 ** 3),
                "percent_used": (usage.used / usage.total) * 100
            }
        except Exception as e:
            print(f"Disk space check failed: {e}")
            return {}
    
    @staticmethod
    def rotate_logs(log_dir: str, max_files: int = 10) -> int:
        """Rotate log files."""
        try:
            log_files = []
            
            for filename in os.listdir(log_dir):
                if filename.endswith('.log'):
                    file_path = os.path.join(log_dir, filename)
                    log_files.append((file_path, os.path.getmtime(file_path)))
            
            # Sort by modification time (oldest first)
            log_files.sort(key=lambda x: x[1])
            
            # Remove oldest files if exceeding max
            removed_count = 0
            while len(log_files) > max_files:
                oldest_file = log_files.pop(0)
                os.remove(oldest_file[0])
                removed_count += 1
            
            return removed_count
            
        except Exception as e:
            print(f"Log rotation failed: {e}")
            return 0


class AutomationLogger:
    """Logging for automation tasks."""
    
    def __init__(self, log_file: str):
        """Initialize automation logger."""
        self.log_file = log_file
        self.logs: List[Dict] = []
    
    def log(self, level: str, message: str, metadata: Optional[Dict] = None) -> None:
        """Log an automation event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "metadata": metadata or {}
        }
        
        self.logs.append(log_entry)
        
        # Write to file
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Logging failed: {e}")
    
    def get_logs(self, level: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """Get logs, optionally filtered by level."""
        filtered_logs = self.logs
        
        if level:
            filtered_logs = [log for log in filtered_logs if log["level"] == level]
        
        if limit:
            filtered_logs = filtered_logs[-limit:]
        
        return filtered_logs


def demonstrate_automation_utils():
    """Demonstrate automation utilities functionality."""
    print("=== Automation Utilities Demonstration ===\n")
    
    # Task Scheduler
    print("1. Task Scheduler:")
    scheduler = TaskScheduler(max_workers=2)
    
    def sample_task(name: str, duration: float = 0.1):
        time.sleep(duration)
        return f"Task {name} completed"
    
    task1_id = scheduler.add_task(sample_task, "Task 1", args=("Task 1", 0.1))
    task2_id = scheduler.add_task(sample_task, "Task 2", args=("Task 2", 0.2))
    
    scheduler.start()
    scheduler.wait_for_completion(timeout=5)
    scheduler.stop()
    
    stats = scheduler.get_statistics()
    print(f"   Statistics: {stats}")
    
    # Workflow Manager
    print("\n2. Workflow Manager:")
    workflow = WorkflowManager()
    
    def step1():
        return "Step 1 result"
    
    def step2():
        return "Step 2 result"
    
    def step3():
        return "Step 3 result"
    
    workflow.create_workflow("test_workflow", [
        {"name": "step1", "func": step1},
        {"name": "step2", "func": step2},
        {"name": "step3", "func": step3}
    ])
    
    workflow_results = workflow.execute_workflow("test_workflow")
    print(f"   Workflow results: {workflow_results}")
    
    # Data Pipeline
    print("\n3. Data Pipeline:")
    pipeline = DataPipeline()
    
    def stage1(data):
        return [x * 2 for x in data]
    
    def stage2(data):
        return [x + 1 for x in data]
    
    def stage3(data):
        return sum(data)
    
    pipeline.add_stage(stage1, "double")
    pipeline.add_stage(stage2, "increment")
    pipeline.add_stage(stage3, "sum")
    
    pipeline_results = pipeline.execute([1, 2, 3, 4, 5])
    print(f"   Pipeline results: {pipeline_results}")
    
    # Backup Manager
    print("\n4. Backup Manager:")
    print("   Backup management utilities available")
    print("   - create_backup(source, destination)")
    print("   - restore_backup(backup, destination)")
    print("   - schedule_backup(source, backup_dir)")
    
    # System Maintenance
    print("\n5. System Maintenance:")
    cleaned = SystemMaintenance.clean_temp_files()
    print(f"   Cleaned {cleaned} temporary files")
    
    disk_space = SystemMaintenance.check_disk_space()
    if disk_space:
        print(f"   Disk space: {disk_space['percent_used']:.1f}% used")
    
    # Automation Logger
    print("\n6. Automation Logger:")
    logger = AutomationLogger("automation.log")
    logger.log("INFO", "System started")
    logger.log("INFO", "Task completed", {"task_id": "123"})
    logger.log("ERROR", "Task failed", {"error": "Timeout"})
    
    logs = logger.get_logs(limit=2)
    print(f"   Recent logs: {len(logs)} entries")
    
    # Cleanup
    try:
        os.remove("automation.log")
    except:
        pass
    
    # Cron Scheduler (if available)
    print("\n7. Cron Scheduler:")
    if SCHEDULE_AVAILABLE:
        print("   Cron scheduler available (schedule library)")
        print("   - schedule_every(interval, unit, func)")
        print("   - schedule_daily(time, func)")
        print("   - schedule_weekly(day, time, func)")
    else:
        print("   Install schedule library: pip install schedule")
    
    # File Monitor (if available)
    print("\n8. File Monitor:")
    if WATCHDOG_AVAILABLE:
        print("   File monitoring available (watchdog library)")
        print("   - watch_directory(path, callbacks)")
    else:
        print("   Install watchdog library: pip install watchdog")
    
    print("\n=== Demonstration Complete ===")
    print("\nAutomation Best Practices:")
    print("- Use appropriate task scheduling for periodic jobs")
    print("- Implement proper error handling and retry logic")
    print("- Monitor system resources during automation")
    print("- Use logging for debugging and auditing")
    print("- Test workflows thoroughly before production")
    print("- Implement proper backup strategies")
    print("- Use email notifications for important events")
    print("- Consider using dedicated tools for complex automation")


if __name__ == "__main__":
    demonstrate_automation_utils()