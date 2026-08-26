import datetime

def main():
    # Get the current date and time
    now = datetime.datetime.now()
    print(f"Current Date and Time: {now}")

    # Get just the current date
    today = datetime.date.today()
    print(f"Today's Date: {today}")

    # Formatting a date using strftime
    formatted_date = now.strftime("%A, %B %d, %Y - %H:%M:%S")
    print(f"Formatted Date: {formatted_date}")

    # Calculating future or past dates using timedelta
    next_week = now + datetime.timedelta(days=7)
    print(f"Date next week: {next_week.date()}")

if __name__ == "__main__":
    main()
