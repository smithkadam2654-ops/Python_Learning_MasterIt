def main():
    # Traditional way to create a list of squares
    squares_loop = []
    for i in range(1, 11):
        squares_loop.append(i * i)
    print(f"Squares using loop: {squares_loop}")

    # Using list comprehension
    squares_comp = [i * i for i in range(1, 11)]
    print(f"Squares using comprehension: {squares_comp}")

    # List comprehension with a condition (even squares)
    even_squares = [i * i for i in range(1, 11) if i % 2 == 0]
    print(f"Even squares only: {even_squares}")

if __name__ == "__main__":
    main()
