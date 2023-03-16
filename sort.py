import time
from typing import Union
from settings import *

def terminate() -> None:
    status['sorting'] = False
    status['playing'].clear()
    selected['alg'] = None
    selected['function'] = None
    selected['text'] = ''

def swap(array: list, rect1: int, rect2: int) -> None:
    # Store the two rectangles' index and positions
    swap_rect['rect1'] = rect1
    swap_rect['rect2'] = rect2
    swap_rect['rect1_pos'] = array[rect1].x
    swap_rect['rect2_pos'] = array[rect2].x

    # Begin swapping process on the GUI
    if status['sorting']: 
        status['swapping'] = True
        while status['swapping']:
            time.sleep(0.01)

        # Swap elements
        array[rect1], array[rect2] = array[rect2], array[rect1]

# Bubble Sort
def bubble_sort(array: list, size: int) -> None:
    i = 0
    while i < size - 1 and status['sorting']:
        j = 0
        while j < size - i - 1 and status['sorting']:
            # Highlight the two elements being compared
            array[j].color = RED
            array[j+1].color = RED

            time.sleep(Speed.delay)

            if array[j].num > array[j+1].num:
                # Swap elements
                swap(array, j, j + 1)

            # Pause if requested by user
            status['playing'].wait()
            # Abort sorting operation if user clicked on "Stop"
            if not status['sorting']: break

            array[j].color = WHITE
            array[j+1].color = WHITE

            j += 1
        i += 1

    terminate()
    return

# Selection Sort
def selection_sort(array: list, size: int) -> None:
    i = 0
    min_index = i

    while i < size and status['sorting']:
        min_index = i

        # Pause if requested by user
        status['playing'].wait()
        # Abort sorting operation if user clicked on "Stop"
        if not status['sorting']: break

        # Highlight the rectangle with the minimum value 
        if status['sorting']: array[min_index].color = RED

        time.sleep(Speed.delay)

        j = i + 1
        while j < size and status['sorting']:
            # Highlight the rectangle being scanned
            array[j].color = RED

            
            # Pause if requested by user
            status['playing'].wait()
            # Abort sorting operation if user clicked on "Stop"
            if not status['sorting']: break
            
            time.sleep(Speed.delay)

            # Update current value to minimum value if current value if smaller than current minimum value
            if array[j].num < array[min_index].num:
                array[min_index].color = WHITE
                min_index = j
            else:
                array[j].color = WHITE

            j += 1

        # Swap elements
        swap(array, i, min_index)

        array[i].color = WHITE
        array[min_index].color = WHITE

        i += 1

    array[min_index].color = WHITE
    terminate()
    return

# Insertion Sort
def insertion_sort(array: list, size: int) -> None:
    index = 1
    while index < size and status['sorting']:
        i = index
        j = i - 1

        # Pause if requested by user
        status['playing'].wait()
        # Abort sorting operation if user clicked on "Stop"
        if not status['sorting']: break

        while array[i].num < array[j].num and j >= 0 and status['sorting']:
            # Highlight the two elements being compared
            array[i].color = RED
            array[j].color = RED

            time.sleep(Speed.delay)
            
            # Swap elements
            swap(array, j, i)
            
            # Pause if requested by user
            status['playing'].wait()
            # Abort sorting operation if user clicked on "Stop"
            if not status['sorting']: break

            array[i].color = WHITE
            array[j].color = WHITE

            i -= 1
            j -= 1

        # Highlight the two elements being compared
        array[index].color = RED
        array[index-1].color = RED
        time.sleep(Speed.delay)
        array[index].color = WHITE
        array[index-1].color = WHITE
        
        index += 1
        
    terminate()
    return

# Quick Sort
def quick_sort(array: list, end: int, start: int=0) -> None:
    # Abort sorting operation if user clicked on "Stop"
    if not status['sorting']: return
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

    pivot = partition(array, start, end - 1)

    # Pause if requested by user
    status['playing'].wait()

    quick_sort(array, start=start, end=pivot)
    quick_sort(array, start=pivot + 1, end=end)
    
    if end - start == len(array):
        # Reset all the rectangle's colors
        for rect in array:
            rect.border = BLACK
            rect.text_color = BLACK
        terminate()
        return

# Helper function for quick sort
def partition(array: list, start: int, end: int) -> int:
    # Set j as start and i as the element before start
    j = start
    i = start - 1

    # Highlight the rectangle that is set as pivot
    array[end].color = RED
    
    while j < end + 1 and status['sorting']:
        # Hightlight elements being compared
        if i >= start: array[i].color = RED
        array[j].color = RED

        time.sleep(Speed.delay)
        if array[j].num < array[end].num:
            if i >= start: array[i].color = WHITE
            i += 1
            array[i].color = RED
            if i != j: time.sleep(Speed.delay)

            # Swap elements
            swap(array, i, j)
            
        # Pause if requested by user
        status['playing'].wait()
        # Abort sorting operation if user clicked on "Stop"
        if not status['sorting']: break

        array[j].color = WHITE
        j += 1

    array[i].color = WHITE
    i += 1
    array[end].color = RED

    # Swap elements
    swap(array, i, end)

    array[i].color = WHITE
    array[end].color = WHITE
    return i

# Merge Sort
def merge_sort(array: list, end: int, start: int=0) -> None:
    # Move rectangles up from initial call stack
    if end - start == len(array):
        shift_rectangles()

    # Abort sorting operation if user clicked on "Stop"
    if not status['sorting']:
        # Move rectangles down
        shift_rectangles()
        terminate()
        return

    # Pause if requested by user
    status['playing'].wait()

    # Gray out the other rectangles that arent being compared in the current stack
    for rect in array:
        rect.border = HOVER
        rect.text_color = HOVER

    for i in range(start, end):
        array[i].border = BLACK
        array[i].text_color = BLACK

    time.sleep(Speed.delay * 2)

    # Base case
    if end - start == 1: return
    
    # Determine midpoint
    mid = (start + end) // 2

    merge_sort(array, start=start, end=mid)
    merge_sort(array, start=mid, end=end)

    merge(array, start, mid, end)

    # Pause if requested by user
    status['playing'].wait()

    # Terminate sorting operation from initial call stack 
    if end - start == len(array):
        status['sorting'] = False
        # Move rectangles down
        shift_rectangles()

        terminate()
        return

def merge(array, start, mid, end):

    # Create a temporary array for storing sorted subarray
    temp = []
    i, j = start, mid
    start_pos = array[start].x
    
    # Highlight rectangles in subarray
    for k in range(start, end):
        array[k].border = BLACK
        array[k].text_color = BLACK
    
    # Abort sorting operation if user clicked on "Stop"
    if not status['sorting']: return
    
    time.sleep(Speed.delay * 2)

    while i < mid and j < end:
        # Pause if requested by user
        status['playing'].wait()

        if array[i].num < array[j].num:
            # Sort subarray
            sort_subarray_gui(array, i, start_pos + (RECT_WIDTH + RECT_SPACING) * (len(temp)))
            temp.append(array[i])
            i += 1
        else:
            # Sort subarray
            sort_subarray_gui(array, j, start_pos + (RECT_WIDTH + RECT_SPACING) * (len(temp)))
            temp.append(array[j])
            j += 1
        
    while i < mid:
        # Pause if requested by user
        status['playing'].wait()
        # Sort subarray
        sort_subarray_gui(array, i, start_pos + (RECT_WIDTH + RECT_SPACING) * len(temp))
        temp.append(array[i])
        i += 1

    while j < end:
        # Pause if requested by user
        status['playing'].wait()
        # Sort subarray
        sort_subarray_gui(array, j, start_pos + (RECT_WIDTH + RECT_SPACING) * len(temp))    
        temp.append(array[j])
        j += 1

    # Pause if requested by user
    status['playing'].wait()

    # Merge rectangles
    for k in range(end - start):
        array[start + k] = temp[k]
    merge_subarray_gui(start, end)

def shift_rectangles() -> None:
    status['moving'] = True
    while status['moving']:
        time.sleep(0.01)

def sort_subarray_gui(array: list, index: int, stopping_pos: Union[int, float]) -> None:
    # Store the rectangle's index and position
    sub_sort['rect'] = index
    sub_sort['rect_x_pos'] = array[index].x
    # Store the rectangle's stopping position
    sub_sort['rect_pos_dest'] = stopping_pos

    # Begin subarray sorting process on the GUI
    status['sub_sorting'] = True
    while status['sub_sorting']:
        time.sleep(0.01)

def merge_subarray_gui(start: int, end: int) -> None:
    # Begin merging process on the GUI
    merge_rect[0], merge_rect[1] = start, end
    status['merging'] = True
    while status['merging']:
        time.sleep(0.01)
