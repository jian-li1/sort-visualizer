import time
import threading
from settings import *

# Create a threading lock to ensure that only one sorting thread runs at a time
lock = threading.Lock()

# Bubble Sort
def bubble_sort(array: list, size: int, swap_index: dict, scan_speed: list) -> None:
    time.sleep(0.2)
    lock.acquire()
    i = 0
    while i < size - 1 and sorting.is_set():
        j = 0
        while j < size - i - 1 and sorting.is_set():
            # Highlight the two elements being compared
            array[j].color = RED
            array[j+1].color = RED

            time.sleep(scan_speed[0])
            
            if array[j].num > array[j+1].num:
                # Store the two rectangles' index and positions
                swap_index['rect1'] = j
                swap_index['rect2'] = j + 1
                swap_index['rect1_pos'] = array[j].x
                swap_index['rect2_pos'] = array[j+1].x

                # Begin swapping process on the GUI
                if sorting.is_set(): 
                    swapping.set()
                    while swapping.is_set():
                        time.sleep(0.01)
                    # Swap elements
                    array[j], array[j+1] = array[j+1], array[j]

            # Pause if requested by user
            playing.wait()
            # Abort sorting operation if user clicked on "Stop"
            if not sorting.is_set(): break

            array[j].color = WHITE
            array[j + 1].color = WHITE

            j += 1
        i += 1

    lock.release()
    sorting.clear()
    playing.clear()
    return

# Selection Sort
def selection_sort(array: list, size: int, swap_index: dict, scan_speed: list) -> None:
    time.sleep(0.2)
    lock.acquire()
    i = 0
    while i < size and sorting.is_set():
        min = array[i]
        min_index = i

        # Pause if requested by user
        playing.wait()
        # Abort sorting operation if user clicked on "Stop"
        if not sorting.is_set(): break

        # Highlight the rectangle with the minimum value 
        if sorting.is_set(): array[min_index].color = RED
        time.sleep(scan_speed[0])

        j = i + 1
        while j < size and sorting.is_set():
            # Highlight the rectangle being scanned
            array[j].color = RED
            
            # Pause if requested by user
            playing.wait()
            # Abort sorting operation if user clicked on "Stop"
            if not sorting.is_set(): break
            
            time.sleep(scan_speed[0])

            # Update current value to minimum value if current value if smaller than current minimum value
            if array[j].num < min.num:
                array[min_index].color = WHITE
                min = array[j]
                min_index = j
            else:
                array[j].color = WHITE

            j += 1

        # Store the two rectangles' index and positions
        swap_index['rect1'] = i
        swap_index['rect2'] = min_index
        swap_index['rect1_pos'] = array[i].x
        swap_index['rect2_pos'] = array[min_index].x

        # Begin swapping process on the GUI
        if sorting.is_set(): 
            swapping.set()
            while swapping.is_set():
                time.sleep(0.01)
                # Swap elements
            array[i], array[min_index] = array[min_index], array[i]

        array[i].color = WHITE
        array[min_index].color = WHITE

        i += 1

    array[min_index].color = WHITE
    lock.release()
    sorting.clear()
    playing.clear()
    return

def insertion_sort(array: list, size: int, swap_index: dict, scan_speed:  list) -> None:
    time.sleep(0.2)
    lock.acquire()
    index = 0
    while index < size - 1 and sorting.is_set():
        i = index
        j = i + 1

        # Pause if requested by user
        playing.wait()
        # Abort sorting operation if user clicked on "Stop"
        if not sorting.is_set(): break

        while array[j].num < array[i].num and i >= 0 and sorting.is_set():
            # Highlight the two elements being compared
            array[i].color = RED
            array[j].color = RED

            time.sleep(scan_speed[0])
            
            # Store the two rectangles' index and positions
            swap_index['rect1'] = i
            swap_index['rect2'] = j
            swap_index['rect1_pos'] = array[i].x
            swap_index['rect2_pos'] = array[j].x

            # Begin swapping process on the GUI
            if sorting.is_set(): 
                swapping.set()
                while swapping.is_set():
                    time.sleep(0.01)
                # Swap elements
                array[i], array[j] = array[j], array[i]
            
            # Pause if requested by user
            playing.wait()
            # Abort sorting operation if user clicked on "Stop"
            if not sorting.is_set(): break

            array[i].color = WHITE
            array[j].color = WHITE

            i -= 1
            j -= 1

        # Highlight the two elements being compared
        array[index].color = RED
        array[index+1].color = RED
        time.sleep(scan_speed[0])
        array[index].color = WHITE
        array[index+1].color = WHITE
        
        index += 1
        
    lock.release()
    sorting.clear()
    playing.clear()
    return
