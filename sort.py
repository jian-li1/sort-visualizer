import time
from settings import *

# Bubble Sort
def bubble_sort(array: list, size: int, swap_index: dict, scan_speed: list) -> None:
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
            array[j+1].color = WHITE

            j += 1
        i += 1

    sorting.clear()
    playing.clear()
    selected['alg'] = None
    selected['function'] = None
    return

# Selection Sort
def selection_sort(array: list, size: int, swap_index: dict, scan_speed: list) -> None:
    i = 0
    min_index = i

    while i < size and sorting.is_set():
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
            if array[j].num < array[min_index].num:
                array[min_index].color = WHITE
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
    sorting.clear()
    playing.clear()
    selected['alg'] = None
    selected['function'] = None
    return

# Insertion Sort
def insertion_sort(array: list, size: int, swap_index: dict, scan_speed: list) -> None:
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
        
    sorting.clear()
    playing.clear()
    selected['alg'] = None
    selected['function'] = None
    return

# Quick Sort
def quick_sort(array: list, end: int, swap_index: dict, scan_speed: list, start: int=0) -> None:
    # Abort sorting operation if user clicked on "Stop"
    if not sorting.is_set(): return
    # Base case
    if end <= start: return

    # Set the length and height of the pivot line
    quick_sort_line['start'] = (array[start].x, array[start].y)
    quick_sort_line['end'] = (array[end - 1].x, array[end - 1].y)
    
    # Gray out the other rectangles that arent being compared in the current stack
    for rect in array:
        rect.border = HOVER
        rect.text_color = HOVER

    for i in range(start, end):
        array[i].border = BLACK
        array[i].text_color = BLACK

    pivot = partition(array, start, end - 1, swap_index, scan_speed)

    # Pause if requested by user
    playing.wait()

    quick_sort(array, start=start, end=pivot, swap_index=swap_index, scan_speed=scan_speed)
    quick_sort(array, start=pivot + 1, end=end, swap_index=swap_index, scan_speed=scan_speed)
    
    if end - start == len(array):
        # Reset all the rectangle's colors
        for rect in array:
            rect.border = BLACK
            rect.text_color = BLACK
        sorting.clear()
        playing.clear()
        selected['alg'] = None
        selected['function'] = None
        return

# Helper function for quick sort
def partition(array: list, start: int, end: int, swap_index: dict, scan_speed: list) -> int:
    # Set j as start and i as the element before start
    j = start
    i = start - 1

    # Highlight the rectangle that is set as pivot
    array[end].color = RED
    
    while j < end + 1 and sorting.is_set():
        # Hightlight elements being compared
        if i >= start: array[i].color = RED
        array[j].color = RED

        time.sleep(scan_speed[0])
        if array[j].num < array[end].num:
            if i >= start: array[i].color = WHITE
            i += 1
            array[i].color = RED
            if i != j: time.sleep(scan_speed[0])

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

        array[j].color = WHITE
        j += 1

    array[i].color = WHITE
    i += 1
    array[end].color = RED

    # Store the two rectangles' index and positions
    swap_index['rect1'] = i
    swap_index['rect2'] = end
    swap_index['rect1_pos'] = array[i].x
    swap_index['rect2_pos'] = array[end].x

    # Begin swapping process on the GUI
    if sorting.is_set(): 
        swapping.set()
        while swapping.is_set():
            time.sleep(0.01)
        # Swap elements
        array[i], array[end] = array[end], array[i]

    array[i].color = WHITE
    array[end].color = WHITE
    return i
