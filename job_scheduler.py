"""
Job Scheduler - Cron-like job scheduling system.
Features: Scheduled jobs, interval-based execution, and job management.
"""

import time
import threading
from typing import Callable, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import uuid


class JobStatus(Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobType(Enum):
    """Job scheduling types."""
    ONE_TIME = "one_time"
    INTERVAL = "interval"
    CRON = "cron"


@dataclass
class Job:
    """Scheduled job."""
    id: str
    name: str
    func: Callable
    job_type: JobType
    args: tuple = ()
    kwargs: dict = None
    interval: Optional[float] = None
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    run_count: int = 0
    error_count: int = 0
    last_error: Optional[Exception] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
        if self.id is None:
            self.id = str(uuid.uuid4())


class JobScheduler:
    """Job scheduler for running tasks at scheduled times."""
    
    def __init__(self) -> None:
        """Initialize job scheduler."""
        self.jobs: Dict[str, Job] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
    
    def schedule_once(self, name: str, func: Callable, run_at: datetime,
                     args: tuple = (), kwargs: dict = None) -> str:
        """
        Schedule a one-time job.
        
        Args:
            name: Job name
            func: Function to execute
            run_at: When to run the job
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Job ID
        """
        if kwargs is None:
            kwargs = {}
        
        job = Job(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            job_type=JobType.ONE_TIME,
            args=args,
            kwargs=kwargs,
            next_run=run_at
        )
        
        with self._lock:
            self.jobs[job.id] = job
        
        return job.id
    
    def schedule_interval(self, name: str, func: Callable, interval: float,
                         args: tuple = (), kwargs: dict = None,
                         start_immediately: bool = False) -> str:
        """
        Schedule a recurring job with interval.
        
        Args:
            name: Job name
            func: Function to execute
            interval: Interval in seconds
            args: Positional arguments
            kwargs: Keyword arguments
            start_immediately: Whether to run immediately
            
        Returns:
            Job ID
        """
        if kwargs is None:
            kwargs = {}
        
        if start_immediately:
            next_run = datetime.now()
        else:
            next_run = datetime.now() + timedelta(seconds=interval)
        
        job = Job(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            job_type=JobType.INTERVAL,
            args=args,
            kwargs=kwargs,
            interval=interval,
            next_run=next_run
        )
        
        with self._lock:
            self.jobs[job.id] = job
        
        return job.id
    
    def schedule_cron(self, name: str, func: Callable, cron_expression: str,
                    args: tuple = (), kwargs: dict = None) -> str:
        """
        Schedule a job with cron expression (simplified).
        
        Args:
            name: Job name
            func: Function to execute
            cron_expression: Simplified cron (e.g., "*/5 * * * *" for every 5 minutes)
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Job ID
        """
        # Simplified cron parsing - just support "*/N * * * *" format
        if kwargs is None:
            kwargs = {}
        
        # Parse interval from cron expression
        parts = cron_expression.split()
        if parts[0].startswith("*/"):
            interval = int(parts[0][2:])
        else:
            interval = 60  # Default to 1 minute
        
        next_run = datetime.now() + timedelta(seconds=interval)
        
        job = Job(
            id=str(uuid.uuid4()),
            name=name,
            func=func,
            job_type=JobType.CRON,
            args=args,
            kwargs=kwargs,
            interval=interval,
            next_run=next_run
        )
        
        with self._lock:
            self.jobs[job.id] = job
        
        return job.id
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a scheduled job.
        
        Args:
            job_id: Job ID to cancel
            
        Returns:
            True if job was cancelled
        """
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id].status = JobStatus.CANCELLED
                del self.jobs[job_id]
                return True
        return False
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """
        Get job by ID.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job or None if not found
        """
        with self._lock:
            return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Job]:
        """Get all scheduled jobs."""
        with self._lock:
            return list(self.jobs.values())
    
    def _execute_job(self, job: Job) -> None:
        """Execute a job."""
        job.status = JobStatus.RUNNING
        
        try:
            result = job.func(*job.args, **job.kwargs)
            job.status = JobStatus.COMPLETED
            job.run_count += 1
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_count += 1
            job.last_error = e
            print(f"Job {job.name} failed: {e}")
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop."""
        while self._running:
            now = datetime.now()
            jobs_to_run = []
            
            with self._lock:
                for job_id, job in list(self.jobs.items()):
                    if job.next_run and job.next_run <= now:
                        jobs_to_run.append(job)
            
            # Execute jobs
            for job in jobs_to_run:
                self._execute_job(job)
                
                with self._lock:
                    if job.job_type == JobType.INTERVAL or job.job_type == JobType.CRON:
                        # Schedule next run
                        job.next_run = datetime.now() + timedelta(seconds=job.interval)
                    elif job.job_type == JobType.ONE_TIME:
                        # Remove one-time job
                        del self.jobs[job.id]
            
            time.sleep(0.1)  # Check every 100ms
    
    def start(self) -> None:
        """Start the scheduler."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self._thread.start()
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running


class JobStatistics:
    """Statistics for job execution."""
    
    def __init__(self) -> None:
        """Initialize statistics."""
        self.total_runs = 0
        self.total_failures = 0
        self.job_stats: Dict[str, Dict] = {}
    
    def record_run(self, job: Job, success: bool) -> None:
        """Record job execution."""
        if job.id not in self.job_stats:
            self.job_stats[job.id] = {
                "name": job.name,
                "runs": 0,
                "failures": 0
            }
        
        self.job_stats[job.id]["runs"] += 1
        self.total_runs += 1
        
        if not success:
            self.job_stats[job.id]["failures"] += 1
            self.total_failures += 1
    
    def get_summary(self) -> Dict:
        """Get statistics summary."""
        return {
            "total_runs": self.total_runs,
            "total_failures": self.total_failures,
            "success_rate": (self.total_runs - self.total_failures) / self.total_runs if self.total_runs > 0 else 0,
            "job_count": len(self.job_stats)
        }


def main() -> None:
    """Demonstrate job scheduler functionality."""
    
    print("=== Job Scheduler Demo ===")
    
    scheduler = JobScheduler()
    
    # Define some jobs
    def hello_job(name: str):
        """Simple hello job."""
        print(f"Hello, {name}!")
        time.sleep(0.1)
    
    def counter_job(count: int):
        """Counter job."""
        print(f"Count: {count}")
    
    def failing_job():
        """Job that fails."""
        raise Exception("This job always fails")
    
    # Schedule jobs
    print("Scheduling jobs...")
    
    # One-time job
    job1_id = scheduler.schedule_once(
        "Hello Job",
        hello_job,
        datetime.now() + timedelta(seconds=1),
        args=("World",)
    )
    
    # Interval job
    job2_id = scheduler.schedule_interval(
        "Counter Job",
        counter_job,
        interval=0.5,
        args=(42,),
        start_immediately=False
    )
    
    # Cron-style job (every 2 seconds)
    job3_id = scheduler.schedule_cron(
        "Cron Job",
        hello_job,
        "*/2 * * * *",
        args=("Cron",)
    )
    
    # Start scheduler
    scheduler.start()
    print("Scheduler started")
    
    # Let it run for a while
    time.sleep(5.0)
    
    # Show job status
    print("\n=== Job Status ===")
    for job in scheduler.get_all_jobs():
        print(f"Job: {job.name}")
        print(f"  Status: {job.status.value}")
        print(f"  Runs: {job.run_count}")
        print(f"  Errors: {job.error_count}")
        print(f"  Next run: {job.next_run}")
    
    # Cancel a job
    print(f"\nCancelling job {job2_id}")
    scheduler.cancel_job(job2_id)
    
    # Let it run a bit more
    time.sleep(3.0)
    
    # Stop scheduler
    scheduler.stop()
    print("\nScheduler stopped")
    
    print("\n=== Failing Job Demo ===")
    scheduler2 = JobScheduler()
    
    job4_id = scheduler2.schedule_interval(
        "Failing Job",
        failing_job,
        interval=1.0
    )
    
    scheduler2.start()
    time.sleep(3.0)
    
    failing_job = scheduler2.get_job(job4_id)
    if failing_job:
        print(f"Failing job errors: {failing_job.error_count}")
        print(f"Last error: {failing_job.last_error}")
    
    scheduler2.stop()
    
    print("\n=== Immediate Start ===")
    scheduler3 = JobScheduler()
    
    job5_id = scheduler3.schedule_interval(
        "Immediate Job",
        hello_job,
        interval=2.0,
        args=("Immediate",),
        start_immediately=True
    )
    
    scheduler3.start()
    time.sleep(3.0)
    
    immediate_job = scheduler3.get_job(job5_id)
    if immediate_job:
        print(f"Immediate job runs: {immediate_job.run_count}")
    
    scheduler3.stop()


if __name__ == "__main__":
    main()
