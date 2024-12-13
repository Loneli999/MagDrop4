import time
from modules.button_reader import read_buttons
from modules.ir_sensor_reader import read_ir_sensors
from modules.limit_switch_reader import read_limit_switches
from modules.stepper_motor import move_motor
from modules.gantry_cart import move_gantry
from modules.game_ai import (
    create_board,
    drop_piece,
    is_valid_move,
    get_valid_moves,
    get_next_open_row,
    is_winning_move,
    get_best_move
)



class MagDropFSM:
    def __init__(self):
        self.state = "idle"  # Initial state
        self.board = create_board()
        self.level = 1
        self.ai_col = None
        self.human_col = None
        self.draw = False
        self.human_won = False
        self.ai_won = False

    def run(self):
        """
        Main loop for the FSM. Executes the method corresponding to the current state.
        """
        while True:
            if self.state == "idle":
                self.idle()
            elif self.state == "difficulty_selection":
                self.difficulty_selection()
            elif self.state == "human_move":
                self.human_move()
            elif self.state == "game_ai":
                self.game_ai()
            elif self.state == "ai_move":
                self.ai_move()
            elif self.state == "game_end":
                self.game_end()
            else:
                print(f"Unknown state: {self.state}")
                break

    def idle(self):
        print("Red to reload")
        print("Blue to continue")

        # Waiting for button press
        while True:
            red_button, blue_button = read_buttons()
            if red_button:
                self.state = "difficulty_selection"
                break
            
            if blue_button:
                self.state = "reloading"
                break

    def reloading(self):
        print("clear display")

        move_gantry("mag", "reload")

        print("Press any Button")
        print("to continue")

        while True:
            red_button, blue_button = read_buttons()
            if red_button or blue_button:
                break

        move_gantry("reload", "mag")

        self.state = "difficulty_selection"

    def difficulty_selection(self):
        print("Difficuly")
        print("Selection")

        time.sleep(3)

        print("Press Red: Change")
        print("Press Blue: Start")

        while True:
            red_button, blue_button = read_buttons()
            if red_button:
                self.level = self.level + 1
                if self.level > 4:
                    self.level = 1

                print("Selected Diff:")
                print(f'Level: {self.level}')


                time.sleep(0.5) # Debounce

            if blue_button:
                break
        
        self.state = "human_move"

    def human_move(self):
        print("Waiting for")
        print("your Move")

        while True:
            self.human_col = read_ir_sensors()

            if self.human_col is not None:
                print(f"IR Sensor {self.human_col} triggered")
                if is_valid_move(self.board, self.human_col - 1):
                    row = get_next_open_row(self.board, self.human_col - 1)
                    drop_piece(self.board, row, self.human_col - 1, 2)
                break

        if is_winning_move(self.board, 2):
            self.human_won = True
            self.state = "game_end"

        self.state = "game_ai"

    def game_ai(self):
        print(self.board)
        self.ai_col = get_best_move(self.board, depth=self.level)

        if self.ai_col is not None:
            row = get_next_open_row(self.board, self.ai_col)
            drop_piece(self.board, row, self.ai_col, 1)

        if is_winning_move(self.board, 1):
            self.ai_won = True
        elif len(get_valid_moves(self.board)) == 0:
            self.draw = True
    
        self.state = "ai_move"

    def ai_move(self):
        left_switch, right_switch = read_limit_switches()

        if not left_switch:
            move_motor("left", 5000)
            time.sleep(0.1)
        
        #activate electromagnet
        time.sleep(0.1)
        move_gantry("mag", f"col{self.ai_col+1}")
        time.sleep(0.1)
        #deactivate electromagnet
        time.sleep(0.2)
        move_gantry(f"col{self.ai_col+1}", "mag")

        if self.ai_won or self.draw:
            self.state = "game_end"
        else:
            self.state = "human_move"

    def game_end(self):
        if self.human_won:
            print("Congrats!")
            print("You Won!")
        elif self.ai_won:
            print("The machine")
            print("has won!")
        elif self.draw:
            print("It's a Draw!")
            print("")
        
        time.sleep(10)

        print("Button press")
        print("for restart!")

        # Waiting for button press
        while True:
            red_button, blue_button = read_buttons()
            if red_button or blue_button:
                break

        self.state = "idle"  # Transition

if __name__ == "__main__":
    fsm = MagDropFSM()
    fsm.run()