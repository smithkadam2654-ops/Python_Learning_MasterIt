def main():
    # Regular function
    def add(x, y):
        return x + y
    
    # Lambda function
    add_lambda = lambda x, y: x + y

    print(f"Regular function (5 + 3): {add(5, 3)}")
    print(f"Lambda function (5 + 3): {add_lambda(5, 3)}")

    # Using lambda with map()
    numbers = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Original numbers: {numbers}")
    print(f"Doubled using map & lambda: {doubled}")

if __name__ == "__main__":
    main()
