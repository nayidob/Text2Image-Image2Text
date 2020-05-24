# a few examples
import math
import operator
import random
from simpleimage import SimpleImage
import nltk
from nltk.corpus import stopwords
from PIL import Image


BIBLE = "bible.txt"
FULL_TEXT = "The_Little_Prince"
TEXT = "The_Little.txt"
PUNCTUATION = '.!?,-:;""'
MAX_COLOR = 255
MIN_COLOR = 0

en_stops = set(stopwords.words('english'))

def main():
    text_filename = (FULL_TEXT+".txt")
    count_words(text_filename)
    main_string = create_string_from_file(text_filename)
    length = count_char(text_filename, main_string)
    image = Image.open(FULL_TEXT + ".jpeg").convert("RGBA")
    width_original_image, height_original_image = image.size
    original_aspect_ratio = height_original_image / width_original_image
    print(original_aspect_ratio)
    size = get_size(length, original_aspect_ratio)
    print(size)
    final_image = image.resize((size[0], size[1]))
    final_image = draw_text(main_string, final_image, size)
    final_image.save("Test.png")
    final_image.show()
    dict_words = get_counts_dict(text_filename)
    s = sorted(dict_words.items(), key=operator.itemgetter(1), reverse=True)
    print(s[0:20])


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


def count_char(text_filename, main_string):
    char_count = len(main_string)
    print(text_filename + " contains " + str(char_count) + " characters")
    return char_count

def count_words(filename):
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
    print(filename + " contains " + str(count) + " words")


def draw_text(main_string, final_image, size):
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