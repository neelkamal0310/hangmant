import time
import os
import random
from getch import getche

# Clear the terminal
os.system("clear")

# Find the number of columns in the terminal. The game centres itself
# in the given number of columns.
if os.name == 'posix':
    COLS = int(os.popen("stty size", "r").read().split()[1])
    COLOR = True
else:
    COLS = 80
    COLOR = False

# ANSI color codes
CRED = 31
CGREEN = 32
CYELLOW = 33
CBLUE = 34
CMAGENTA = 35
CCYAN = 36
CNONE = 0

# List of HANGMAN strings
HANGMAN = [
    """
_____
|
|
|
|
|
|
    """,
    """
_____
|   |
|
|
|
|
|
    """,
    """
_____
|   |
|  (x)
|   
|   
|
|
    """,
    """
_____
|   |
|  (x)
|   |
|   |
|
|
    """,
    """
_____
|   |
|  (x)
|  /|
|   |
|
|
    """,
    """
_____
|   |
|  (x)
|  /|\\
|   |
|  
|
    """,
    """
_____
|   |
|  (x)
|  /|\\
|   |
|  /
|
    """,
    """
_____
|   |
|  (x)
|  /|\\
|   |
|  / \\
|
    """,
]

HANG_COLS = [ CGREEN, CGREEN, CGREEN, CYELLOW, CYELLOW, CYELLOW, CRED, CRED ]


# Function to set colors
def set_col(col, bold=False):
    if COLOR:
        if bold:
            print(f"\033[{col};1m", end="")
        else:
            print(f"\033[{col}m", end="")
    else:
        pass


# Print the title of tha game
def show_title():
    print()
    set_col(CBLUE, bold=True)
    title_string = "HANGMAN - Guess the word"
    print(f"{title_string:^{COLS}}")
    print(f"{'-'*len(title_string):^{COLS}}")
    set_col(CNONE)
    print()


# Determine and show the correct status depending on the
# number of wrong letters aligned to center of the screen
def show_hangman(wrong_letters, COLS):
    temp = HANGMAN[wrong_letters].lstrip().split('\n')
    spaces = COLS//2 - len(temp[0])//2
    set_col(HANG_COLS[wrong_letters])
    for i in temp:
        print(' '*spaces, i, sep="")
    set_col(CNONE)


# Function to show the game over screen
def show_game_over(dashed_string, word, wrong_letters):
    os.system("clear")
    show_title()
    temp = ' '.join(dashed_string) + " ==> " + word
    set_col(CRED, bold=True)
    print(f"{temp:^{COLS}}")
    set_col(CNONE)
    show_hangman(wrong_letters, COLS)
    set_col(CRED, bold=True)
    print(f"{'YOU LOSE!!':^{COLS}}\n\n")
    set_col(CNONE)


# Function to show the winning screen
def show_win(dashed_string, wrong_letters):
    os.system("clear")
    show_title()
    temp = ' '.join(dashed_string)
    set_col(CGREEN, bold=True)
    print(f"{temp:^{COLS}}")
    set_col(CNONE)
    show_hangman(wrong_letters, COLS)
    set_col(CGREEN, bold=True)
    print(f"{'CONGRATULATIONS!! YOU WIN':^{COLS}}\n\n")
    set_col(CNONE)


# Get the list of words from the word_list file
words_list = open('./words', 'r').read().strip().split('\n')

# Display the words to the plater for a few seconds
show_title()
print(f"{'Have a look at the words.':^{COLS}}")
print(f"{'You have 5 seconds.':^{COLS}}\n")
for i in words_list:
    print(f"{i:^{COLS}}")
time.sleep(5)

again = True

while again:
    # Choose a random word from the word list
    word = random.choice(words_list)

    # A list that contains the letters that are already entered by the user
    letters_entered = []

    word_len = len(word)

    # Create the same word with dashes
    dashed_string = ["_"] * word_len

    # A variable that keeps track of the number of wrong letters.
    # Also used to determine the hanging man status to be displayed
    wrong_letters = 0

    # Main loop
    while True:
        # Clear the screen
        os.system("clear")

        show_title()
        temp = ' '.join(dashed_string)
        set_col(HANG_COLS[wrong_letters], bold=True)
        print(f"{temp:^{COLS}}")
        show_hangman(wrong_letters, COLS)
        set_col(HANG_COLS[wrong_letters])
        print(f"{'Letters already used':^{COLS}}")
        temp = ' '.join(letters_entered)
        print(f'{temp:^{COLS}}\n')
        set_col(CNONE)

        # If there are no letters entered pick up a random letter
        if len(letters_entered) == 0:
            letter = random.choice(list(set(word)))
        else:
            input_string = "Enter a letter: "
            set_col(CBLUE)
            print(f"{input_string:>{COLS//2+len(input_string)//2}}",
                  end='', flush=True)
            letter = getche()
            set_col(CNONE)

        # Check if the entered letter is a whitespace or newline
        # If not checked whitespaces and enter count as characters and
        # increase the number of wrong_letters
        if letter in letters_entered or letter in [' ', '\n']:
            continue
        else:
            letters_entered.append(letter)
            if letter in word:
                for i, j in enumerate(word):
                    if j == letter:
                        dashed_string[i] = letter
            else:
                wrong_letters += 1

        # Check for game over
        if wrong_letters == 7:
            show_game_over(dashed_string, word, wrong_letters)
            break

        # Check if the enterd word so far matches the original word
        if ''.join(dashed_string) == word:
            show_win(dashed_string, wrong_letters)
            break

    # Ask the user if the user wants to play again
    prompt_string = "Play again?(y/n)"
    set_col(CGREEN, bold=True)
    print(f"{prompt_string:>{COLS//2+len(prompt_string)//2}}",
          end='', flush=True)
    set_col(CNONE)
    try_again = getche()
    print()

    if try_again.lower() == 'y':
        again = True
    else:
        again = False
