import pygame
import threading
from sort import *
from settings import *
from helpers import *

# Import all modules from pygame
pygame.init()
pygame.font.init()

# Create a clock object for controlling frame rate
clock = pygame.time.Clock()

# Infomation for swapping two rectangles: both rectangles' index in the array and their positions (x coordinates)
swap_rect = {'rect1': None, 'rect1_pos': None, 'rect2': None, 'rect2_pos': None}

def main():
    # Set up the font object
    default_font_size = 24
    font = pygame.font.SysFont(None, default_font_size)

    # Create a dictionary for storing iterative sort functions as arguments (used for creating a thread later)
    sort_algs = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        #"Merge Sort": None, # In development
        #"Quick Sort": None # In development
    }

    # Create interactive buttons
    sort_algs = create_sort_btns(sort_algs)
    randomize_btn = Button(x=SCREEN_WIDTH - S_BTN_WIDTH - MARGIN[0], y=MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Randomize")
    start_btn = Button(x=MARGIN[0], y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Start")
    stop_btn = Button(x=MARGIN[0], y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Stop")
    pause_btn = Button(x=MARGIN[0] + S_BTN_WIDTH + BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=S_BTN_WIDTH, height=BTN_HEIGHT, color=WHITE, text="Pause")

    adjust_speed_text = font.render("Adjust speed", True, BLACK) 
    slow_down_btn = Button(x=SCREEN_WIDTH // 2 - BTN_HEIGHT - adjust_speed_text.get_width() / 2 - BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=BTN_HEIGHT, height=BTN_HEIGHT, color=WHITE, text="-", font=36)
    speed_up_btn = Button(x=SCREEN_WIDTH // 2 + adjust_speed_text.get_width() / 2 + BTN_SPACING, y=SCREEN_HEIGHT - BTN_HEIGHT - MARGIN[1], width=BTN_HEIGHT, height=BTN_HEIGHT, color=WHITE, text="+", font=36)

    # Seperate buttons displayed when program is performing sort and when it's idle
    idle_buttons = [sort_btn for sort_btn in sort_algs.keys()] + [randomize_btn, start_btn]
    action_buttons = [stop_btn, pause_btn]
    speed_buttons = [slow_down_btn, speed_up_btn]
    idle_buttons_visible = True
    action_buttons_visible = False

    # Initialize list for storing elements and rectangles
    rectangles = []

    # Randomize the elements
    randomize_array(rectangles)

    # Speed adjust of sorting
    speed_adjust = [len(PIXEL_CHANGE) // 3]
    scan_speed = [(RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[speed_adjust[0]] / FPS['idle'] / 60 * FPS['idle']]

    selected = {'alg': None, 'function': None}

    # Main operation of the program
    while True:
        # Fill user interface with white background
        screen.fill(WHITE)

        for event in pygame.event.get():
            # Abort the program and halt all sorting operations when user X out the window
            if event.type == pygame.QUIT:
                sorting.clear()
                swapping.clear()
                playing.set()
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not sorting.is_set() and not swapping.is_set():
                    pause_btn.text = "Pause"
                    # Randomize array if user clicked on "Randomize" button
                    if randomize_btn.rect.collidepoint(event.pos):
                        randomize_btn.click()
                        randomize_array(rectangles)
                    for sort in sort_algs:
                        # If user clicked on one of the sorting buttons
                        if sort.rect.collidepoint(event.pos):
                            sort.click()
                            sort.active = False
                            # Save the selected sorting algorithm
                            selected['alg'] = sort
                            selected['function'] = sort_algs[sort]
                    # Reset color of sort buttons
                    for sort in sort_algs:
                        if sort_algs[sort] != selected['function']:
                            sort.active = True
                    if start_btn.rect.collidepoint(event.pos):
                        start_btn.click()
                        # Start sorting operation if there is a user has selected a sorting algorithm
                        if selected['function']:
                            sorting.set()
                            playing.set()
                            # Begin sorting process and start a thread, target being the selected sorting algorithm
                            sort_thread = threading.Thread(target=selected['function'], args=(rectangles, len(rectangles), swap_rect, scan_speed))
                            sort_thread.start()
                            selected['alg'].active = True
                # Abort sorting operation if user clicked on the "Stop" button
                if stop_btn.rect.collidepoint(event.pos) and action_buttons_visible:
                    stop_btn.click()
                    playing.set()
                    sorting.clear()
                    selected['alg'] = None
                    selected['function'] = None
                # Pause the sorting operation if user clicked on the "Pause" button
                # Continue the sorting operation if user clicked on the "Continue" button
                elif pause_btn.rect.collidepoint(event.pos):
                    pause_btn.click()
                    playing.clear() if playing.is_set() else playing.set()
                    pause_btn.text = "Pause" if playing.is_set() else "Continue"
                # Increase the speed of sorting until it is at highest speed
                elif speed_up_btn.rect.collidepoint(event.pos):
                    if speed_adjust[0] < len(PIXEL_CHANGE) - 1:
                        slow_down_btn.active = True
                        speed_up_btn.click()
                        speed_adjust[0] += 1
                        # Deactivate the speed down button if speed of sorting is at its lowest
                        if speed_adjust[0] == len(PIXEL_CHANGE) - 1:
                            speed_up_btn.active = False
                # Decrease the speed of sorting until it is at lowest speed
                elif slow_down_btn.rect.collidepoint(event.pos):
                    if speed_adjust[0] > 0:
                        speed_up_btn.active = True
                        slow_down_btn.click()
                        speed_adjust[0] -= 1
                        # Deactivate the slow down button if speed of sorting is at its lowest
                        if speed_adjust[0] == 0:
                            slow_down_btn.active = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Revert to hovering color if user releases the left mouse click
                for btn in idle_buttons + action_buttons + speed_buttons:
                    btn.clicked = False
                    if btn.rect.collidepoint(event.pos) or not btn.active:
                        btn.color = HOVER

        # Make idle buttons hidden and action buttons shown when sorting
        if sorting.is_set(): idle_buttons_visible, action_buttons_visible = False, True
        else: idle_buttons_visible, action_buttons_visible = True, False
        
        # Reset button color if not visible on the window
        for btn in idle_buttons + action_buttons:
            if btn in action_buttons and not action_buttons_visible: btn.color = WHITE
            elif btn in idle_buttons and not idle_buttons_visible: btn.color = WHITE
        
        if swapping.is_set():
            # Animate the swapping of the two rectangles
            swap_rectangles(rectangles, swap_rect, speed_adjust)
        
        if pygame.display.get_active():
            btn_animate.clear()
            if idle_buttons_visible and len(threading.enumerate()) == 1:
                # Display "idle" buttons when sorting operation is not active
                draw_buttons(idle_buttons)
            elif sorting.is_set():
                # Display "action" buttons when sorting operation is active
                selected_alg = pygame.font.SysFont(None, 28).render(selected['alg'].text, True, BLACK)
                screen.blit(selected_alg, (MARGIN[0], MARGIN[1]))
                draw_buttons(action_buttons)

            # Display speed buttons
            screen.blit(adjust_speed_text, (SCREEN_WIDTH / 2 - adjust_speed_text.get_width() / 2, SCREEN_HEIGHT - slow_down_btn.height / 2  - MARGIN[1] -  adjust_speed_text.get_height() / 2))
            draw_buttons(speed_buttons)

            # Display FPS
            fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, BLACK)
            screen.blit(fps_text, (SCREEN_WIDTH - fps_text.get_width() - MARGIN[0], SCREEN_HEIGHT - fps_text.get_height() - MARGIN[1]))

        # Update the screen and display all rectangles if window is opened
            draw_rectangles(rectangles)
            pygame.display.flip()

        if (sorting.is_set() and playing.is_set()) or btn_animate.is_set() or swapping.is_set():
            # Set FPS to 60 if program is currently playing sorting animation or button hovering animation or swapping animation
            # Scale scan speed according to the current FPS
            scan_speed[0] = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[speed_adjust[0]] / 60 / FPS['active'] * 60
            clock.tick(FPS['active'])
        else:
            # Lower FPS if program is idle
            # Scale scan speed according to the current FPS
            scan_speed[0] = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[speed_adjust[0]] / FPS['idle'] / 60 * FPS['idle']
            clock.tick(FPS['idle'])

if __name__ == "__main__":
    main()
