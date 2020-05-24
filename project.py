import tkinter as tk
import time
import random
from PIL import ImageTk
from PIL import Image

canvas_width = 200
canvas_height = 300
COLOR = "black"
ARROW_FILE = 'arrow.png'

def paint(event):
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    # color = random.choice(['blue', 'salmon', 'red', 'green', 'orange', 'plum'])
    canvas.create_oval(x1, y1, x2, y2, fill=COLOR, outline="")


def show_arrow(canvas):
    image = ImageTk.PhotoImage(Image.open("arrow.png"))
    canvas.create_image(300, 300, anchor="nw", image=image)
    canvas.create_image(0, 0, anchor="nw", image=image)
    root.update()

condition=True
print('Hello, world')
root = tk.Tk()
root.title("Painting using Ovals")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
show_arrow(canvas)


while condition:
    root.bind("<B1-Motion>", paint)
    root.update_idletasks()
    root.update()

#root.mainloop()