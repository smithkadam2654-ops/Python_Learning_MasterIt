"""
Date/Time Utilities - Comprehensive datetime operations.
Features: Parsing, formatting, arithmetic, timezone handling, and common operations.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Tuple
import re
from dateutil.parser import parse as date_parse
from dateutil.tz import UTC


class DateTimeUtils:
    """Utility class for date/time operations."""
    
    # Common date formats
    FORMATS = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]
    
    @staticmethod
    def now() -> datetime:
        """Get current datetime in UTC."""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def parse_date(date_string: str) -> Optional[datetime]:
        """
        Parse date string using multiple formats.
        
        Args:
            date_string: Date string to parse
            
        Returns:
            Parsed datetime object, or None if parsing fails
        """
        for fmt in DateTimeUtils.FORMATS:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        # Try dateutil parser as fallback
        try:
            return date_parse(date_string)
        except:
            return None
    
    @staticmethod
    def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
        """
        Format datetime to string.
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            Formatted date string
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """
        Add days to datetime.
        
        Args:
            dt: Datetime object
            days: Number of days to add (can be negative)
            
        Returns:
            New datetime with days added
        """
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """
        Add hours to datetime.
        
        Args:
            dt: Datetime object
            hours: Number of hours to add (can be negative)
            
        Returns:
            New datetime with hours added
        """
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """
        Add minutes to datetime.
        
        Args:
            dt: Datetime object
            minutes: Number of minutes to add (can be negative)
            
        Returns:
            New datetime with minutes added
        """
        return dt + timedelta(minutes=minutes)
    
    @staticmethod
    def diff_days(dt1: datetime, dt2: datetime) -> int:
        """
        Calculate difference in days between two datetimes.
        
        Args:
            dt1: First datetime
            dt2: Second datetime
            
        Returns:
            Difference in days (absolute value)
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
            Difference in hours (absolute value)
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
            Difference in minutes (absolute value)
        """
        return abs((dt2 - dt1).total_seconds() / 60)
    
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        Check if datetime falls on a weekend.
        
        Args:
            dt: Datetime to check
            
        Returns:
            True if Saturday or Sunday, False otherwise
        """
        return dt.weekday() >= 5  # 5=Saturday, 6=Sunday
    
    @staticmethod
    def is_weekday(dt: datetime) -> bool:
        """
        Check if datetime falls on a weekday.
        
        Args:
            dt: Datetime to check
            
        Returns:
            True if Monday-Friday, False otherwise
        """
        return dt.weekday() < 5
    
    @staticmethod
    def get_week_start(dt: datetime, start_day: int = 0) -> datetime:
        """
        Get start of week for given datetime.
        
        Args:
            dt: Datetime object
            start_day: Day week starts (0=Monday, 6=Sunday)
            
        Returns:
            Datetime at start of week
        """
        days_to_subtract = (dt.weekday() - start_day) % 7
        return dt - timedelta(days=days_to_subtract)
    
    @staticmethod
    def get_month_start(dt: datetime) -> datetime:
        """
        Get start of month for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of month (first day, 00:00:00)
        """
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_month_end(dt: datetime) -> datetime:
        """
        Get end of month for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of month (last day, 23:59:59)
        """
        if dt.month == 12:
            next_month = dt.replace(year=dt.year + 1, month=1, day=1)
        else:
            next_month = dt.replace(month=dt.month + 1, day=1)
        
        return next_month - timedelta(seconds=1)
    
    @staticmethod
    def get_year_start(dt: datetime) -> datetime:
        """
        Get start of year for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at start of year (Jan 1, 00:00:00)
        """
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_year_end(dt: datetime) -> datetime:
        """
        Get end of year for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Datetime at end of year (Dec 31, 23:59:59)
        """
        return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def get_age(birth_date: datetime) -> int:
        """
        Calculate age from birth date.
        
        Args:
            birth_date: Birth date
            
        Returns:
            Age in years
        """
        today = DateTimeUtils.now()
        age = today.year - birth_date.year
        
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    @staticmethod
    def get_quarter(dt: datetime) -> int:
        """
        Get quarter of year for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Quarter number (1-4)
        """
        return (dt.month - 1) // 3 + 1
    
    @staticmethod
    def get_week_number(dt: datetime) -> int:
        """
        Get ISO week number for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Week number (1-53)
        """
        return dt.isocalendar()[1]
    
    @staticmethod
    def get_day_of_year(dt: datetime) -> int:
        """
        Get day of year for given datetime.
        
        Args:
            dt: Datetime object
            
        Returns:
            Day of year (1-366)
        """
        return dt.timetuple().tm_yday
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Check if year is a leap year.
        
        Args:
            year: Year to check
            
        Returns:
            True if leap year, False otherwise
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Get number of days in a month.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Number of days in the month
        """
        if month == 2:
            return 29 if DateTimeUtils.is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31
    
    @staticmethod
    def get_business_days(start: datetime, end: datetime) -> int:
        """
        Count business days (weekdays) between two dates.
        
        Args:
            start: Start datetime
            end: End datetime
            
        Returns:
            Number of business days
        """
        days = 0
        current = start.date()
        end_date = end.date()
        
        while current <= end_date:
            if current.weekday() < 5:  # Monday-Friday
                days += 1
            current += timedelta(days=1)
        
        return days
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration in seconds to human-readable string.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
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
    def get_time_ago(dt: datetime) -> str:
        """
        Get human-readable "time ago" string.
        
        Args:
            dt: Datetime in the past
            
        Returns:
            Human-readable time ago string
        """
        now = DateTimeUtils.now()
        diff = now - dt
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"


def main() -> None:
    """Demonstrate datetime utilities."""
    
    utils = DateTimeUtils()
    
    print("=== Current Time ===")
    now = utils.now()
    print(f"Current UTC time: {now}")
    print(f"Formatted: {utils.format_date(now, '%Y-%m-%d %H:%M:%S')}")
    
    print("\n=== Date Parsing ===")
    date_strings = [
        "2024-01-15",
        "15/01/2024",
        "January 15, 2024",
        "2024-01-15T10:30:00",
    ]
    
    for date_str in date_strings:
        parsed = utils.parse_date(date_str)
        print(f"'{date_str}' -> {parsed}")
    
    print("\n=== Date Arithmetic ===")
    base_date = datetime(2024, 1, 15)
    print(f"Base date: {base_date}")
    print(f"Add 7 days: {utils.add_days(base_date, 7)}")
    print(f"Add 3 hours: {utils.add_hours(base_date, 3)}")
    print(f"Subtract 2 days: {utils.add_days(base_date, -2)}")
    
    print("\n=== Date Differences ===")
    dt1 = datetime(2024, 1, 1)
    dt2 = datetime(2024, 1, 15)
    print(f"Between {dt1} and {dt2}:")
    print(f"  Days: {utils.diff_days(dt1, dt2)}")
    print(f"  Hours: {utils.diff_hours(dt1, dt2)}")
    print(f"  Minutes: {utils.diff_minutes(dt1, dt2)}")
    
    print("\n=== Week/Weekend ===")
    test_dates = [
        datetime(2024, 1, 15),  # Monday
        datetime(2024, 1, 20),  # Saturday
        datetime(2024, 1, 21),  # Sunday
    ]
    
    for dt in test_dates:
        print(f"{dt.strftime('%Y-%m-%d (%A)')}: Weekend={utils.is_weekend(dt)}, Weekday={utils.is_weekday(dt)}")
    
    print("\n=== Period Boundaries ===")
    dt = datetime(2024, 3, 15, 14, 30, 0)
    print(f"Date: {dt}")
    print(f"Week start: {utils.get_week_start(dt)}")
    print(f"Month start: {utils.get_month_start(dt)}")
    print(f"Month end: {utils.get_month_end(dt)}")
    print(f"Year start: {utils.get_year_start(dt)}")
    print(f"Year end: {utils.get_year_end(dt)}")
    
    print("\n=== Age Calculation ===")
    birth_date = datetime(1990, 5, 15)
    age = utils.get_age(birth_date)
    print(f"Birth date: {birth_date}")
    print(f"Age: {age}")
    
    print("\n=== Date Properties ===")
    dt = datetime(2024, 3, 15)
    print(f"Date: {dt}")
    print(f"Quarter: {utils.get_quarter(dt)}")
    print(f"Week number: {utils.get_week_number(dt)}")
    print(f"Day of year: {utils.get_day_of_year(dt)}")
    
    print("\n=== Leap Year ===")
    years = [2000, 2004, 1900, 2024, 2023]
    for year in years:
        print(f"{year}: {'Leap' if utils.is_leap_year(year) else 'Not leap'}")
    
    print("\n=== Days in Month ===")
    months = [(2024, 2), (2023, 2), (2024, 4), (2024, 12)]
    for year, month in months:
        print(f"{year}-{month}: {utils.days_in_month(year, month)} days")
    
    print("\n=== Business Days ===")
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 14)
    print(f"From {start} to {end}: {utils.get_business_days(start, end)} business days")
    
    print("\n=== Duration Formatting ===")
    durations = [30, 120, 3600, 7200, 86400, 172800]
    for seconds in durations:
        print(f"{seconds}s -> {utils.format_duration(seconds)}")
    
    print("\n=== Time Ago ===")
    past_dates = [
        datetime(2024, 1, 1),
        datetime.now(timezone.utc) - timedelta(minutes=30),
        datetime.now(timezone.utc) - timedelta(hours=5),
        datetime.now(timezone.utc) - timedelta(days=3),
    ]
    
    for dt in past_dates:
        print(f"{dt}: {utils.get_time_ago(dt)}")


if __name__ == "__main__":
    main()
