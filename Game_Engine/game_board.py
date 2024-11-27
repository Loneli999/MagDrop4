import numpy as np

ROWS = 6
COLS = 7

class GameBoard:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)

    def is_valid_move(self, col):
        return 0 <= col < COLS and self.board[0, col] == 0

    def get_next_open_row(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.board[row, col] == 0:
                return row
        return None

    def drop_piece(self, row, col, piece):
        self.board[row, col] = piece

    def is_winning_move(self, piece):
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.board[row, col + i] == piece for i in range(4)):
                    return True
        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLS):
                if all(self.board[row + i, col] == piece for i in range(4)):
                    return True
        # Check positively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.board[row + i, col + i] == piece for i in range(4)):
                    return True
        # Check negatively sloped diagonals
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(self.board[row - i, col + i] == piece for i in range(4)):
                    return True
        return False

    def render(self):
        print("\nCurrent Board:")
        for row in self.board:
            print('|' + '|'.join([' ' if cell == 0 else 'X' if cell == 1 else 'O' for cell in row]) + '|')
        print(' ' + ' '.join(map(str, range(COLS))))