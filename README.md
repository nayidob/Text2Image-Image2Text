# Text2Image
 
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
the aspect ratio. 


File: Image2Text.py
----------------
This program takes an image that has been previously modified
by the program Text2Image and extracts the text that contains.
In order to extract the tex the user must load the image and
enter the password generated by Text2Image. Then the decryption
process starts, getting the real value and finding the ASCII
character that corresponds.
The final text is prompted in the Scrolled Text object and the
user is able to save the text as a .txt with a button.

ENJOY!!

by Jonathan Nayid Orozco for Code in Place, Stanford, May 2020
