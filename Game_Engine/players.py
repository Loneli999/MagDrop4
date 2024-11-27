from game_board import GameBoard, COLS

class HumanAgent:
    def __init__(self, piece):
        self.piece = piece

    def make_move(self, game_board: GameBoard):
        valid_move = False
        while not valid_move:
            try:
                col = self.get_human_move()
                if game_board.is_valid_move(col):
                    valid_move = True
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")
        row = game_board.get_next_open_row(col)
        game_board.drop_piece(row, col, self.piece)

    def get_human_move(self):
        # replace with physical method for input
        return int(input("Player (Human), enter your move (0-6): "))

class ComputerAgent:
    def __init__(self, piece):
        self.piece = piece

    def make_move(self, game_board: GameBoard):
        col = self.get_best_move(game_board, depth=3)
        row = game_board.get_next_open_row(col)
        game_board.drop_piece(row, col, self.piece)

    def get_best_move(self, game_board: GameBoard, depth):
        # placeholder for agent logic
        for col in range(COLS):
            if game_board.is_valid_move(col):
                return col
        return 0