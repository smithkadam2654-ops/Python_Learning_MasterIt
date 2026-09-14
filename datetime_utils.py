"""
DateTime Utilities - Date and time manipulation utilities.
Features: Date parsing, formatting, arithmetic, timezone handling, and common operations.
"""

from typing import Optional, List
from datetime import datetime, timedelta, timezone
import time


class DateTimeUtils:
    """Date and time utility functions."""
    
    @staticmethod
    def now() -> datetime:
        """
        Get current datetime.
        
        Returns:
            Current datetime
        """
        return datetime.now()
    
    @staticmethod
    def utc_now() -> datetime:
        """
        Get current UTC datetime.
        
        Returns:
            Current UTC datetime
        """
        return datetime.now(timezone.utc)
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime to string.
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            Formatted string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
        """
        Parse string to datetime.
        
        Args:
            date_str: Date string
            format_str: Format string
            
        Returns:
            Datetime object or None if invalid
        """
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError:
            return None
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """
        Add days to datetime.
        
        Args:
            dt: Datetime object
            days: Number of days to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """
        Add hours to datetime.
        
        Args:
            dt: Datetime object
            hours: Number of hours to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """
        Add minutes to datetime.
        
        Args:
            dt: Datetime object
            minutes: Number of minutes to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(minutes=minutes)
    
    @staticmethod
    def add_seconds(dt: datetime, seconds: int) -> datetime:
        """
        Add seconds to datetime.
        
        Args:
            dt: Datetime object
            seconds: Number of seconds to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(seconds=seconds)
    
    @staticmethod
    def diff_days(dt1: datetime, dt2: datetime) -> int:
        """
        Calculate difference in days between two datetimes.
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            Difference in days
        """
        return abs((dt2 - dt1).days)
    
    @staticmethod
    def diff_hours(dt1: datetime, dt2: datetime) -> float:
        """
        Calculate difference in hours between two datetimes.
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            Difference in hours
        """
        return abs((dt2 - dt1).total_seconds() / 3600)
    
    @staticmethod
    def diff_minutes(dt1: datetime, dt2: datetime) -> float:
        """
        Calculate difference in minutes between two datetimes.
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            Difference in minutes
        """
        return abs((dt2 - dt1).total_seconds() / 60)
    
    @staticmethod
    def diff_seconds(dt1: datetime, dt2: datetime) -> float:
        """
        Calculate difference in seconds between two datetimes.
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            Difference in seconds
        """
        return abs((dt2 - dt1).total_seconds())
    
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        Check if datetime is on weekend.
        
        Args:
            dt: Datetime object
            
        Returns:
            True if weekend
        """
        return dt.weekday() >= 5  # 5=Saturday, 6=Sunday
    
    @staticmethod
    def is_weekday(dt: datetime) -> bool:
        """
        Check if datetime is on weekday.
        
        Args:
            dt: Datetime object
            
        Returns:
            True if weekday
        """
        return dt.weekday() < 5
    
    @staticmethod
    def start_of_day(dt: datetime) -> datetime:
        """
        Get start of day (midnight).
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of day
        """
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_day(dt: datetime) -> datetime:
        """
        Get end of day (23:59:59.999999).
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of day
        """
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def start_of_week(dt: datetime) -> datetime:
        """
        Get start of week (Monday).
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of week
        """
        return dt - timedelta(days=dt.weekday())
    
    @staticmethod
    def end_of_week(dt: datetime) -> datetime:
        """
        Get end of week (Sunday).
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of week
        """
        return dt + timedelta(days=6 - dt.weekday())
    
    @staticmethod
    def start_of_month(dt: datetime) -> datetime:
        """
        Get start of month.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of month
        """
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_month(dt: datetime) -> datetime:
        """
        Get end of month.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of month
        """
        if dt.month == 12:
            next_month = dt.replace(year=dt.year + 1, month=1, day=1)
        else:
            next_month = dt.replace(month=dt.month + 1, day=1)
        
        return next_month - timedelta(microseconds=1)
    
    @staticmethod
    def start_of_year(dt: datetime) -> datetime:
        """
        Get start of year.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of year
        """
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_year(dt: datetime) -> datetime:
        """
        Get end of year.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of year
        """
        return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def age(birth_date: datetime) -> int:
        """
        Calculate age from birth date.
        
        Args:
            birth_date: Birth date
            
        Returns:
            Age in years
        """
        today = datetime.now()
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Get number of days in month.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Number of days
        """
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        
        return (next_month - datetime(year, month, 1)).days
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Check if year is leap year.
        
        Args:
            year: Year
            
        Returns:
            True if leap year
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    @staticmethod
    def quarter(dt: datetime) -> int:
        """
        Get quarter of year.
        
        Args:
            dt: Datetime object
            
        Returns:
            Quarter (1-4)
        """
        return (dt.month - 1) // 3 + 1
    
    @staticmethod
    def week_of_year(dt: datetime) -> int:
        """
        Get week number of year.
        
        Args:
            dt: Datetime object
            
        Returns:
            Week number (1-53)
        """
        return dt.isocalendar()[1]
    
    @staticmethod
    def date_range(start: datetime, end: datetime, 
                   days: int = 1) -> List[datetime]:
        """
        Generate list of dates in range.
        
        Args:
            start: Start datetime
            end: End datetime
            days: Step in days
            
        Returns:
            List of datetimes
        """
        dates = []
        current = start
        
        while current <= end:
            dates.append(current)
            current += timedelta(days=days)
        
        return dates
    
    @staticmethod
    def business_days(start: datetime, end: datetime) -> int:
        """
        Count business days between two dates.
        
        Args:
            start: Start datetime
            end: End datetime
            
        Returns:
            Number of business days
        """
        count = 0
        current = start
        
        while current <= end:
            if DateTimeUtils.is_weekday(current):
                count += 1
            current += timedelta(days=1)
        
        return count
    
    @staticmethod
    def to_timestamp(dt: datetime) -> float:
        """
        Convert datetime to Unix timestamp.
        
        Args:
            dt: Datetime object
            
        Returns:
            Unix timestamp
        """
        return dt.timestamp()
    
    @staticmethod
    def from_timestamp(timestamp: float) -> datetime:
        """
        Convert Unix timestamp to datetime.
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            Datetime object
        """
        return datetime.fromtimestamp(timestamp)
    
    @staticmethod
    def sleep(seconds: float) -> None:
        """
        Sleep for specified seconds.
        
        Args:
            seconds: Seconds to sleep
        """
        time.sleep(seconds)
    
    @staticmethod
    def measure_time(func) -> float:
        """
        Measure execution time of function.
        
        Args:
            func: Function to measure
            
        Returns:
            Execution time in seconds
        """
        start = time.time()
        func()
        end = time.time()
        return end - start


class TimezoneUtils:
    """Timezone utility functions."""
    
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        """
        Convert datetime to UTC.
        
        Args:
            dt: Datetime object
            
        Returns:
            UTC datetime
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def from_utc(dt: datetime, tz: timezone) -> datetime:
        """
        Convert UTC datetime to specified timezone.
        
        Args:
            dt: UTC datetime
            tz: Target timezone
            
        Returns:
            Datetime in target timezone
        """
        return dt.astimezone(tz)


class DurationFormatter:
    """Duration formatting utilities."""
    
    @staticmethod
    def format_seconds(seconds: float) -> str:
        """
        Format seconds as human-readable duration.
        
        Args:
            seconds: Seconds to format
            
        Returns:
            Formatted string
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f}h"
        else:
            days = seconds / 86400
            return f"{days:.1f}d"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format seconds as HH:MM:SS.
        
        Args:
            seconds: Seconds to format
            
        Returns:
            Formatted string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def main() -> None:
    """Demonstrate datetime utilities."""
    
    print("=== DateTime Utilities Demo ===")
    
    # Current time
    print("\n--- Current Time ---")
    now = DateTimeUtils.now()
    utc_now = DateTimeUtils.utc_now()
    print(f"Local: {DateTimeUtils.format_datetime(now)}")
    print(f"UTC: {DateTimeUtils.format_datetime(utc_now)}")
    
    # Formatting and parsing
    print("\n--- Format and Parse ---")
    formatted = DateTimeUtils.format_datetime(now, "%Y-%m-%d")
    print(f"Formatted: {formatted}")
    
    parsed = DateTimeUtils.parse_datetime("2024-01-15 10:30:00")
    print(f"Parsed: {parsed}")
    
    # Date arithmetic
    print("\n--- Date Arithmetic ---")
    future = DateTimeUtils.add_days(now, 7)
    print(f"7 days from now: {DateTimeUtils.format_datetime(future)}")
    
    past = DateTimeUtils.add_hours(now, -24)
    print(f"24 hours ago: {DateTimeUtils.format_datetime(past)}")
    
    # Differences
    print("\n--- Differences ---")
    dt1 = datetime(2024, 1, 1)
    dt2 = datetime(2024, 1, 10)
    print(f"Days between {dt1.date()} and {dt2.date()}: {DateTimeUtils.diff_days(dt1, dt2)}")
    print(f"Hours: {DateTimeUtils.diff_hours(dt1, dt2):.1f}")
    
    # Date boundaries
    print("\n--- Date Boundaries ---")
    print(f"Start of day: {DateTimeUtils.format_datetime(DateTimeUtils.start_of_day(now))}")
    print(f"End of day: {DateTimeUtils.format_datetime(DateTimeUtils.end_of_day(now))}")
    print(f"Start of week: {DateTimeUtils.format_datetime(DateTimeUtils.start_of_week(now))}")
    print(f"Start of month: {DateTimeUtils.format_datetime(DateTimeUtils.start_of_month(now))}")
    
    # Checks
    print("\n--- Checks ---")
    print(f"Is weekend: {DateTimeUtils.is_weekend(now)}")
    print(f"Is weekday: {DateTimeUtils.is_weekday(now)}")
    print(f"Is leap year 2024: {DateTimeUtils.is_leap_year(2024)}")
    print(f"Days in Feb 2024: {DateTimeUtils.days_in_month(2024, 2)}")
    
    # Age calculation
    print("\n--- Age ---")
    birth = datetime(1990, 5, 15)
    print(f"Birth date: {birth.date()}")
    print(f"Age: {DateTimeUtils.age(birth)}")
    
    # Quarter and week
    print("\n--- Quarter and Week ---")
    print(f"Quarter: {DateTimeUtils.quarter(now)}")
    print(f"Week of year: {DateTimeUtils.week_of_year(now)}")
    
    # Date range
    print("\n--- Date Range ---")
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 10)
    dates = DateTimeUtils.date_range(start, end, days=2)
    print(f"Dates: {[d.date() for d in dates]}")
    
    # Business days
    print("\n--- Business Days ---")
    business_days = DateTimeUtils.business_days(start, end)
    print(f"Business days: {business_days}")
    
    # Timestamp
    print("\n--- Timestamp ---")
    timestamp = DateTimeUtils.to_timestamp(now)
    print(f"Timestamp: {timestamp}")
    print(f"From timestamp: {DateTimeUtils.from_timestamp(timestamp)}")
    
    # Duration formatting
    print("\n--- Duration Formatting ---")
    print(f"90 seconds: {DurationFormatter.format_seconds(90)}")
    print(f"3600 seconds: {DurationFormatter.format_seconds(3600)}")
    print(f"86400 seconds: {DurationFormatter.format_seconds(86400)}")
    print(f"3661 seconds: {DurationFormatter.format_duration(3661)}")


if __name__ == "__main__":
    main()
