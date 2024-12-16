import numpy as np
from random import shuffle

ROWS = 6
COLS = 7

operations_count = 0

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def print_board(board):
    symbols = {
        0: ' ', 
        1: '○',  # AI (Black pieces)
        2: '●',  # Human (White pieces)
    }

    print("┌" + ("───┬" * 6) + "───┐")

    for i, row in enumerate(board):
        row_content = "│".join(f"{symbols[cell]:^3}" for cell in row)
        print(f"│{row_content}│")
        if i < len(board) - 1:
            print("├" + ("───┼" * 6) + "───┤")
    
    print("└" + ("───┴" * 6) + "───┘")
    print("  1   2   3   4   5   6   7")

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0, col] == 0

def get_next_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row, col] == 0:
            return row

def drop_piece(board, row, col, piece):
    board[row, col] = piece

def get_full_columns(board):
    full_columns = []
    for col in range(COLS):
        if not is_valid_move(board, col):  # If the column is not a valid move, it's full
            full_columns.append(col)
    return full_columns

def is_winning_move(board, piece):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row, col + i] == piece for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i, col] == piece for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i, col + i] == piece for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i, col + i] == piece for i in range(4)):
                return True
    return False

def evaluate_window(window, piece):
    """Scores a window of 4 cells."""
    opponent_piece = 1 if piece == 2 else 2
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5

    if window.count(opponent_piece) == 4:
        score -= 100
    elif window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 8

    return score

def score_position(board, piece):
    """Scores the entire board for a given piece."""
    score = 0
    center_array = [int(i) for i in list(board[:,COLS//2])]
    score += center_array.count(piece) * 6  # Encourage central play

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board[row, col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = [board[row + i, col] for i in range(4)]
            score += evaluate_window(window, piece)

    # Positive Diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i, col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Negative Diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i, col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def is_terminal_node(board):
    return is_winning_move(board, 1) or is_winning_move(board, 2) or len(get_valid_moves(board)) == 0

def MiniMaxAlphaBeta(board, depth):
    global operations_count
    operations_count = 0  # Reset the operations count each time this is called
    
    valid_moves = get_valid_moves(board)
    # If no valid moves are available, just return None
    if len(valid_moves) == 0:
        return None
    
    # Shuffle the valid moves for variety
    shuffle(valid_moves)

    alpha = -float('inf')
    beta = float('inf')
    best_col = valid_moves[0]
    best_score = -float('inf')

    # Explore all valid columns to find the best (max) score
    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 1)  # piece=1 for AI
        operations_count += 1

        score = minimizeBeta(temp_board, depth - 1, alpha, beta)
        if score > best_score:
            best_score = score
            best_col = col
        alpha = max(alpha, best_score)
        
        # Early pruning
        if alpha >= beta:
            break

    return best_col


def minimizeBeta(board, depth, alpha, beta):
    global operations_count
    
    # Terminal or depth limit check
    if depth == 0 or is_terminal_node(board):
        operations_count += 1
        if is_terminal_node(board):
            # Winning/losing/draw scoring
            if is_winning_move(board, 1):
                return 100000 + depth * 1000
            elif is_winning_move(board, 2):
                return -100000 - depth * 1000
            else:
                return 0
        else:
            return score_position(board, 1)  # Evaluate from AI's perspective

    value = float('inf')
    valid_moves = get_valid_moves(board)

    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 2)  # piece=2 for Human
        operations_count += 1

        new_score = maximizeAlpha(temp_board, depth - 1, alpha, beta)
        value = min(value, new_score)
        beta = min(beta, value)

        # Early pruning
        if alpha >= beta:
            break

    return value


def maximizeAlpha(board, depth, alpha, beta):
    global operations_count

    # Terminal or depth limit check
    if depth == 0 or is_terminal_node(board):
        operations_count += 1
        if is_terminal_node(board):
            # Winning/losing/draw scoring
            if is_winning_move(board, 1):
                return 100000 + depth * 1000
            elif is_winning_move(board, 2):
                return -100000 - depth * 1000
            else:
                return 0
        else:
            return score_position(board, 1)

    value = -float('inf')
    valid_moves = get_valid_moves(board)

    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 1)  # piece=1 for AI
        operations_count += 1

        new_score = minimizeBeta(temp_board, depth - 1, alpha, beta)
        value = max(value, new_score)
        alpha = max(alpha, value)

        # Early pruning
        if alpha >= beta:
            break

    return value


def get_best_move(board, depth=4):
    global operations_count
    operations_count = 0
    best_col = MiniMaxAlphaBeta(board, depth)
    return best_col