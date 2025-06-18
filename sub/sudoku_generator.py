import random
import copy

def is_valid(board, row, col, num):
    size = len(board)
    block = int(size ** 0.5)
    
    for x in range(size):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row, start_col = row - row % block, col - col % block
    for i in range(start_row, start_row + block):
        for j in range(start_col, start_col + block):
            if board[i][j] == num:
                return False

    return True

def solve(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_full_board(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    numbers = list(range(1, size + 1))
    
    for i in range(size):
        for j in range(size):
            random.shuffle(numbers)
            for num in numbers:
                if is_valid(board, i, j, num):
                    board[i][j] = num
                    if solve(copy.deepcopy(board)):
                        break
                    board[i][j] = 0
            else:
                return generate_full_board(size)
    return board

def remove_numbers(board, difficulty):
    size = len(board)
    levels = {
        "easy": size * size // 3,
        "medium": size * size // 2,
    }
    count = levels.get(difficulty, size * size // 3)
    removed = 0
    puzzle = copy.deepcopy(board)

    while removed < count:
        row, col = random.randint(0, size-1), random.randint(0, size-1)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            removed += 1
    return puzzle

def print_board(board):
    return '\n'.join(' '.join(str(num) if num != 0 else '.' for num in row) for row in board)

def generate_sudoku(size=9, difficulty="easy", count=2):
    results = []
    for _ in range(count):
        solution = generate_full_board(size)
        puzzle = remove_numbers(solution, difficulty)
        results.append((puzzle, solution))
    return results

def main():
    sizes = [6, 9]
    difficulties = ["easy", "medium"]
    count = 2  # Number of puzzles per difficulty per size

    with open("sudoku.txt", "w") as f:
        for size in sizes:
            for diff in difficulties:
                f.write(f"\n{'='*20}\nSUDOKU {size}x{size} - {diff.upper()}\n{'='*20}\n")
                puzzles = generate_sudoku(size=size, difficulty=diff, count=count)
                for idx, (puzzle, solution) in enumerate(puzzles):
                    f.write(f"\nPuzzle #{idx + 1}:\n")
                    f.write(print_board(puzzle) + '\n')
                    f.write("\nAnswer:\n")
                    f.write(print_board(solution) + '\n')

if __name__ == "__main__":
    main()
