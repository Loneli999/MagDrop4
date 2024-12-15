from modules.stepper_motor import move_motor

# Define positions and step distances
POSITIONS = {
    "mag": 0,         # Leftmost position
    "col1": 1049,     # Steps from "mag" to "col1"
    "col2": 1485,     # Steps from "mag" to "col2"
    "col3": 1925,     # Steps from "mag" to "col3"
    "col4": 2370,     # Steps from "mag" to "col4"
    "col5": 2800,     # Steps from "mag" to "col5"
    "col6": 3240,     # Steps from "mag" to "col6"
    "col7": 3676,     # Steps from "mag" to "col7"
    "reload": 3800    # Steps from "mag" to "reload"
}

# Gantry movement function
def move_gantry(current_position, desired_position):
    """
    Move the gantry from the current position to the desired position.
    
    Parameters:
        current_position (str): Current position name (e.g., "mag", "col1", etc.)
        desired_position (str): Desired position name (e.g., "reload", "col3", etc.)
    """
    if current_position not in POSITIONS or desired_position not in POSITIONS:
        print("Invalid position. Use predefined positions: " + ", ".join(POSITIONS.keys()))
    
    # Calculate the step difference
    current_steps = POSITIONS[current_position]
    desired_steps = POSITIONS[desired_position]
    step_difference = desired_steps - current_steps

    # Determine direction and number of steps
    if step_difference > 0:
        direction = 'right'
        steps = step_difference
    elif step_difference < 0:
        direction = 'left'
        steps = abs(step_difference)
    else:
        print(f"Already at {desired_position}. No movement needed.")
        return
    
    # Assure it hits the limit switch when going back to magazine
    if desired_position == "mag":
        steps = steps + 5000

    # Move the gantry
    move_motor(direction, steps)
    print(f"Gantry moved to {desired_position}.")
