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
import tkinter.scrolledtext as st

ARROW_FILE = 'arrow.png'
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600     # Height of drawing canvas in pixels
SQUARE_SIZE = 70
BUTTON_OFFSET = 100
BUTTON_MARGIN = 300
BUTTON_HEIGHT = 100
FONT_SIZE = 60


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Move Square')
    # make the rectangle...
    start_y = CANVAS_HEIGHT / 2 - SQUARE_SIZE / 2
    end_y = start_y + SQUARE_SIZE
    rect = canvas.create_rectangle(0, start_y, SQUARE_SIZE, end_y, fill='black')
    image = ImageTk.PhotoImage(Image.open("arrow.png"))
    canvas.create_image(300, 300, anchor="nw", image=image)
    btn_num_list = [3, 4, 5]
    btn_list = []
    for i in range(3):
        btn_num = btn_num_list[i]
        btn = tkinter.Button(canvas, text=btn_num, fg='black', font=("Calibri", FONT_SIZE),
                             command=lambda: check_num(canvas, btn_num))
        canvas.create_window(BUTTON_MARGIN + BUTTON_OFFSET * i, BUTTON_HEIGHT, window=btn)
        btn_list.append(btn)
    # pause
    canvas.update()
    time.sleep(1/100000.)  # parameter is seconds to pause.

    rect = canvas.create_rectangle(300, 300, 400, 400, fill='yellow')
    canvas.update()
    tkinter.Label(canvas, text="Preview Your Text File", font=("Calibri", 15),
                  background='green', foreground="white").grid(column=0, row=0)
    text_area = st.ScrolledText(canvas, width=80, height=10, font=("Calibri", 15))
    text_area.grid(column=0, pady=10, padx=10)
    # Inserting Text which is read only
    text_area.insert(tkinter.INSERT,
                     """\ 
                     This is a scrolledtext widget to make tkinter text read only. 
                     Hi 
                     Geeks !!! 
                     Geeks !!! 
                     Geeks !!!  
                     Geeks !!! 
                     Geeks !!! 
                     Geeks !!! 
                     Geeks !!! 
                     """)

    # Making the text read only
    text_area.configure(state='disabled')
    # animation loop
    canvas.update()
    canvas.mainloop()

def show_arrow(canvas):
    image = ImageTk.PhotoImage(Image.open("arrow.png"))
    canvas.create_image(300, 300, anchor="nw", image=image)
    # pause
    time.sleep(10)  # parameter is seconds to pause.
    rect = canvas.create_rectangle(300, 400, 300, 400, fill='white')
    canvas.update()


def is_past_middle(canvas, rect):
    max_x = CANVAS_WIDTH / 2 - SQUARE_SIZE / 2
    curr_x = get_left_x(canvas, rect)
    return curr_x > max_x

######## These helper methods use "lists" ###########
### Which is a concept you will learn Monday ###########

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
