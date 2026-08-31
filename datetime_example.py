from datetime import datetime, timedelta

def date_math_and_formatting():
    # 1. Get the current date and time
    now = datetime.now()
    print(f"Current Date and Time: {now}")
    
    # 2. Format a date into a readable string
    # %B = Full month name, %d = Day of month, %Y = Year, %I:%M %p = 12-hour time AM/PM
    formatted_now = now.strftime("%B %d, %Y at %I:%M %p")
    print(f"Formatted: {formatted_now}")
    
    # 3. Parse a string back into a datetime object
    date_string = "2024-12-25 08:30:00"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print(f"\nParsed Date Object: {parsed_date}")
    
    # 4. Perform date math (calculating future or past dates)
    # timedelta represents a duration
    one_week_later = now + timedelta(days=7)
    two_hours_ago = now - timedelta(hours=2)
    
    print("\nDate Math:")
    print(f"One week from now: {one_week_later.strftime('%Y-%m-%d')}")
    print(f"Two hours ago: {two_hours_ago.strftime('%H:%M:%S')}")
    
    # 5. Calculate the difference between two dates
    time_difference = parsed_date - now
    print(f"\nTime difference to our parsed date (Dec 25, 2024):")
    print(f"{time_difference.days} days, {time_difference.seconds // 3600} hours")

if __name__ == "__main__":
    date_math_and_formatting()
