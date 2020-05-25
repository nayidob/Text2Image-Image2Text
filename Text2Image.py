"""
File: Text2Image.py
----------------
This program takes a .txt file provided by the user and
embedded it in any image the user wants. The program takes care
of the type of image as well as it size. Depending on the size of
the text the image is resized. At the end it will save a .png file
in the root directory.
Then the user can use the Image2Text file to load and decrypt the
image and get back the original text.
The program works with small text but its great benefit comes from
large documents. In the folder /Resources you will find 4 different
examples of text, including The Bible (which can be embedded in a
2000 pixels image)
It is important to note, that I provide example images but you are
free to choose the one you prefer. The program will take care of
the aspect ratio. ENJOY!!

by Jonathan Nayid Orozco for Code in Place, Stanford, May 2020
"""
# Importing Libraries
import math
import random
import pathlib
import tkinter
import operator
from PIL import Image
from PIL import ImageTk
import tkinter.scrolledtext as st
from tkinter.filedialog import askopenfilename

# Defining Constants
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600     # Height of drawing canvas in pixels
PUNCTUATION = '.!?,-:;""'
MAX_COLOR = 255
MIN_COLOR = 0
MIN_NUM = 100000
MAX_NUM = 999999
# English Language Stop Words
en_stops = ['whom', 'out', 'ain', 'any', 'will', 'between', 'had', "shouldn't", 'was', "you'll", 'nor', 'now', 'it',
            'those', "hadn't", 'shan', 'me', 'which', 'not', "won't", 'can', 'd', 'most', 'a', 'be', 'as', 'we', 'do',
            'their', 'further', 'ours', 'ourselves', 'about', 'during', "don't", 'some', 'through', 'only', 'isn',
            'while', 'have', 'very', 'that', 'our', 'did', 'until', 'should', 'because', 'where', 'he', 'or', 'so',
            'and', 'the', "it's", "shan't", 'll', 'down', 'when', 'you', 'on', 'she', 'm', "aren't", "wasn't", 'an',
            'here', 'there', 'all', 've', 'by', 'hasn', 'herself', 'shouldn', 'in', 'been', 'into', 'this', 'don', 't',
            'than', "wouldn't", "you've", "isn't", 'yourselves', 'him', 'if', "you'd", 'then', 'y', 'itself', 'other',
            'hers', 'is', 'my', 'why', 'myself', 'over', 'aren', 'needn', 'what', "she's", 'both', 's', "that'll",
            'below', "didn't", 'themselves', "needn't", 'weren', 'for', 'has', 'mightn', "weren't", "couldn't", 'too',
            'o', 'himself', 'against', 'under', 'doing', 'ma', 'am', 'again', 'having', 'once', 'off', 'from', 'above',
            'i', 'to', 'these', 'mustn', 'how', 'they', 'your', "mustn't", 'being', 'after', 'haven', 'wouldn',
            "haven't", 'before', 'just', 'at', 'of', 'does', 'were', "mightn't", 'yours', 'won', 'own', 'no', 'are',
            'her', 'them', 'more', "you're", 'theirs', 'up', 'such', 'doesn', 're', 'yourself', 'but', 'few', 'hadn',
            "hasn't", 'with', 'wasn', 'his', "doesn't", "should've", 'same', 'didn', 'who', 'couldn', 'its', 'each']


def main():
    # Define main dictionaries to keep useful info through the code
    filename_text_image = {}
    objects_info = {}
    # Set environment - analyze text and encrypt the text into the image
    set_environment(filename_text_image, objects_info)
    # Show the result, comparing final image with the original one
    show_result(filename_text_image, objects_info)


def set_environment(filename_text_image, objects_info):
    """
    Creates the initial view (Messages, Buttons, Frames, Scroll Text, Footer Image)
    :param filename_text_image: Dictionary used to keep information about text file
    and image provided by the user
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    """
    # Creates the main canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Secret Image')
    canvas.rowconfigure(5, minsize=50, weight=1)
    canvas.columnconfigure(4, minsize=50, weight=1)
    # Define a boolean to keep showing this canvas until a button is clicked
    objects_info["show"] = True
    # Welcome and summary Messages
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
    # Scrolled Text to show the full text loaded
    tkinter.Label(canvas, text="Scroll down to see your full text...",
                  fg="blue").grid(row=0, column=1, sticky="sw")
    txt_edit = st.ScrolledText(canvas, font=("Calibri", 15))
    # No Image Selected yet
    image_text = ImageTk.PhotoImage(Image.open("dat/no_image_selected.png"))
    tkinter.Label(canvas, text="^^ Loaded Image ^^", fg="blue").grid(row=3, column=0, sticky="sew")
    image_label = tkinter.Label(canvas, image=image_text)
    # Footer
    image_text2 = ImageTk.PhotoImage(Image.open("dat/encrypt_footer.png"))
    image_label2 = tkinter.Label(canvas, image=image_text2)
    image_label2.grid(row=5, column=0, sticky="ew", columnspan=4)
    # Buttons to Open the .txt file and Load the Image by the user
    format_buttons = tkinter.Frame(canvas, relief=tkinter.RAISED, bd=2)
    # Open button calls out the function open_file()
    button_open = tkinter.Button(format_buttons, text="Open Text",
                                 command=lambda: open_file(filename_text_image, txt_edit))
    # Load button calls out the function load_image()
    button_load = tkinter.Button(format_buttons, text="Load Image",
                                 command=lambda: load_image(filename_text_image, image_label))
    # Encrypt button calls out the function encrypt()
    button_encrypt = tkinter.Button(canvas, text="Click"
                                                 "\n to"
                                                 "\n ENCRYPT",
                                    fg="red", font="Calibri 12 bold",
                                    command=lambda: encrypt(filename_text_image, objects_info))
    # Positioning of Objects in the canvas
    button_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    button_load.grid(row=2, column=0, sticky="ew", padx=5)
    button_encrypt.grid(row=5, column=4, sticky="nsew", padx=10, pady=10)
    format_buttons.grid(row=1, column=0, sticky="n")
    txt_edit.grid(row=1, column=1, sticky="nsew", rowspan=4, columnspan=4)
    image_label.grid(row=3, column=0, sticky="ew")
    # Validation to update canvas until a button is clicked (Information saved in objects_info dict)
    while objects_info["show"]:
        canvas.update()


def open_file(filename_text_image, txt_edit):
    """
    The function receives the file extension of the .txt file and loads it in the
    scrolled text object. Finally, it adds the file extension to the dictionary
    filename_text_image.
    :param filename_text_image: Dictionary used to keep information about text file
    and image provided by the user
    :param txt_edit: Scrolled Text object
    """
    """Open a file for editing."""
    filename = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filename:
        return
    txt_edit.delete(1.0, tkinter.END)
    with open(filename, "r") as input_file:
        text = input_file.read()
        # Loads the text in the Scrolled Text object
        txt_edit.insert(tkinter.END, text)
    filename_text_image["text"] = filename


def load_image(filename_text_image, image_label):
    """
    The function opens the image that the user wants to load, it will only allow
    .png/.jpg/.jpeg files.
    :param filename_text_image: Dictionary used to keep information about text file
    and image provided by the user
    :param image_label: Receives the Label from the main canvas and load the image on it.
    """
    filename = askopenfilename(
        filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpeg"),
                   ("Image Files", "*.jpg"), ("All Files", "*.*")]
    )
    if not filename:
        return
    new_image = Image.open(filename)
    width_image, height_image = new_image.size
    original_aspect_ratio = height_image / width_image
    # Cause the image could be large, it is resized to show a thumbnail in the main canvas
    new_image = new_image.resize((200, int(200 * original_aspect_ratio)))
    new_image = ImageTk.PhotoImage(new_image)
    # Loads the image in the Label
    image_label.configure(image=new_image)
    image_label.image = new_image
    filename_text_image["image"] = filename


def encrypt(filename_text_image, objects_info):
    """
    This function creates a new canvas where the relevant information is shown. In
    addition, it will put the image in the text, using the alpha channel.
    Finally it puts a click-able button in the new canvas to show the final result
    :param filename_text_image: Dictionary used to keep information about text file
    and image provided by the user
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    """
    # Create new canvas
    canvas_text = show_text_summary(filename_text_image, objects_info)
    # Loads the original image and resized it according to the length of the text
    final_image = load_and_prepare_image(filename_text_image, objects_info)
    # Magic is done! Puts the text in the image
    final_image = put_text_within_image(objects_info["main_string"], final_image, objects_info["size"], objects_info)
    # Save the resulting encrypted image
    final_image.save("Encrypted_Image_Text.png")
    # Creates a Button to Show the Final Result, calls out show_button()
    button_show = tkinter.Button(canvas_text, text="Click to"
                                                   "\n Show Result",
                                 fg="red", font="Calibri 12 bold",
                                 command=lambda: show_button(objects_info))
    button_show.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)


def show_button(objects_info):
    """
    This function changes the value of the key 'show' in the dictionary to False in
    order to stop the update of the main canvas.
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    """
    objects_info["show"] = False


def show_text_summary(filename_text_image, objects_info):
    """
    This function creates a new canvas where relevant information about the text loaded
    is shown. File extension, number of words, number of characters and a list of the Top 20
    more frequent words avoiding the stop words of the english language.
    :param filename_text_image:Dictionary used to keep information about text file
    and image provided by the user
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    :return canvas_text: Returns the object canvas_text with the loaded information
    """
    # Create canvas
    canvas_text = make_canvas(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 4, 'Information About Text File')
    text_filename = (filename_text_image["text"])
    # Count the number of words
    count_words(text_filename, canvas_text)
    # Store in the dictionary a string with the whole text
    objects_info["main_string"] = create_string_from_file(text_filename)
    # Count the number of characters that will be relevant to resize the image
    objects_info["length"] = count_char(objects_info["main_string"], canvas_text)
    # Finds the Top 20 frequent words
    frequency_of_20_top_words(text_filename, canvas_text)
    return canvas_text


def load_and_prepare_image(filename_text_image, objects_info):
    """
    Resize the original image having the length of the full text and keeping
    the original aspect ratio.
    :param filename_text_image:Dictionary used to keep information about text file
    and image provided by the user
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    :return final_image: Returns the original image loaded by the user, with the
    required size to keep the text
    """
    # Converts the image file in order to enable the alpha channel
    image = Image.open(filename_text_image["image"]).convert("RGBA")
    objects_info["width_original_image"], objects_info["height_original_image"] = image.size
    # Determine the aspect ratio
    objects_info["original_aspect_ratio"] = \
        objects_info["height_original_image"] / objects_info["width_original_image"]
    objects_info["size"] = get_size(objects_info["length"], objects_info["original_aspect_ratio"])
    # Resize the image accordingly with the length of the text document and it aspect ratio
    final_image = image.resize((objects_info["size"][0], objects_info["size"][1]))
    return final_image


def put_text_within_image(main_string, final_image, size, objects_info):
    """
    This function embed the text within the image using the alpha channel
    :param main_string: string with ALL the characters of the .txt file
    :param final_image: image that has been resized to fit the whole text on it
    :param size: size of the image to be used in the nested for
    :return final_image: resulting image with the text on it (alpha channel affected)
    """
    count = 0
    width, height = final_image.size
    # Load pixels from image
    create_random(objects_info)
    pixels = final_image.load()
    for x in range(width):
        for y in range(height):
            # Assign the value of the specific pixel into the channels
            red, green, blue, alpha = pixels[x, y]
            if count < (size[2]*size[2]):
                # Gets the ASCII value of the nth character
                char_number = get_char(main_string, count)
                # Puts the ASCII value in the alpha channel.
                # It was necessary to do 255 - value in order to get a lighter image
                char_number = get_rand(char_number, objects_info)
                pixels[x, y] = (red, green, blue, char_number)
                #pixels[x, y] = (red, green, blue, 255 - char_number)
            else:
                # For the pixels that are redundant, meaning the ones left
                # after placing the whole text, will be filled with spaces
                char_number = get_rand(32, objects_info)
                pixels[x, y] = (red, green, blue, char_number)
            count += 1
    # Return the modified canvas
    return final_image


def create_random(objects_info):
    objects_info["rand_num"] = random.randint(MIN_NUM, MAX_NUM)


def get_rand(char_number, objects_info):
    rand_eq = char_number + objects_info["rand_num"]
    rand_eq = rand_eq % 256
    return rand_eq


def show_result(filename_text_image, objects_info):
    """
    This function creates a new canvas to show the final result. It previews both images
    the original one and the encrypted with the text inside. In addition, it presents
    relevant information about the size of each image in pixels as well as the final route
    of the created image.
    Includes some comments about decryption and a button to finish the program.
    :param filename_text_image:Dictionary used to keep information about text file
    and image provided by the user
    :param objects_info: Dictionary used to keep information about the objects
    (size, strings, etc.)
    """
    # Creates new canvas as Toplevel, tkinter was showing me error so I needed to create this one
    # differently, I mean, not using the make_canvas function. It seems that a tkinter instance over
    # the same class was not able to load.
    top = tkinter.Toplevel()
    top.title('Resulting Image')
    canvas_image = tkinter.Canvas(top, width=CANVAS_WIDTH + 1, height=CANVAS_HEIGHT // 2 + 1)
    canvas_image.pack()
    # Load the original image
    image_filename = (filename_text_image["image"])
    # Messages about both Images
    tkinter.Message(canvas_image, text="\n"
                                       "========================"
                                       "\n ORIGINAL IMAGE"
                                       "\nThe dimensions of "
                                       "your original image"
                                       "\n in pixels are:"
                                       "\n"
                                       "\n Width: %s pixels"
                                       "\n Height: %s pixels"
                                       "\n======================"
                                       % (objects_info["width_original_image"],
                                          objects_info["height_original_image"]),
                    width=300, justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")

    tkinter.Message(canvas_image, text="\n"
                                       "========================"
                                       "\n RESULTING IMAGE"
                                       "\nThis image contains your"
                                       "\nfull text."
                                       "\nThe dimensions of "
                                       "your resulting image"
                                       "\n in pixels are:"
                                       "\n"
                                       "\n Width: %s pixels"
                                       "\n Height: %s pixels"
                                       "\n======================="
                                       % (objects_info["size"][0], objects_info["size"][1]),
                    width=300, justify=tkinter.CENTER).grid(row=1, column=0, sticky="ew")
    # Open and resize the original image (200 px x 200*ratio px)
    original_image = Image.open(image_filename)
    original_image = original_image.resize((200, int(objects_info["original_aspect_ratio"] * 200)))
    original_image = ImageTk.PhotoImage(original_image)
    image_label = tkinter.Label(canvas_image, image=original_image)
    image_label.grid(row=0, column=1, sticky="ew", columnspan=2)
    # Open and resize the encrypted image (200 px x 200*ratio px)
    modified_image = Image.open("Encrypted_Image_Text.png")
    modified_image = modified_image.resize((200, int(objects_info["original_aspect_ratio"] * 200)))
    modified_image = ImageTk.PhotoImage(modified_image)
    image_label2 = tkinter.Label(canvas_image, image=modified_image)
    image_label2.grid(row=1, column=1, sticky="ew", columnspan=2)
    # Shows the path of the resulting image
    tkinter.Message(canvas_image, text="\n"
                                       "*** These images have been resized in"
                                       " order to fit the screen."
                                       "\nThe encrypted image is in the root directory:"
                                       "\n%s/Encrypted_Image_Text.png"
                                       % (pathlib.Path().absolute()),
                    width=600, justify=tkinter.LEFT).grid(row=3, column=0, sticky="w", columnspan=2)
    # Shows message about decryption process
    tkinter.Message(canvas_image, text="\n"
                                       "*** Use the Image2Text Program to Decrypt."
                                       "\n Enter this number: %s" % objects_info["rand_num"],
                    fg="blue", font="Calibri 15 bold",
                    width=600, justify=tkinter.LEFT).grid(row=4, column=0, sticky="w", columnspan=2)
    # Button to exit the whole program
    button_show = tkinter.Button(canvas_image, text="Click to"
                                                    "\n Exit",
                                 fg="red", font="Calibri 12 bold",
                                 command=lambda: exit())
    button_show.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)
    canvas_image.update()
    canvas_image.mainloop()


def make_canvas(width, height, title):
    """
    ORIGINAL function provided by Code in Place
    Creates and returns a drawing canvas
    of the given int size ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


def frequency_of_20_top_words(text_filename, canvas_text):
    """
    This function receives a string and calculates the frequency of each word,
    organize them from largest to smallest. Updates the canvas to show the results.
    :param text_filename: string with ALL the characters in the .txt file
    :param canvas_text: Canvas object where the Text Summary is shown
    """
    # Calculate the frequency of each word in the string
    dict_words = get_counts_dict(text_filename)
    # Sort the list from largest to smallest
    s = sorted(dict_words.items(), key=operator.itemgetter(1), reverse=True)
    tkinter.Message(canvas_text, text="\n"
                                      "=================================="
                                      "\n"
                                      "\nThese are the TOP 20 words in the text"
                                      " and their frequency: ('word', freq)"
                                      "\n"
                                      "\n %s" % s[0:20], width=300,
                    justify=tkinter.CENTER).grid(row=3, column=0, sticky="ew")


def get_counts_dict(filename):
    """
    Reads file and returns a dictionary with the words in the file
    and the number of occurrences of each word.
    """
    # Creates empty dictionary
    counts = {}
    # Open file for reading
    with open(filename, 'r') as file:
        for line in file:
            # Deletes punctuation
            words = delete_punctuation(line).split()
            for word in words:
                # Lower all the character
                word = word.lower()
                if word.isalpha():
                    # Take care of the stop words
                    if word not in en_stops:
                        if word not in counts:
                            counts[word] = 1
                        else:
                            counts[word] += 1
    return counts


def create_string_from_file(text_filename):
    """
    This function creates a string from a file
    :param text_filename: .txt file extension
    :return text_file: string with ALL the characters in the .txt file
    """
    count = 0
    text_file = ""
    # Open file to read
    with open(text_filename, 'r') as file:
        for line in file:
            for char in line:
                text_file += char
                count += 1
    return text_file


def delete_punctuation(s):
    """
    Function provided by Code in Place
    Removes punctuation characters from a string and returns the
    resulting string (without punctuation).
    >>> delete_punctuation('REMOVE --the-- punctuation!!!!')
    'REMOVE the punctuation'
    """
    result = ''
    for char in s:
        # Check char is not a punctuation mark
        if char not in PUNCTUATION:
            # append non-punctuation characters
            result += char

    return result


def count_char(main_string, canvas_text):
    """
    This function counts the number of characters in a given string
    :param main_string: string with ALL the characters in the .txt file
    :param canvas_text: Canvas object with the relevant information about the text
    :return char_count: number of characters in this string
    """
    char_count = len(main_string)
    # Add a message in the Canvas showing the number of characters
    tkinter.Message(canvas_text, text="%s characters" % char_count,
                    width=200, fg="blue", font="Calibri 16 bold",
                    justify=tkinter.CENTER).grid(row=2, column=0, sticky="ew")
    return char_count


def count_words(filename, canvas_text):
    """
    This function counts the total number of words in the given file and print it out
    on the canvas.
    :param filename: file name of the .txt. file
    :param canvas_text: Canvas object with the relevant information about the text
    """
    count = 0
    # Open file to read
    with open(filename, 'r') as file:
        for line in file:
            # Remove newline
            line = line.strip()
            # Create list of words
            word_list = line.split()
            # Print words
            for word in word_list:
                count += 1
    # Print number of words in the canvas
    tkinter.Message(canvas_text, text="The text selected: "
                                      "\n %s"
                                      "\n contains:" % filename,
                    width=200, font="Calibri 14 bold",
                    justify=tkinter.CENTER).grid(row=0, column=0, sticky="ew")
    tkinter.Message(canvas_text, text="%s words" % count,
                    width=200, fg="blue", font="Calibri 16 bold",
                    justify=tkinter.CENTER).grid(row=1, column=0, sticky="ew")


def get_char(original, count):
    """
    This function gets the ASCII equivalent of any character
    :param original: string with the ALL the characters of the text
    :param count: counter that moves along the text and the image (pixels)
    :return char_number: returns the ASCII equivalent
    """
    if ord(original[count]) < 255:
        char_number = ord(original[count])
    else:
        char_number = 255
    return char_number


def get_size(length, original_aspect_ratio):
    """
    This function calculates the size required for the new image
    :param length: length of the string containing ALL the characters
    :param original_aspect_ratio: aspect ratio of the original image
    :return size: returns a list with n and m and the root square of length
    """
    sqr_len = math.sqrt(length)
    n = math.sqrt(length/original_aspect_ratio)
    m = define_m(n, original_aspect_ratio)
    size = [int(n), m, sqr_len]
    return size


def define_m(n, original_aspect_ratio):
    """
    This function calculates the new height of the image having the width
    :param n: height of the new image
    :param original_aspect_ratio: original aspect ratio
    :return: returns the calculated height for the new image
    """
    m = int(n * original_aspect_ratio)
    if n == m:
        return int(n)
    else:
        return int(m + original_aspect_ratio) + 1


if __name__ == '__main__':
    main()
