"""
File: pyramid.py
----------------
YOUR DESCRIPTION HERE
"""
import pathlib
import tkinter
import math
import operator
import random
from PIL import ImageTk
from PIL import Image
from nltk.corpus import stopwords
import tkinter.scrolledtext as st
from tkinter.filedialog import askopenfilename, asksaveasfilename


CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600     # Height of drawing canvas in pixels
PUNCTUATION = '.!?,-:;""'
MAX_COLOR = 255
MIN_COLOR = 0
en_stops = set(stopwords.words('english'))


def main():
    filename_text_image = {}
    objects_info = {}
    set_environment(filename_text_image, objects_info)


def set_environment(filename_text_image, objects_info):
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Secret Image')
    canvas.rowconfigure(5, minsize=50, weight=1)
    canvas.columnconfigure(4, minsize=50, weight=1)

    objects_info["show"] = True

    tkinter.Message(canvas, text="Welcome to the Image2Text Decrypter"
                                 "\n --------------------------",
                    width=600, font="Calibri 24 bold",
                    justify=tkinter.CENTER).grid(row=0, column=1, sticky="new")
    tkinter.Message(canvas, text="\n"
                                 "\n"
                                 "\n>>> This program extracts text from an image <<<"
                                 "\n"
                                 "\nTo do that, we kindly ask you to select the image file"
                                 " using the button, you can save the decrypted text"
                                 " as a .txt file afterwards"
                                 "\n ", width=200, font="Calibri 12",
                    justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")
    tkinter.Label(canvas, text="Scroll down to see your full text...",
                  fg="blue").grid(row=1, column=2, sticky="se")
    txt_edit = st.ScrolledText(canvas, font=("Calibri", 15))
    image_text = ImageTk.PhotoImage(Image.open("dat/no_image_selected.png"))
    tkinter.Label(canvas, text="^^ Loaded Image ^^", fg="blue").grid(row=3, column=0, sticky="sew")
    image_label = tkinter.Label(canvas, image=image_text)

    image_text2 = ImageTk.PhotoImage(Image.open("dat/encrypt_footer.png"))
    image_label2 = tkinter.Label(canvas, image=image_text2)
    image_label2.grid(row=5, column=0, sticky="ew", columnspan=4)

    format_buttons = tkinter.Frame(canvas, relief=tkinter.RAISED, bd=2)
    button_load = tkinter.Button(format_buttons, text="Load Image",
                                 command=lambda: load_image(filename_text_image, image_label))
    button_save = tkinter.Button(format_buttons, text="Save Text",
                                 command=lambda: save_file(objects_info))
    button_decrypt = tkinter.Button(canvas, text="Click to DECRYPT"
                                                 , fg="red", font="Calibri 12 bold",
                                    command=lambda: decrypt(filename_text_image, txt_edit, objects_info))
    button_load.grid(row=1, column=0, sticky="ew", padx=5)
    button_save.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    button_decrypt.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    format_buttons.grid(row=1, column=0, sticky="n")
    txt_edit.grid(row=2, column=1, sticky="nsew", rowspan=3, columnspan=4)
    image_label.grid(row=3, column=0, sticky="ew")


    while objects_info["show"]:
        canvas.update()


def decrypt(filename_text_image, text_edit, objects_info):
    filename = filename_text_image["image"]
    original = Image.open(filename).convert("RGBA")
    objects_info["text"] = get_text(original)
    show_text(text_edit, objects_info["text"])


def get_text(image):
    count = 0
    text = ""
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = pixels[x, y]
            value = int(255 - alpha)
            text += chr(value)
            count += 1
    return text


def show_text(txt_edit, text):
    txt_edit.insert(tkinter.END, text)


def save_file(objects_info):
    text_file = open("Decrypted_Text.txt", "w+")
    text_file.write(objects_info["text"])
    text_file.close()
    objects_info["show"] = False
    show_confirmation()

def show_confirmation():
    top = tkinter.Toplevel()
    top.title('Decryption done!')
    canvas_text = tkinter.Canvas(top, width=CANVAS_WIDTH // 2, height=CANVAS_HEIGHT // 2)
    canvas_text.pack()

    decrypt_image = Image.open("dat/unlocked.png")
    decrypt_image = ImageTk.PhotoImage(decrypt_image)
    image_label = tkinter.Label(canvas_text, image=decrypt_image, justify=tkinter.CENTER)
    image_label.grid(row=0, column=0, sticky="nsew")

    tkinter.Message(canvas_text, text="\n"
                                      "** Your image has been decrypted"
                                      "\nThe extracted text is in the root directory:"
                                      "\n%s/Decrypted_Text.png"
                                      % (pathlib.Path().absolute()),
                    width=200, justify=tkinter.CENTER).grid(row=1, column=0, sticky="ew", columnspan=2)

    button_exit = tkinter.Button(canvas_text, text="Click to Exit",
                                 fg="red", font="Calibri 12 bold", command=lambda: exit())
    button_exit.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
    canvas_text.update()
    canvas_text.mainloop()


def load_image(filename_text_image, image_label):
    """Open a file for editing."""
    filename = askopenfilename(
        filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpeg"),
                   ("Image Files", "*.jpg"), ("All Files", "*.*")]
    )
    if not filename:
        return
    new_image = Image.open(filename)
    width_image, height_image = new_image.size
    original_aspect_ratio = height_image / width_image
    new_image = new_image.resize((200, int(200 * original_aspect_ratio)))
    new_image = ImageTk.PhotoImage(new_image)
    image_label.configure(image=new_image)
    image_label.image = new_image
    filename_text_image["image"] = filename


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
