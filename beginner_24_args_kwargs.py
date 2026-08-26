def main():
    # *args allows you to pass a variable number of positional arguments
    def add_all(*args):
        total = 0
        for num in args:
            total += num
        return total

    print(f"Sum of 1, 2, 3: {add_all(1, 2, 3)}")
    print(f"Sum of 10, 20, 30, 40, 50: {add_all(10, 20, 30, 40, 50)}")

    # **kwargs allows you to pass a variable number of keyword arguments
    def print_user_info(**kwargs):
        for key, value in kwargs.items():
            print(f"{key.capitalize()}: {value}")

    print("\nUser Info:")
    print_user_info(name="Bob", age=25, occupation="Developer")

if __name__ == "__main__":
    main()
