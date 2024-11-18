import numpy as np
import os
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROWS = 6
COLS = 7

# Global variable to count operations during the computer's turn
operations_count = 0

# Helper functions
def create_board():
    """Creates an empty Connect4 board."""
    return np.zeros((ROWS, COLS), dtype=int)

def is_valid_move(board, col):
    """Checks if a move is valid in the given column."""
    return 0 <= col < COLS and board[0, col] == 0

def get_next_open_row(board, col):
    """Gets the next open row for a given column."""
    for row in range(ROWS-1, -1, -1):
        if board[row, col] == 0:
            return row

def drop_piece(board, row, col, piece):
    """Drops a piece into the board."""
    board[row, col] = piece

def is_winning_move(board, piece):
    """Checks if the given piece has a winning move."""
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
        score += 100  # Winning
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10  # Strong threat
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5   # Potential threat

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 15  # Block opponent's strong threat

    return score

def score_position(board, piece):
    """Scores the entire board for a given piece."""
    score = 0
    center_array = [board[row, COLS // 2] for row in range(ROWS)]
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
    """Returns a list of valid columns."""
    return [col for col in range(COLS) if is_valid_move(board, col)]

def is_terminal_node(board):
    """Checks if the game has ended."""
    return is_winning_move(board, 1) or is_winning_move(board, 2) or len(get_valid_moves(board)) == 0

def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player):
    global operations_count
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        operations_count += 1  # Increment for terminal evaluations
        if is_terminal:
            if is_winning_move(board, 1):
                return None, 100000
            elif is_winning_move(board, 2):
                return None, -100000
            else:
                return None, 0
        else:
            return None, score_position(board, 1)

    if maximizing_player:
        value = -float('inf')
        best_col = np.random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            operations_count += 1  # Increment for each branch evaluation
            new_score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = float('inf')
        best_col = np.random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            operations_count += 1  # Increment for each branch evaluation
            new_score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def get_best_move(board, depth=4):
    """Gets the best move for Player 1 using Alpha-Beta Pruning."""
    global operations_count
    operations_count = 0  # Reset operations count
    col, _ = alpha_beta_pruning(board, depth, -float('inf'), float('inf'), True)
    return col

def clear_screen():
    """Clears the terminal/console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_connect4_interactive(board, handle_click):
    """
    Displays the Connect4 game board using Matplotlib in interactive mode with mouse click handling.
    Allows players to click on a column to make a move.
    """
    rows, cols = board.shape

    fig, ax = plt.subplots(figsize=(cols, rows))

    def draw_board():
        ax.clear()
        for row in range(rows):
            for col in range(cols):
                # Draw grid
                rect = patches.Rectangle((col, rows - row - 1), 1, 1, edgecolor='black', facecolor='blue')
                ax.add_patch(rect)
                
                # Draw pieces
                piece_color = 'white'
                if board[row, col] == 1:
                    piece_color = 'red'
                elif board[row, col] == 2:
                    piece_color = 'yellow'
                circle = patches.Circle((col + 0.5, rows - row - 0.5), 0.4, color=piece_color)
                ax.add_patch(circle)
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.draw()

    def on_click(event):
        global selected_column
        # Detect the column based on the x-coordinate of the click
        if event.inaxes == ax:
            col = int(event.xdata)
            if 0 <= col < cols:
                selected_column = col  # Update the global selected column

    fig.canvas.mpl_connect('button_press_event', on_click)  # Attach the click event
    draw_board()
    return fig, ax, draw_board


def play_game():
    global selected_column
    board = create_board()
    game_over = False

    # Initialize the interactive display
    fig, ax, draw_board = display_connect4_interactive(board, None)

    while not game_over:
        draw_board()  # Redraw the board

        # Player 2 (Human) turn
        print("Player 2 (Human), click on a column to make your move.")
        selected_column = None
        while selected_column is None:
            plt.pause(0.1)  # Wait for the player to click on a column
        col = selected_column

        if not is_valid_move(board, col):
            print("Invalid move. Try again.")
            continue

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 2)

        if is_winning_move(board, 2):
            draw_board()  # Update the display
            print("Player 2 (Human) wins!")
            game_over = True
            continue

        # Player 1 (Computer) turn
        print("Player 1 (Computer) is thinking...")
        start_time = time.time()
        col = get_best_move(board, depth=3)
        computation_time = time.time() - start_time

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 1)

        if is_winning_move(board, 1):
            draw_board()  # Update the display
            print("Player 1 (Computer) wins!")
            game_over = True
            continue

        # Check for draw
        if len(get_valid_moves(board)) == 0:
            draw_board()  # Update the display
            print("It's a draw!")
            game_over = True

    plt.ioff()  # Turn off interactive mode
    plt.show()  # Keep the final board displayed

if __name__ == "__main__":
    play_game()