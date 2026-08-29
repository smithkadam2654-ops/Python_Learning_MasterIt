import calendar
from datetime import date

def demonstrate_calendar():
    """Demonstrate useful functions from the built-in calendar module."""
    
    print("--- 1. Basic Calendar Output ---")
    # Print the calendar for a specific month
    year = 2024
    month = 2
    print(f"Calendar for {calendar.month_name[month]} {year}:\n")
    # Print it formatted like a real calendar
    print(calendar.month(year, month))
    
    print("--- 2. Leap Years ---")
    # Check if a year is a leap year
    is_leap = calendar.isleap(year)
    print(f"Is {year} a leap year? {is_leap}")
    
    # Count leap years in a range
    leap_days_between = calendar.leapdays(2000, 2025)
    print(f"Number of leap years between 2000 and 2025: {leap_days_between}")
    
    print("\n--- 3. Weekday Calculations ---")
    # Find out what day of the week a specific date was/is
    # (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    day_index = calendar.weekday(1969, 7, 20) # Moon landing
    day_name = calendar.day_name[day_index]
    print(f"The Apollo 11 Moon Landing (July 20, 1969) was on a: {day_name}")
    
    print("\n--- 4. Month Ranges ---")
    # Get the first weekday of the month and how many days are in it
    # Returns (weekday_of_first_day, number_of_days)
    first_weekday, num_days = calendar.monthrange(2024, 2)
    print(f"February 2024 starts on a {calendar.day_name[first_weekday]} and has {num_days} days.")

if __name__ == "__main__":
    demonstrate_calendar()
