import pygame
import random
import threading
from sort import bubble_sort, selection_sort, insertion_sort
import os
import sys
from typing import Union

# Import all modules from pygame
pygame.init()
pygame.font.init()

# If running in PyInstaller bundle, get the path to the root directory of the bundle using the sys._MEIPASS attribute
# Else if running in normal Python runtime environment, get the path to the directory containing the Python script
root_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(root_dir, 'assets', 'icon_1024x1024.png')

# Display application icon
icon_surface = pygame.image.load(img_path)
pygame.display.set_icon(icon_surface)

# Width and height of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600

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
L_BTN_WIDTH, BTN_HEIGHT = 150, 50
S_BTN_WIDTH = 100
BTN_SPACING = 5

# The rate at which the rectangles move
PIXEL_CHANGE = [] #[i for i in range(1, RECT_WIDTH + RECT_SPACING + 1) if (RECT_WIDTH + RECT_SPACING) % i == 0]
i = 0.25
while i < RECT_WIDTH + RECT_SPACING + 1:
    if (RECT_WIDTH + RECT_SPACING) % i == 0:
        PIXEL_CHANGE.append(i)
    i += 0.25

# Infomation for swapping two rectangles: both rectangles' index in the array and their positions (x coordinates)
swap_rect = {'rect1': None, 'rect1_pos': None, 'rect2': None, 'rect2_pos': None}

# Initialize screen and title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sort Visualizer")

# Initialize variables for keeping track of the program's status
abort = {'status': False}
sorting = threading.Event()
playing = threading.Event()
swapping = threading.Event()
hovering = threading.Event()

# Frames per second
FPS = 60
idle_FPS = 10

class Rectangle():
    def __init__(self, number: int, x: Union[int, float], y: Union[int, float], height: Union[int, float], font: int=24, color: tuple=WHITE):
        self.num = number
        self.x = x
        self.y = y
        self.height = height
        self.font = pygame.font.SysFont(None, font)
        self.color = color

    def draw(self):
        # Display the rectangle and its outline
        if not sorting.is_set(): self.color = WHITE
        pygame.draw.rect(screen, self.color, (self.x, self.y, RECT_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, RECT_WIDTH, self.height), 3)
        # Display the number below each rectangle
        self.number_surface = self.font.render(str(self.num), True, BLACK)
        self.number_rect = self.number_surface.get_rect(center=(self.x + RECT_WIDTH // 2, self.y + self.height + 20))
        screen.blit(self.number_surface , self.number_rect)

class Button():
    def __init__(self, x: Union[int, float], y: Union[int, float], width: Union[int, float], height: Union[int, float], color: tuple, text: str='', font: int=24, text_color: tuple=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.border = BLACK
        self.font = pygame.font.SysFont(None, font)
    
    def draw(self):
        # Display the button and its outline
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border, self.rect, 3)
        # Display the text inside the button
        self.text_surface = self.font.render(str(self.text), True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.text_surface, self.text_rect)

def create_sort_btns(sort_dict: dict) -> dict:
    sort_algs = dict()
    # Generate buttons for the sorting algorithms
    for i, sort in enumerate(sort_dict):
        sort_btn = Button(x=MARGIN[0] + i * L_BTN_WIDTH + i * BTN_SPACING, y=MARGIN[1], width=L_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text=sort)
        sort_algs[sort_btn] = sort_dict[sort]
    # Return a dictionary with the button objects and the sort functions
    return sort_algs
        
def randomize_array(rectangles: list) -> None:
    rectangles.clear()
    i = 0
    # Randomize an array with unique integers from 1 to 99
    for number in random.sample(range(1, 100), NUM_RECT):
        rectangles.append(Rectangle(number=number, x=MARGIN[0] + (RECT_WIDTH + RECT_SPACING) * i, y=BASE - RECT_HEIGHT - number * 2, height=RECT_HEIGHT + number * 2))
        i += 1

def draw_rectangles(rectangles: list) -> None:
    for rectangle in rectangles:
        # Display each rectangle
        rectangle.draw()

def draw_buttons(buttons: list) -> None:
    global idle_FPS
    idle_FPS = 10
    # Rate at which the color changes per fram
    rgb_change = 15
    hovering.clear()
    for btn in buttons:
        # Animate color change of the button when cursor hovers over it
        if btn.rect.collidepoint(pygame.mouse.get_pos()) and btn.color > HOVER:
            hovering.set()
            btn.color = (btn.color[0] - rgb_change, btn.color[1] - rgb_change, btn.color[2] - rgb_change)
        # Revert back to original color of the button when cursor no longer hovers over it
        elif not btn.rect.collidepoint(pygame.mouse.get_pos()) and btn.color < WHITE:
            hovering.set()
            btn.color = (btn.color[0] + rgb_change, btn.color[1] + rgb_change, btn.color[2] + rgb_change)
        if btn.color == HOVER:
            idle_FPS = 20
        btn.draw()

def swap_rectangles(rectangles: list, swapping: threading.Event, rect1: int, rect2: int, rect1_pos: Union[int, float], rect2_pos: Union[int, float], speed_adjust: list) -> None:
    # Swapping is complete if two rectangles have exchanged their positions
    if rectangles[rect1].x == rect2_pos and rectangles[rect2].x == rect1_pos:
        swapping.clear()
        return

    # Calculate the pixel difference between the two rectangles and scale up or down the swapping speed accordingly
    # This can ensure that the swapping animation of the two farthest rectangles is as fast as the swapping animation of the two closest rectangles
    distance = rect2_pos - rect1_pos
    scaling = int(distance / (RECT_WIDTH + RECT_SPACING))
    
    pixel_per_frame = PIXEL_CHANGE[speed_adjust[0]] * scaling

    # Change both rectangles' x coordinates until one approaches the other's position
    if rectangles[rect1].x < rect2_pos:
        if rect2_pos - rectangles[rect1].x >= pixel_per_frame:
            rectangles[rect1].x += PIXEL_CHANGE[speed_adjust[0]] * scaling
        else:
            rectangles[rect1].x += rectangles[rect2].x - rect1_pos
    if rectangles[rect2].x > rect1_pos:
        if rectangles[rect2].x - rect1_pos >= pixel_per_frame:
            rectangles[rect2].x -= PIXEL_CHANGE[speed_adjust[0]] * scaling
        else:
            rectangles[rect2].x -= rectangles[rect2].x - rect1_pos

def main():
    # Create a clock object for controlling frame rate
    clock = pygame.time.Clock()

    # Set up the font object
    default_font_size = 24
    font = pygame.font.SysFont(None, default_font_size)

    # Create a dictionary for storing iterative sort functions as arguments (used for creating a thread later)
    iter_sort = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort
    }

    # Create interactive buttons
    iter_sort = create_sort_btns(iter_sort)
    randomize_btn = Button(x=SCREEN_WIDTH - S_BTN_WIDTH - MARGIN[0], y=MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Randomize")
    stop_btn = Button(x=MARGIN[0], y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Stop")
    pause_btn = Button(x=MARGIN[0] + S_BTN_WIDTH + BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Pause")

    adjust_speed_text = font.render("Adjust speed", True, BLACK) 
    slow_down_btn = Button(x=SCREEN_WIDTH // 2 - BTN_HEIGHT - adjust_speed_text.get_width() / 2 - BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=BTN_HEIGHT, height=BTN_HEIGHT, color=WHITE, text="-", font=36)
    speed_up_btn = Button(x=SCREEN_WIDTH // 2 + adjust_speed_text.get_width() / 2 + BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=BTN_HEIGHT, height=BTN_HEIGHT, color=WHITE, text="+", font=36)

    # Seperate buttons displayed when program is performing sort and when it's not
    idle_buttons = [sort_btn for sort_btn in iter_sort.keys()] + [randomize_btn]
    idle_buttons_visible = True
    action_buttons = [stop_btn, pause_btn, slow_down_btn, speed_up_btn]
    action_buttons_visible = False

    # Initialize list for storing elements and rectangles
    rectangles = []

    randomize_array(rectangles)

    speed_adjust = [len(PIXEL_CHANGE) // 4]
    scan_speed = [(RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[speed_adjust[0]] / 60]

    # Main operation of the program
    while True:
        # Fill user interface with white background
        screen.fill(WHITE)

        scan_speed[0] = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[speed_adjust[0]] / 60

        for event in pygame.event.get():
            # Abort the program and halt all sorting operations when user X out the window
            if event.type == pygame.QUIT or abort['status']:
                pygame.quit()
                sorting.clear()
                swapping.clear()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Randomize array if user clicked on "Randomize" button
                if not sorting.is_set() and not swapping.is_set() and randomize_btn.rect.collidepoint(event.pos):
                    randomize_btn.color = CLICKED
                    randomize_array(rectangles)
                for sort in iter_sort.keys():
                    # If user clicked on one of the sorting buttons
                    if not sorting.is_set() and not swapping.is_set() and sort.rect.collidepoint(event.pos):
                        # Begin sorting process and start a thread, target being the selected sorting algorithm
                        sorting.set()
                        playing.set()
                        sort_thread = threading.Thread(target=iter_sort[sort], args=(rectangles, len(rectangles), swap_rect, swapping, sorting, playing, scan_speed))
                        sort_thread.start()
                        pause_btn.text = "Pause"
                        break
                # Abort sorting operation if user clicked on the "Stop" button
                if stop_btn.rect.collidepoint(event.pos):
                    stop_btn.color = CLICKED
                    playing.set()
                    sorting.clear()
                # Pause the sorting operation if user clicked on the "Pause" button
                # Continue the sorting operation if user clicked on the "Continue" button
                elif pause_btn.rect.collidepoint(event.pos):
                    pause_btn.color = CLICKED
                    playing.clear() if playing.is_set() else playing.set()
                    pause_btn.text = "Pause" if playing.is_set() else "Continue"
                # Increase the speed of sorting until it is at highest speed
                elif speed_up_btn.rect.collidepoint(event.pos):
                    if speed_adjust[0] < len(PIXEL_CHANGE) - 1:
                        speed_up_btn.color = CLICKED
                        speed_adjust[0] += 1
                # Decrease the speed of sorting until it is at lowest speed
                elif slow_down_btn.rect.collidepoint(event.pos):
                    if speed_adjust[0] > 0:
                        slow_down_btn.color = CLICKED
                        speed_adjust[0] -= 1
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Revert to hovering color if user releases the left mouse click
                for btn in idle_buttons + action_buttons:
                    if btn.rect.collidepoint(event.pos): btn.color = HOVER

        # Make idle buttons hidden and action buttons shown when sorting
        if sorting.is_set(): idle_buttons_visible, action_buttons_visible = False, True
        else: idle_buttons_visible, action_buttons_visible = True, False
        
        # Reset button color if not visible on the window
        for btn in idle_buttons + action_buttons:
            if btn in action_buttons and not action_buttons_visible: btn.color = WHITE
            elif btn in idle_buttons and not idle_buttons_visible: btn.color = WHITE
        
        if swapping.is_set():
            # Animate the swapping of the two rectangles
            swap_rectangles(rectangles, swapping, swap_rect['rect1'], swap_rect['rect2'], swap_rect['rect1_pos'], swap_rect['rect2_pos'], speed_adjust)

        # Display all the rectangles
        draw_rectangles(rectangles)
        
        if idle_buttons_visible and len(threading.enumerate()) == 1:
            # Display "idle" buttons when sorting operation is not active
            draw_buttons(idle_buttons)
        elif sorting.is_set():
            # Display "action" buttons when sorting operation is active
            screen.blit(adjust_speed_text, (SCREEN_WIDTH / 2 - adjust_speed_text.get_width() / 2, SCREEN_HEIGHT - slow_down_btn.height / 2  - MARGIN[1] -  adjust_speed_text.get_height() / 2))
            draw_buttons(action_buttons)

        # Update the screen
        pygame.display.flip()
        if (sorting.is_set() and playing.is_set()) or hovering.is_set() or swapping.is_set():
            # Set FPS to 60 if program is currently playing sorting animation or button hovering animation or swapping animation
            clock.tick(FPS)
        else:
            # Lower FPS if program is idle
            clock.tick(idle_FPS)

if __name__ == "__main__":
    main()