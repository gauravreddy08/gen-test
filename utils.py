import toml
import inquirer

class Prompt():
    def __init__(self, filename='prompts.toml'):
        file = open(filename, 'r')
        self.data = toml.load(file)

    def fetch(self, key: str) -> str:
        return self.data[key]

def write_file(file_path: str, content: str) -> str:
    print(file_path)
    try:
        with open(file_path, 'w+') as file:
            file.write(content)
        response = f"Changed {file_path}"
        file.close()
    except FileNotFoundError:
        response = "The file does not exist."
    except Exception as e:
        response = "An unexpected error occurred: {e}"
    
    return response

def get_user_choice(items, message="Select an option"):
        questions = [
            inquirer.List('item',
                        message=message,
                        choices=items,
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers['item'] 

def DIVIDE(title=None, character='-', length=40):
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