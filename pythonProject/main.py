import random
import threading

#grid print
def print_grid(grid):
    horizontal_line = "+-------+-------+-------+"
    print(horizontal_line)
    for i in range(9):
        row = "| "
        for j in range(9):
            if grid[i][j] == 0:
                row += ". "
            else:
                row += str(grid[i][j]) + " "
            if (j + 1) % 3 == 0:
                row += "| "
        print(row)
        if (i + 1) % 3 == 0:
            print(horizontal_line)


def is_valid_move(board, row, col, num):
    # Check if the number is already present in the row
    if num in board[row]:
        return False

    # Check if the number is already present in the column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number is already present in the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False


def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)

    # Remove numbers to create the puzzle
    for _ in range(40):  # Adjust difficulty by changing the number of removed numbers
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board


def check_column(board, col):
    nums = set()
    for row in range(9):
        num = board[row][col]
        if num in nums:
            return False
        if num != 0:
            nums.add(num)
    return True


def check_row(board, row):
    nums = set()
    for col in range(9):
        num = board[row][col]
        if num in nums:
            return False
        if num != 0:
            nums.add(num)
    return True


def check_subgrid(board, start_row, start_col):
    nums = set()
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            num = board[i][j]
            if num in nums:
                return False
            if num != 0:
                nums.add(num)
    return True

#Implementation of threads below
def check_board(board):
    # Check columns
    column_threads = []
    for col in range(9):
        column_thread = threading.Thread(target=check_column, args=(board, col))  # Multithreading
        column_threads.append(column_thread)
        column_thread.start()
    for thread in column_threads:
        thread.join()

    # Check rows
    row_threads = []
    for row in range(9):
        row_thread = threading.Thread(target=check_row, args=(board, row))  # Multithreading
        row_threads.append(row_thread)
        row_thread.start()
    for thread in row_threads:
        thread.join()

    # Check subgrids
    subgrid_threads = []
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            subgrid_thread = threading.Thread(target=check_subgrid,
                                              args=(board, start_row, start_col))  # Multithreading
            subgrid_threads.append(subgrid_thread)
            subgrid_thread.start()
    for thread in subgrid_threads:
        thread.join()


def main():
    print("Welcome to Sudoku!")
    board = generate_sudoku()
    print("Here's your Sudoku puzzle:")
    print_grid(board)  # Print the clear Sudoku grid

    while True:
        row = int(input("Enter row number (1-9, 0 to quit): ")) - 1
        if row == -1:
            print("Thanks for playing!")
            break
        col = int(input("Enter column number (1-9): ")) - 1
        num = int(input("Enter the number (1-9): "))

        if is_valid_move(board, row, col, num):
            board[row][col] = num
            print("Updated Sudoku:")
            print_grid(board)  # Print the updated Sudoku grid

            if all(0 not in row for row in board):
                print("Congratulations! You solved the puzzle!")
                break
        else:
            print("Invalid move! Try again.")

    print("Checking if the puzzle is solved...")
    check_board(board)
    print("Puzzle validation completed.")


if __name__ == "__main__":
    main()
