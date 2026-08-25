import random

def roll_dice(num_dice, num_sides):
    print(f"\nRolling {num_dice}d{num_sides}...")
    results = [random.randint(1, num_sides) for _ in range(num_dice)]
    total = sum(results)
    
    print(f"Results: {results}")
    print(f"Total: {total}")
    return total

def main():
    print("Welcome to the Dice Roller!")
    
    while True:
        try:
            dice_str = input("\nEnter dice to roll (e.g., 2d6) or 'q' to quit: ").lower()
            if dice_str == 'q':
                break
                
            if 'd' not in dice_str:
                print("Invalid format. Use format like '2d6'.")
                continue
                
            num_dice_str, num_sides_str = dice_str.split('d')
            num_dice = int(num_dice_str) if num_dice_str else 1
            num_sides = int(num_sides_str)
            
            if num_dice <= 0 or num_sides <= 0:
                print("Numbers must be greater than 0.")
                continue
                
            roll_dice(num_dice, num_sides)
            
        except ValueError:
            print("Invalid format. Use format like '2d6'.")

if __name__ == "__main__":
    main()
