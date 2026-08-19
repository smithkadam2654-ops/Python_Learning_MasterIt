def check_even_odd(number):
    """Returns a string stating if the number is even or odd."""
    if number % 2 == 0:
        return f"{number} is Even."
    else:
        return f"{number} is Odd."

def main():
    print("Checking numbers from 1 to 5:")
    for i in range(1, 6):
        print(check_even_odd(i))

if __name__ == "__main__":
    main()
