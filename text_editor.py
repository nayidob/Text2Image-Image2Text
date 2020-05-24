import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

window = tk.Tk()
window.title("Simple Text Editor")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
sb = tk.Scrollbar(txt_edit, orient='vertical')
sb.pack(side='right', fill='y')
# canvas.pack(side='left', fill=fill, expand='yes')
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")



window.mainloop()


"""import os
from tkinter import *

HEIGHT = 32
WIDTH = 80

root = Tk()
root.title("Text editor")

def onlist():
    onclear()
    file_list = '\n'.join(os.listdir())
    textarea.insert('@0,0', file_list)

def onread():
    onclear()
    try:
        fobj = open(txtFile.get(), "r")
        textarea.insert("@0,0", fobj.read())
        fobj.close()
        textarea["fg"] = "#000"
    except IOError:
        textarea.insert("@0,0", "Error: Can't read file\n")
        textarea["fg"] = "#f00"

def onwrite():
    try:
        fobj = open(txtFile.get(), "w")
        fobj.write(textarea.get("@0,0", END))
        fobj.close()
        textarea["fg"] = "#000"
    except IOError as e:
        textarea.insert("@0,0", "Error: Can't write file\n")
        textarea["fg"] = "#ff722b"

def onclear():
    textarea.delete("@0,0", END)

btnList = Button(root, text = "List", command = onlist)
btnList.grid(row = 0, column = 0)
btnRead = Button(root, text = "Read", command = onread)
btnRead.grid(row = 0, column = 1)
btnWrite = Button(root, text = "Write", command = onwrite)
btnWrite.grid(row = 0, column = 2)
btnClear = Button(root, text = "Clear", command = onclear)
btnClear.grid(row = 0, column = 3)
txtFile = Entry(root, width = WIDTH)
txtFile.grid(row = 1, column = 0, columnspan = 4)

textarea = Text(root, width = WIDTH, height = HEIGHT)
textarea.grid(row = 2, column = 0, columnspan = 4)

root.mainloop()"""