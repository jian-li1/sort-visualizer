import pygame
import threading
import os
import sys
import platform

# Width and height of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

# If running in PyInstaller bundle, get the path to the root directory of the bundle using the sys._MEIPASS attribute
# Else if running in normal Python runtime environment, get the path to the directory containing the Python script
root_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

try:
    if platform.system() == "Darwin":
        img_path = os.path.join(root_dir, 'assets', 'icon_1024x1024.png')
    else:
        img_path = os.path.join(root_dir, 'assets', 'app_icon.JPG')
except FileNotFoundError:
    pass

# Display application icon
icon_surface = pygame.image.load(img_path)
pygame.display.set_icon(icon_surface)

# Initialize screen and title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sort Visualizer")

# Frames per second
FPS = {'active': 60, 'idle': 10}

# RGB number for each color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER = (180, 180, 180)
CLICKED = (150, 150, 150)
RED = (255, 0, 0)

# Width and height of the rectangles and the number of rectangles being displayed
RECT_WIDTH, RECT_HEIGHT = 25, 10
NUM_RECT = 30

# Base of the rectangles and the alignment
BASE = 400
RECT_SPACING = 3
MARGIN = [(SCREEN_WIDTH - ((RECT_WIDTH + RECT_SPACING) * NUM_RECT - RECT_SPACING)) / 2, 10]

# Width and height of the buttons and the spacing between each button
L_BTN_WIDTH, BTN_HEIGHT = 125, 50
S_BTN_WIDTH = 100
BTN_SPACING = 5

# The rate at which the rectangles move
PIXEL_CHANGE = [i / 100 for i in range(25, (RECT_WIDTH + RECT_SPACING + 1) * 100, 25) if (RECT_WIDTH + RECT_SPACING) % (i / 100) == 0] 
#[i for i in range(1, RECT_WIDTH + RECT_SPACING + 1) if (RECT_WIDTH + RECT_SPACING) % i == 0]

# Initialize variables for keeping track of the program's status
status = {
    'sorting': False, # Is set when sorting operation is active
    'playing': threading.Event(), # Is set when sorting operation is being played
    'swapping': False, # Is set when swapping is being animated
    'moving': False, # Is set when rectangle is moving up or down
    'sub_sorting': False, # Is set when sorting sub arrays during merge sort
    'merging': False, # Is set when merging is being animated
    'btn_animate': False # Is set when user hovers over a button; animates color change of the button
}

# Speed adjust and delay of sorting
class Speed():
    adjust = len(PIXEL_CHANGE) // 3
    delay = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[adjust] / FPS['idle'] / 60 * FPS['idle']

# Pivot line for quick sorting
quick_sort_line = {'start': None, 'end': None}
# Infomation for swapping two rectangles: both rectangles' index in the array and their positions (x coordinates)
swap_rect = {'rect1': None, 'rect1_pos': None, 'rect2': None, 'rect2_pos': None}
# Information for moving two rectangles for merge sorting
sub_sort = {'rect': None, 'rect_x_pos': None, 'rect_pos_dest': None}
merge_rect = [None, None]

# Selected algorithm
selected = {'alg': None, 'text': '', 'function': None}
