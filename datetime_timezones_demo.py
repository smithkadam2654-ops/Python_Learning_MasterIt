from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    print("This script requires Python 3.9+ for the zoneinfo module.")
    exit()

def demonstrate_timezones():
    """Demonstrate handling timezones using the standard library."""
    
    # 1. Get the current time in UTC (Always store times in UTC in databases!)
    utc_now = datetime.now(ZoneInfo("UTC"))
    print(f"Current Time (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # 2. Convert UTC to different timezones
    ny_time = utc_now.astimezone(ZoneInfo("America/New_York"))
    tokyo_time = utc_now.astimezone(ZoneInfo("Asia/Tokyo"))
    london_time = utc_now.astimezone(ZoneInfo("Europe/London"))
    
    print("\n--- Time Around the World ---")
    print(f"New York: {ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"London:   {london_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Tokyo:    {tokyo_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # 3. Create an aware datetime object directly
    # e.g., A meeting scheduled for 3 PM in New York
    meeting_ny = datetime(2023, 11, 15, 15, 0, 0, tzinfo=ZoneInfo("America/New_York"))
    
    # What time is that meeting for someone in Tokyo?
    meeting_tokyo = meeting_ny.astimezone(ZoneInfo("Asia/Tokyo"))
    print("\n--- Meeting Conversion ---")
    print(f"Meeting scheduled at: {meeting_ny.strftime('%H:%M %Z')}")
    print(f"Time for Tokyo staff: {meeting_tokyo.strftime('%H:%M %Z')}")

if __name__ == "__main__":
    demonstrate_timezones()
