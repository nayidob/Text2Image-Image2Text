# a few examples
import math
from simpleimage import SimpleImage
from PIL import Image


def main():
    filename = "prov.png"
    original = Image.open(filename).convert("RGBA")
    original.show()
    text = get_text(original)
    print(text)


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


if __name__ == '__main__':
    main()