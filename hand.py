import tkinter as tk
from time import sleep
import random


canvas_width = 500
canvas_height = 150


def main():
    x = 0
    canvas = make_canvas(canvas_width, canvas_height, "Draw")
    scan_mark(x, y)
    canvas.mainloop()

def draw_point(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    coordinates = [[x1, x2], [y1, y2]]
    # canvas.create_oval(x1, y1, x2, y2, fill="black")
    return coordinates

def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()

"""
canvas_width = 1000
canvas_height = 400
COLOR = "black"

def paint(event):
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    # color = random.choice(['blue', 'salmon', 'red', 'green', 'orange', 'plum'])
    canvas.create_oval(x1, y1, x2, y2, fill=COLOR, outline="")


root = tk.Tk()
root.title("Painting using Ovals")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
root.bind("<B1-Motion>", paint)

root.mainloop()
"""
"""
import tkinter as tk
from time import sleep

def myfunction(event):
    x, y = event.x, event.y
    x1 = (x+100)
    y1 = (y+100)
    canvas.create_line(x, y, x1, y1)
    sleep(0.5)
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
root.bind("<Motion>", myfunction)
root.mainloop()
"""