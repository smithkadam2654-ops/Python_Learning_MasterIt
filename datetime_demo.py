from datetime import datetime, timedelta

def demonstrate_datetime():
    """Demonstrate basic datetime manipulation and formatting."""
    
    # 1. Get current date and time
    now = datetime.now()
    print(f"Current Date & Time: {now}")
    
    # 2. Formatting dates
    formatted_now = now.strftime("%A, %B %d, %Y - %I:%M %p")
    print(f"Formatted String: {formatted_now}")
    
    # 3. Parsing dates from strings
    date_string = "2023-12-25 15:30:00"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print(f"\nParsed Date Object: {parsed_date}")
    
    # 4. Time arithmetic (using timedelta)
    one_week_from_now = now + timedelta(days=7)
    two_hours_ago = now - timedelta(hours=2)
    
    print(f"\nOne week from now: {one_week_from_now.strftime('%Y-%m-%d')}")
    print(f"Two hours ago: {two_hours_ago.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    demonstrate_datetime()
