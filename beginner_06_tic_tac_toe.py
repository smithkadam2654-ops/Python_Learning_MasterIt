def print_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def main():
    board = [" " for _ in range(9)]
    current_player = "X"
    
    print("Welcome to Tic-Tac-Toe!")
    print("Positions are 1-9, from top-left to bottom-right.")

    for turn in range(9):
        print_board(board)
        
        while True:
            try:
                move = int(input(f"Player {current_player}, enter your move (1-9): ")) - 1
                if 0 <= move <= 8 and board[move] == " ":
                    board[move] = current_player
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            return
            
        current_player = "O" if current_player == "X" else "X"

    print_board(board)
    print("It's a tie!")

if __name__ == "__main__":
    main()
