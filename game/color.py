import os
class Color:
    RESET = '\033[0m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    GRAY = '\033[90m'
    BLUE = '\033[34m'
    ORANGE = '\033[38;5;208m'
    LIME = '\033[92m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GRAY = '\033[100m'
    CLEAR_SCREEN = os.system('cls')



