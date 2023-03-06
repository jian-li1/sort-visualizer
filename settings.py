import pygame
import threading

# Width and height of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

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
sorting = threading.Event() # Is set when sorting operation is active
playing = threading.Event() # Is set when sorting operation is being played
swapping = threading.Event() # Is set when swapping is being animated
hovering = threading.Event() # Is set when user hovers over a button; animates color change of the button