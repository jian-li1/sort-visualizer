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

def main():
    # Set up the font object
    default_font_size = 24
    font = pygame.font.SysFont(None, default_font_size)

    # Create a dictionary for storing iterative sort functions as arguments (used for creating a thread later)
    sort_algs = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
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

    # Initialize list for storing elements and rectangles
    rectangles = []

    # Randomize the elements
    randomize_array(rectangles)

    sort_thread = threading.Thread()

    # Main operation of the program
    while True:
        # Fill user interface with white background
        screen.fill(WHITE)

        for event in pygame.event.get():
            # Abort the program and halt all sorting operations when user X out the window
            if event.type == pygame.QUIT:
                status['sorting'] = False
                status['swapping'] = False
                status['playing'].set()
                # Only applicable to merge sorting
                while selected['function'] == merge_sort and sort_thread.is_alive():
                    status['moving'] = False
                    status['sub_sorting'] = False
                    status['merging'] = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not status['sorting']:
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
                            selected['text'] = sort.text
                    # Reset color of sort buttons
                    for sort in sort_algs:
                        if sort_algs[sort] != selected['function']:
                            sort.active = True
                    if start_btn.rect.collidepoint(event.pos):
                        start_btn.click()
                        # Start sorting operation if there is a user has selected a sorting algorithm
                        if selected['function']:
                            status['sorting'] = True
                            status['playing'].set()
                            # Begin sorting process and start a thread, target being the selected sorting algorithm
                            sort_thread = threading.Thread(target=selected['function'], args=(rectangles, len(rectangles)))
                            sort_thread.start()
                            selected['alg'].active = True
                # Abort sorting operation if user clicked on the "Stop" button
                if stop_btn.rect.collidepoint(event.pos) and stop_btn.visible:
                    stop_btn.click()
                    status['playing'].set()
                    status['sorting'] = False
                    selected['alg'] = None
                    selected['function'] = None
                    selected['text'] = ''
                # Pause the sorting operation if user clicked on the "Pause" button
                # Continue the sorting operation if user clicked on the "Continue" button
                elif pause_btn.rect.collidepoint(event.pos):
                    pause_btn.click()
                    status['playing'].clear() if status['playing'].is_set() else status['playing'].set()
                    pause_btn.text = "Pause" if status['playing'].is_set() else "Continue"
                # Increase the speed of sorting until it is at highest speed
                elif speed_up_btn.rect.collidepoint(event.pos):
                    if Speed.adjust < len(PIXEL_CHANGE) - 1:
                        slow_down_btn.active = True
                        speed_up_btn.click()
                        Speed.adjust += 1
                        # Deactivate the speed down button if speed of sorting is at its lowest
                        if Speed.adjust == len(PIXEL_CHANGE) - 1:
                            speed_up_btn.active = False
                # Decrease the speed of sorting until it is at lowest speed
                elif slow_down_btn.rect.collidepoint(event.pos):
                    if Speed.adjust > 0:
                        speed_up_btn.active = True
                        slow_down_btn.click()
                        Speed.adjust -= 1
                        # Deactivate the slow down button if speed of sorting is at its lowest
                        if Speed.adjust == 0:
                            slow_down_btn.active = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Revert to hovering color if user releases the left mouse click
                for btn in idle_buttons + action_buttons + speed_buttons:
                    btn.clicked = False
                    if (btn.rect.collidepoint(event.pos) or not btn.active) and btn.visible:
                        btn.color = HOVER

        # Make idle buttons hidden and action buttons shown when sorting
        if status['sorting'] or sort_thread.is_alive(): 
            for btn in idle_buttons: btn.visible = False
            for btn in action_buttons: btn.visible = True
        # Make idle buttons shown and action buttons hidden when idle
        else:
            for btn in idle_buttons: btn.visible = True
            for btn in action_buttons: btn.visible = False
        
        # Reset button color if not visible on the window
        for btn in idle_buttons + action_buttons:
            if not btn.visible: btn.color = WHITE
        
        # Animate the swapping of the two rectangles
        if status['swapping']: swap_rectangles(rectangles)

        # Animate the sorting of the sub arrays (merge sort)
        elif status['sub_sorting']: sorting_sub_rectangles(rectangles)
        
        # Animate the merging of the sub arrays (merge sort)
        elif status['merging']: merge_rectangles(rectangles)

        # Move rectangles up and down for merge sort
        if status['moving'] and status['sorting']:
            move_rectangles_up(rectangles)
        elif status['moving'] and not status['sorting']:
            move_rectangles_down(rectangles)
        
        # If window is opened
        if pygame.display.get_active():
            status['btn_animate'] = False
            if not sort_thread.is_alive():
                # Display "idle" buttons when sorting operation is not active
                draw_buttons(idle_buttons)
            elif status['sorting']:
                # Display "action" buttons when sorting operation is active
                display_info = pygame.font.SysFont(None, 28).render(f"{selected['text']}", True, BLACK)
                screen.blit(display_info, (MARGIN[0], MARGIN[1]))
                draw_buttons(action_buttons)

            # Display speed buttons
            screen.blit(adjust_speed_text, (SCREEN_WIDTH / 2 - adjust_speed_text.get_width() / 2, SCREEN_HEIGHT - slow_down_btn.height / 2  - MARGIN[1] -  adjust_speed_text.get_height() / 2))
            draw_buttons(speed_buttons)

            # Display FPS
            fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, BLACK)
            screen.blit(fps_text, (SCREEN_WIDTH - fps_text.get_width() - MARGIN[0], SCREEN_HEIGHT - fps_text.get_height() - MARGIN[1]))

            # Update the screen and display all rectangles
            draw_rectangles(rectangles)

            # Pivot line for quick sort
            if selected['function'] == quick_sort and status['sorting']:        
                pygame.draw.line(screen, BLACK, (quick_sort_line['start'][0], quick_sort_line['end'][1]), (quick_sort_line['end'][0] + RECT_WIDTH, quick_sort_line['end'][1]))

            pygame.display.flip() # Update display

        if (sort_thread.is_alive() and status['playing'].is_set()) or status['btn_animate'] or status['swapping'] or status['sub_sorting'] or status['merging']:
            # Set FPS to 60 if program is currently playing sorting animation or button hovering animation or swapping animation
            # Scale scan speed according to the current FPS
            Speed.delay = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[Speed.adjust] / 60 / FPS['active'] * 60
            clock.tick(FPS['active'])
        else:
            # Lower FPS if program is idle
            # Scale scan speed according to the current FPS
            Speed.delay = (RECT_WIDTH + RECT_SPACING) / PIXEL_CHANGE[Speed.adjust] / FPS['idle'] / 60 * FPS['idle']
            clock.tick(FPS['idle'])

if __name__ == "__main__":
    main()
