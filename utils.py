import inquirer
import subprocess
import os

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    return result.stdout.strip()

def get_user_choice(items, message="Select an option", addNone=False):
    if addNone: items.append(None)
    questions = [
        inquirer.List('item',
                    message=message,
                    choices=items,
                ),
    ]
    answers = inquirer.prompt(questions)
    return answers['item'] 

def get_target_coverage(min_val=0, max_val=100):
    number = -1
    while number < min_val or number > max_val:
        try:
            number = int(input(f"Please enter a number between {min_val} and {max_val}: "))
            if number < min_val or number > max_val:
                print(f"Number out of range. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return number

def DIVIDE(title=None, character='-', length=50):
    if title:
        # Calculate the padding needed to center the title
        padding = (length - len(title) - 2) // 2
        # Construct the divider with title
        divider = f"{character * padding} {title} {character * padding}"
        # Adjust length if title length and padding cause an off-by-one issue
        if len(divider) < length:
            divider += character
    else:
        # Construct a simple divider
        divider = character * length + '\n'
    
    print(divider)