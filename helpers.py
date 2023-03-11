from typing import Union
import random
import pygame
from settings import *

class Rectangle():
    def __init__(self, number: int, x: Union[int, float], y: Union[int, float], height: Union[int, float], font: int=24, color: tuple=WHITE, text_color: tuple=BLACK) -> None:
        self.num = number
        self.x = x
        self.y = y
        self.width = RECT_WIDTH
        self.height = height
        self.font = pygame.font.SysFont(None, font)
        self.color = color
        self.text_color = text_color
        self.border = BLACK

    def draw(self) -> None:
        # Display the rectangle and its outline
        if not status['sorting']: 
            self.color = WHITE
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border, (self.x, self.y, self.width, self.height), 3)
        # Display the number below each rectangle
        self.number_surface = self.font.render(str(self.num), True, self.text_color)
        self.number_rect = self.number_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height + 20))
        screen.blit(self.number_surface , self.number_rect)

class Button():
    def __init__(self, x: Union[int, float], y: Union[int, float], width: Union[int, float], height: Union[int, float], color: tuple, text: str='', font: int=24, text_color: tuple=BLACK) -> None:
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
        self.active = True
        self.clicked = False
        self.visible = True
    
    def draw(self) -> None:
        # Display the button and its outline
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border, self.rect, 3)
        # Display the text inside the button
        self.text_surface = self.font.render(str(self.text), True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.text_surface, self.text_rect)
    
    def click(self) -> None:
        # User clicked on a button
        if self.active:
            self.clicked = True
            self.color = CLICKED

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
    # Rate at which the color changes per frame
    rgb_change = 30
    for btn in buttons:
        # Animate color change of the button when cursor hovers over it
        # Also animates color change when button is inactivated
        if btn.rect.collidepoint(pygame.mouse.get_pos()) and btn.color > HOVER and not btn.clicked:
            status['btn_animate'] = True
            btn.color = (btn.color[0] - min(rgb_change, btn.color[0] - HOVER[0]),
                         btn.color[1] - min(rgb_change, btn.color[1] - HOVER[1]),
                         btn.color[2] - min(rgb_change, btn.color[2] - HOVER[2]))
        # Revert back to original color of the button when cursor no longer hovers over it
        elif not btn.rect.collidepoint(pygame.mouse.get_pos()) and btn.color < WHITE and btn.active and not btn.clicked:
            status['btn_animate'] = True
            btn.color = (btn.color[0] + min(rgb_change, WHITE[0] - btn.color[0]),
                         btn.color[1] + min(rgb_change, WHITE[1] - btn.color[1]),
                         btn.color[2] + min(rgb_change, WHITE[2] - btn.color[2]))
        btn.draw()

def swap_rectangles(rectangles: list) -> None:
    # Swapping is complete if two rectangles have exchanged their positions
    if rectangles[swap_rect['rect1']].x == swap_rect['rect2_pos'] and rectangles[swap_rect['rect2']].x == swap_rect['rect1_pos']:
        status['swapping'] = False
        return

    # Calculate the pixel difference between the two rectangles and scale the swapping speed accordingly
    # This can ensure that the swapping animation of the two farthest rectangles is as fast as the swapping animation of the two closest rectangles
    distance = swap_rect['rect2_pos'] - swap_rect['rect1_pos']
    scaling = int(distance / (RECT_WIDTH + RECT_SPACING))
    
    # Scale the pixel per frame according to the current FPS
    pixel_per_frame = PIXEL_CHANGE[Speed.adjust] * scaling * (60 / FPS['active'])

    # Change both rectangles' x coordinates until one approaches the other's position
    if rectangles[swap_rect['rect1']].x < swap_rect['rect2_pos']:
        # If pixel difference between stopping position and rectangle 1 position is less than the pixels per frame, change pixel by the difference instead
        rectangles[swap_rect['rect1']].x += min(pixel_per_frame, swap_rect['rect2_pos'] - rectangles[swap_rect['rect1']].x)
    if rectangles[swap_rect['rect2']].x > swap_rect['rect1_pos']:
        # If pixel difference between rectangle 2 position and stopping position is less than the pixels per frame, change pixel by the difference instead
        rectangles[swap_rect['rect2']].x -= min(pixel_per_frame, rectangles[swap_rect['rect2']].x - swap_rect['rect1_pos'])

def sorting_sub_rectangles(rectangles: list) -> None:
    # Subarray sorting is complete if rectangle have approached its position 
    if rectangles[sub_sort['rect']].x == sub_sort['rect_pos_dest'] and int(rectangles[sub_sort['rect']].y + rectangles[sub_sort['rect']].height) == 500:
        status['sub_sorting'] = False
        return
    
    # Calculate the x-coordinate pixel difference between the rectangle's current position and stopping position and scale the moving speed accordingly
    x_distance = abs(sub_sort['rect_pos_dest'] - sub_sort['rect_x_pos'])
    x_scaling = int(x_distance / (RECT_WIDTH + RECT_SPACING))

    # Scale the x-coordinate pixel per frame according to the current FPS
    x_pixel_per_frame = PIXEL_CHANGE[Speed.adjust] * x_scaling * (60 / FPS['active']) / 2
    
    # Scale the y-coordinate pixel per frame according to the x-coordinate pixel per frame
    if x_distance != 0:
        y_pixel_per_frame = x_pixel_per_frame * 250 / x_distance
    else:
        y_pixel_per_frame = PIXEL_CHANGE[Speed.adjust] * int(250 / (RECT_WIDTH + RECT_SPACING)) * (60 / FPS['active']) / 2

    # Change each rectangle's x and y coordinates
    # If pixel difference between current rectangle and the stopping position is less than the pixel per frame, change pixel by the difference instead
    if rectangles[sub_sort['rect']].x < sub_sort['rect_pos_dest']:
        rectangles[sub_sort['rect']].x += min(x_pixel_per_frame, sub_sort['rect_pos_dest'] - rectangles[sub_sort['rect']].x)
    elif rectangles[sub_sort['rect']].x > sub_sort['rect_pos_dest']:
        rectangles[sub_sort['rect']].x -= min(x_pixel_per_frame, rectangles[sub_sort['rect']].x - sub_sort['rect_pos_dest'])

    rectangles[sub_sort['rect']].y += min(y_pixel_per_frame, 500 - (rectangles[sub_sort['rect']].y + rectangles[sub_sort['rect']].height))

def merge_rectangles(rectangles: list) -> None:
    # Merging is complete if all rectangles have moved back up to their original positions
    if rectangles[merge_rect[0]].y + rectangles[merge_rect[0]].height == 250:
        status['merging'] = False
        return
    
    # Scale the moving speed accordingly and the pixel per frame according to the current FPS
    y_scaling = int(250 / (RECT_WIDTH + RECT_SPACING))
    y_pixel_per_frame = PIXEL_CHANGE[Speed.adjust] * y_scaling * (60 / FPS['active']) / 2

    for rect in range(merge_rect[0], merge_rect[1]):
        # If pixel difference between current rectangle and the stopping position is less than the pixel per frame, change pixel by the difference instead
        rectangles[rect].y -= min(y_pixel_per_frame, rectangles[rect].y + rectangles[rect].height - 250)

def move_rectangles_up(rectangles: list) -> None:
    # Move base of all rectangles up to y = 250px
    if rectangles[0].y + rectangles[0].height > 250:
        for rectangle in rectangles:
            rectangle.y -= 3
    elif rectangles[0].y + rectangles[0].height == 250:
        status['moving'] = False

def move_rectangles_down(rectangles: list) -> None:
    # Move all rectangles back down to original base
    if rectangles[0].y + rectangles[0].height < BASE:
        for rectangle in rectangles:
            rectangle.y += 3
    elif rectangles[0].y + rectangles[0].height == BASE:
        status['moving'] = False
