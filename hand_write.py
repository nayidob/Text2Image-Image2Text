"""
File: pyramid.py
----------------
YOUR DESCRIPTION HERE
"""


import tkinter
import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk
from PIL import Image

canvas_width = 500
canvas_height = 150


def main():
    x1, x2, y1, y2 = 0, 0, 0, 0
    coordinates = [[x1, x2], [y1, y2]]
    print(coordinates)
    paint = False
    python_green = "#476042"
    canvas = make_canvas(canvas_width, canvas_height, "Draw")
    coordinates = canvas.bind("<Motion>", draw_point)
    print(coordinates)
    # canvas.bind("<Button>", mouse_pressed)
    """
    canvas = make_canvas(canvas_width, canvas_height, "Draw")
    mouse_x = canvas.winfo_pointerxy()
"""
    canvas.mainloop()

######## These helper methods use "lists" ###########
### Which is a concept you will learn Monday ###########

def draw_point(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    coordinates = [[x1, x2], [y1, y2]]
    # canvas.create_oval(x1, y1, x2, y2, fill="black")
    return coordinates

def mouse_moved(event):
    print('x = ' + str(event.x), 'y = ' + str(event.y))

def mouse_pressed(event, canvas):
    print('mouse pressed', event.x, event.y)
    x = event.x
    y = event.y
    found = canvas.find_overlapping(x, y, x, y)
    if len(found) > 0:
        canvas.delete(found[-1])

def get_left_x(canvas, shape):
    # returns the x location of the shape
    return canvas.coords(shape)[0]

def get_top_y(canvas, shape):
    # returns the y location of the shape
    return canvas.coords(shape)[1]


######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas




if __name__ == '__main__':
    main()
