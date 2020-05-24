"""
File: pyramid.py
----------------
YOUR DESCRIPTION HERE
"""

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
    # animation loop
    canvas.rowconfigure(5, minsize=50, weight=1)
    canvas.columnconfigure(4, minsize=50, weight=1)

    tkinter.Message(canvas, text="Welcome to the Text2Image Cryptographer"
                                 "\n --------------------------",
                    width=600, font="Calibri 24 bold",
                    justify=tkinter.CENTER).grid(row=0, column=1, sticky="new")
    tkinter.Message(canvas, text="\n"
                                 "\n"
                                 "\n>>> This program hides a long text within an image <<<"
                                 "\n"
                                 "\nTo do that we kindly ask you to select a .txt file"
                                 " and then upload the image you want to use"
                                 "\n(select files with buttons)", width=200, font="Calibri 12",
                    justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")
    tkinter.Label(canvas, text="Scroll down to see your full text...",
                  fg="blue").grid(row=0, column=1, sticky="sw")
    txt_edit = st.ScrolledText(canvas, font=("Calibri", 15))
    image_text = ImageTk.PhotoImage(Image.open("no_image_selected.png"))
    tkinter.Label(canvas, text="^^ Loaded Image ^^", fg="blue").grid(row=3, column=0, sticky="sew")
    image_label = tkinter.Label(canvas, image=image_text)

    image_text2 = ImageTk.PhotoImage(Image.open("encrypt_footer.png"))
    image_label2 = tkinter.Label(canvas, image=image_text2)
    image_label2.grid(row=5, column=0, sticky="ew", columnspan=4)

    format_buttons = tkinter.Frame(canvas, relief=tkinter.RAISED, bd=2)
    button_open = tkinter.Button(format_buttons, text="Open Text",
                                 command=lambda: open_file(filename_text_image, txt_edit))
    button_load = tkinter.Button(format_buttons, text="Load Image",
                                 command=lambda: load_image(filename_text_image, image_label))
    button_encrypt = tkinter.Button(canvas, text="Click"
                                                 "\n to"
                                                 "\n ENCRYPT"
                                                 , fg="red", font="Calibri 12 bold",
                                    command=lambda: encrypt(filename_text_image, objects_info))
    button_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    button_load.grid(row=2, column=0, sticky="ew", padx=5)
    button_encrypt.grid(row=5, column=4, sticky="nsew", padx=10, pady=10)

    format_buttons.grid(row=1, column=0, sticky="n")
    txt_edit.grid(row=1, column=1, sticky="nsew", rowspan=4, columnspan=4)
    image_label.grid(row=3, column=0, sticky="ew")
    canvas.update()
    canvas.mainloop()


def show_result(filename_text_image, objects_info):
    canvas_image = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT // 2, 'Resulting Image')
    image_filename = (filename_text_image["image"])
    tkinter.Message(canvas_image, text="\n"
                                       "=================================="
                                       "\n"
                                       "\nThe dimensions of your original image"
                                       " in pixels are:"
                                       "\n"
                                       "\n Width %s pixels"
                                       "\n Height %s pixels" % (objects_info["width_original_image"],
                                                                objects_info["height_original_image"]),
                    width=300, justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")

    tkinter.Message(canvas_image, text="\n"
                                       "=================================="
                                       "\n"
                                       "\nThe dimensions of your resulting image"
                                       " in pixels are:"
                                       "\n"
                                       "\n Width %s pixels"
                                       "\n Height %s pixels" % (objects_info["size"][0],
                                                                objects_info["size"][1]),
                    width=300, justify=tkinter.CENTER).grid(row=1, column=0, sticky="ew")

    #original_image2 = ImageTk.PhotoImage(Image.open(image_filename))
    #image_label = tkinter.Label(canvas_image, image=original_image2)
    #image_label.grid(row=0, column=1, sticky="ew", columnspan=2)

    modified_image = ImageTk.PhotoImage(Image.open("Encrypted_Image_Text.png"))
    image_label2 = tkinter.Label(canvas_image, image=modified_image)
    image_label2.grid(row=1, column=1, sticky="ew", columnspan=2)


    canvas_image.update()
    canvas_image.mainloop()


def exit_func():
    quit()


def load_and_prepare_image(filename_text_image, objects_info):
    image = Image.open(filename_text_image["image"]).convert("RGBA")
    objects_info["width_original_image"], objects_info["height_original_image"] = image.size
    original_aspect_ratio = objects_info["height_original_image"] / objects_info["width_original_image"]
    print(original_aspect_ratio)
    objects_info["size"] = get_size(objects_info["length"], original_aspect_ratio)
    print(objects_info["size"])
    final_image = image.resize((objects_info["size"][0], objects_info["size"][1]))
    return final_image


def encrypt(filename_text_image, objects_info):
    show_text_summary(filename_text_image, objects_info)
    final_image = load_and_prepare_image(filename_text_image, objects_info)
    final_image = put_text_within_image(objects_info["main_string"], final_image, objects_info["size"])
    final_image.save("Encrypted_Image_Text.png")
    print(filename_text_image["image"])


def show_text_summary(filename_text_image, string_info):
    canvas_text = make_canvas(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 4, 'Information About Text File')
    text_filename = (filename_text_image["text"])

    count_words(text_filename, canvas_text)
    string_info["main_string"] = create_string_from_file(text_filename)

    string_info["length"] = count_char(text_filename, string_info["main_string"], canvas_text)
    frequency_of_20_top_words(text_filename, canvas_text)

    button_show = tkinter.Button(canvas_text, text="Click to"
                                                   "\n Show Result"
                                                   , fg="red", font="Calibri 12 bold",
                                 command=lambda: show_result(filename_text_image, string_info))
    button_show.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)


def open_file(filename_text_image, txt_edit):
    """Open a file for editing."""
    filename = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filename:
        return
    txt_edit.delete(1.0, tkinter.END)
    with open(filename, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tkinter.END, text)
    filename_text_image["text"] = filename


def load_image(filename_text_image, image_label):
    """Open a file for editing."""
    filename = askopenfilename(
        filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpeg"), ("Image Files", "*.jpg"), ("All Files", "*.*")]
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

"""------
-----------------------
---------"""

def delete_punctuation(s):
    """
    Removes punctuation characters from a string and returns the
    resulting string (without punctuation).
    >>> delete_punctuation('REMOVE --the-- punctuation!!!!')
    'REMOVE the punctuation'
    """
    result = ''
    for char in s:
        # Check char is not a punctuation mark
        if char not in PUNCTUATION:
            result += char          # append non-punctuation characters

    return result


def get_counts_dict(filename):
    """
    Reads file and returns a dictionary with the words in the file
    and the number of occurrences of each word.
    """
    counts = {}                             # create empty dictionary

    with open(filename, 'r') as file:       # open file for reading
        for line in file:
            words = delete_punctuation(line).split()
            for word in words:
                word = word.lower()
                if word.isalpha():
                    if word not in en_stops:
                        if word not in counts:
                            counts[word] = 1
                        else:
                            counts[word] += 1

    return counts


def create_string_from_file(text_filename):
    count = 0
    text_file = ""
    with open(text_filename, 'r') as file:   # Open file to read
        for line in file:
            for char in line:
                text_file += char
                count += 1
    return text_file

def frequency_of_20_top_words(text_filename, canvas_text):
    dict_words = get_counts_dict(text_filename)
    s = sorted(dict_words.items(), key=operator.itemgetter(1), reverse=True)
    tkinter.Message(canvas_text, text="\n"
                                      "=================================="
                                      "\n"
                                      "\nThese are the TOP 20 words in the text"
                                      " and their frequency: ('word', freq)"
                                      "\n"
                                      "\n %s" % s[0:20], width=300,
                    justify=tkinter.CENTER).grid(row=3, column=0, sticky="ew")
    print(s[0:20])


def count_char(text_filename, main_string, canvas_text):
    char_count = len(main_string)
    tkinter.Message(canvas_text, text="%s characters" % char_count,
                    width=200, fg="blue", font="Calibri 16 bold",
                    justify=tkinter.CENTER).grid(row=2, column=0, sticky="ew")
    print(text_filename + " contains " + str(char_count) + " characters")
    return char_count


def count_words(filename, canvas_text):
    """
    Counts the total number of words in the given file and
    print it out.
    """
    count = 0
    with open(filename, 'r') as file:   # Open file to read
        for line in file:
            line = line.strip()         # Remove newline
            word_list = line.split()    # Create list of words
            for word in word_list:      # Print words
                count += 1
    tkinter.Message(canvas_text, text="The text selected: "
                                      "\n %s"
                                      "\n contains:" % filename,
                    width=200, font="Calibri 14 bold",
                    justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")
    tkinter.Message(canvas_text, text="%s words" % count,
                    width=200, fg="blue", font="Calibri 16 bold",
                    justify=tkinter.CENTER).grid(row=1, column=0, sticky="ew")
    print(filename + " contains " + str(count) + " words")


def put_text_within_image(main_string, final_image, size):
    count = 0
    width, height = final_image.size
    pixels = final_image.load()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = pixels[x, y]
            if count < (size[2]*size[2]):
                char_number = get_char(main_string, count)
                pixels[x, y] = (red, green, blue, 255 - char_number)
            else:
                pixels[x, y] = (red, green, blue, 255 - 32)
            count += 1
    # Return the modified canvas
    return final_image


def get_char(original, count):
    if ord(original[count]):
        char_number = ord(original[count])
    else:
        char_number = 255
    return char_number


def get_size(length, original_aspect_ratio):
    size = []
    sqr_len = math.sqrt(length)
    n = math.sqrt(length/original_aspect_ratio)
    m = define_m(n, original_aspect_ratio)
    size = [int(n), m, sqr_len]
    return size


def define_m(n, original_aspect_ratio):
    m = int(n * original_aspect_ratio)
    if n == m:
        return int(n)
    else:
        return int(m + original_aspect_ratio) + 1


if __name__ == '__main__':
    main()
