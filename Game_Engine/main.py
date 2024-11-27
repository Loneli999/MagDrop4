from game_board import GameBoard
from players import HumanAgent, ComputerAgent
import os

HUMAN = 0
COMPUTER = 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_loop():
    game_board = GameBoard()
    human = HumanAgent(piece=2)
    computer = ComputerAgent(piece=1)
    game_over = False
    turn = HUMAN  # 0 for Human, 1 for Computer

    while not game_over:
        clear_screen()
        game_board.render()
        if turn == HUMAN:
            human.make_move(game_board)
            if game_board.is_winning_move(human.piece):
                clear_screen()
                game_board.render()
                print("Player (Human) wins!")
                game_over = True
        else:
            computer.make_move(game_board)
            if game_board.is_winning_move(computer.piece):
                clear_screen()
                game_board.render()
                print("Player (Computer) wins!")
                game_over = True

        # Check for draw
        if not game_over and not any(game_board.is_valid_move(col) for col in range(COLS)):
            game_board.render()
            print("It's a draw!")
            game_over = True

        turn = 1 - turn  # Switch turns

if __name__ == "__main__":
    main_loop()