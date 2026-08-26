def main():
    # A regular function returns a single value and terminates
    def standard_function():
        return [1, 2, 3]

    # A generator yields one value at a time, pausing its state
    def simple_generator():
        yield 1
        yield 2
        yield 3

    print("Standard function output:", standard_function())

    # Using the generator
    gen = simple_generator()
    print("\nGenerator output one by one:")
    print(next(gen))  # Gets the first yielded value (1)
    print(next(gen))  # Gets the second yielded value (2)
    print(next(gen))  # Gets the third yielded value (3)
    # print(next(gen)) # This would raise a StopIteration error!

    print("\nUsing a generator in a loop:")
    # Generators are often used in loops to save memory on large sequences
    def countdown(num):
        while num > 0:
            yield num
            num -= 1
            
    for i in countdown(5):
        print(i)

if __name__ == "__main__":
    main()
