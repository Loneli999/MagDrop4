import time
from modules.button_reader import read_buttons
from modules.ir_sensor_reader import read_ir_sensors
from modules.limit_switch_reader import read_limit_switches
from modules.stepper_motor import move_motor, motor_off
from modules.gantry_cart import move_gantry
from modules.electromagnet import control_electromagnet
from modules.lcd_display import display
from modules.game_ai import (
    create_board,
    print_board,
    drop_piece,
    is_valid_move,
    get_full_columns,
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
        self.ingame = False
        self.count = 0
        control_electromagnet(False)
        motor_off()
        display(" ", " ")

    def run(self):
        """
        Main loop for the FSM. Executes the method corresponding to the current state.
        """
        while True:
            if self.state == "idle":
                self.idle()
            elif self.state == "reloading":
                self.reloading()
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
        display("Red to reload", "Blue to start")
        self.board = create_board()

        # Waiting for button press
        while True:
            red_button, blue_button = read_buttons()
            if red_button:
                self.state = "reloading"
                time.sleep(0.5) # Debounce
                break
            
            if blue_button:
                self.state = "difficulty_selection"
                break

    def reloading(self):
        display("", "")

        move_gantry("mag", "reload")

        if self.count == 0:
            discs = 7
        else: 
            discs = self.count
        
        display(f"Reload {discs} Discs!", "Btn to continue!")

        while True:
            red_button, blue_button = read_buttons()
            if red_button or blue_button:
                break
            
        self.count = 0

        move_gantry("reload", "mag")

        if self.ingame:
            self.state = "human_move"
        else:
            self.state = "difficulty_selection"

    def difficulty_selection(self):
        display("Difficulty", "Selection")

        time.sleep(2)

        display("Press Red:Change", "Press Blue:Start")

        while True:
            red_button, blue_button = read_buttons()
            if red_button:
                self.level = self.level + 1
                if self.level > 4:
                    self.level = 1

                display("Selected Diff:", f"Level: {self.level}")

                time.sleep(0.5) # Debounce

            if blue_button:
                break
        
        self.state = "human_move"

    def human_move(self):
        display("Waiting for", "your move")

        self.ingame = True

        full_columns = get_full_columns(self.board)
        ignore_sensors = [col + 1 for col in full_columns]

        while True:
            self.human_col = read_ir_sensors(ignore_sensors)

            if self.human_col is not None:
                display(f"Col {self.human_col} triggered", "Ai is computing")
                if is_valid_move(self.board, self.human_col - 1):
                    row = get_next_open_row(self.board, self.human_col - 1)
                    drop_piece(self.board, row, self.human_col - 1, 2)
                break

        if is_winning_move(self.board, 2):
            self.human_won = True
            self.state = "game_end"

        self.state = "game_ai"

    def game_ai(self):
        self.ai_col = get_best_move(self.board, depth=self.level)

        if self.ai_col is not None:
            row = get_next_open_row(self.board, self.ai_col)
            drop_piece(self.board, row, self.ai_col, 1)
        
        print_board(self.board)

        if is_winning_move(self.board, 1):
            self.ai_won = True
        elif len(get_valid_moves(self.board)) == 0:
            self.draw = True
    
        self.state = "ai_move"

    def ai_move(self):
        display("It's the", "maschine's turn!")
        left_switch, right_switch = read_limit_switches()

        if not left_switch:
            move_motor("left", 5000)
            time.sleep(0.1)
        
        control_electromagnet(True)
        time.sleep(0.4)
        move_gantry("mag", f"col{self.ai_col+1}")
        time.sleep(0.1)
        control_electromagnet(False)
        time.sleep(0.2)

        self.count = self.count + 1

        if self.count >= 7:
            self.state = "reloading"
            self.count = 0
        else:
            move_gantry(f"col{self.ai_col+1}", "mag")

            if self.ai_won or self.draw:
                self.state = "game_end"
            else:
                self.state = "human_move"

    def game_end(self):
        if self.human_won:
            display("Congrats! You Won", "Press to Restart!")
        elif self.ai_won:
            display("The machine Won!", "Press to Restart!")
        elif self.draw:
            display("It's a Draw!", "Press to Restart!")

        # Waiting for button press
        while True:
            red_button, blue_button = read_buttons()
            if red_button or blue_button:
                break

        time.sleep(0.5) # Debounce
        self.board = create_board()
        self.level = 1
        self.ai_col = None
        self.human_col = None
        self.draw = False
        self.human_won = False
        self.ai_won = False
        self.ingame = False
        self.state = "idle"  # Transition

if __name__ == "__main__":
    fsm = MagDropFSM()
    fsm.run()