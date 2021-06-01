from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math

global file_opened

display_size = 300, 300


def on_click():
    global file_opened

    file_opened = filedialog.askopenfilename()  # opening file using dialog box
    load_image = Image.open(file_opened)  # loading image using the path

    load_image.thumbnail(display_size, Image.ANTIALIAS)

    np_image = np.asarray(load_image)  # loading image as numpy array for efficient computation
    np_image = Image.fromarray(np.uint8(np_image))
    render = ImageTk.PhotoImage(np_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=20, y=50)


def encrypt():
    global file_opened

    data = txt.get(1.0, "end-1c")

    image = cv2.imread(file_opened)  # loading picture
    data = [format(ord(i), '08b') for i in data]  # represented in ascii
    _, width, _ = image.shape

    PixReq = len(data) * 3  # encoding image

    RowReq = PixReq / width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    for i in range(RowReq + 1):
        while (count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            for index_k, k in enumerate(char):
                if ((k == '1' and image[i][count][index_k % 3] % 2 == 0) or (
                        k == '0' and image[i][count][index_k % 3] % 2 == 1)):
                    image[i][count][index_k % 3] -= 1
                if (index_k % 3 == 2):
                    count += 1
                if (index_k == 7):
                    if (charCount * 3 < PixReq and image[i][count][2] % 2 == 1):
                        image[i][count][2] -= 1
                    if (charCount * 3 >= PixReq and image[i][count][2] % 2 == 0):
                        image[i][count][2] -= 1
                    count += 1
        count = 0

    cv2.imwrite("C:/Users/Aśka/PycharmProjects/encrypted_image.png", image)  # save encrypted image into a file

    message = Label(app, text="Successful!",
                          bg='pink', font=("Times New Roman", 10))
    message.place(x=160, y=300)


app = Tk()  # defining tkinter object
app.configure(background='pink')
app.title("Encoding")
app.geometry('650x400')
on_click_button = Button(app, text="Choose picture", bg='gray', fg='white', command=on_click)  # calling function on_click
on_click_button.place(x=100, y=140)

txt = Text(app, wrap=WORD, width=30)  # text box
txt.place(x=340, y=55, height=165)

encrypt_button = Button(app, text="Start encoding!", bg='black', fg='white', command=encrypt)
encrypt_button.place(x=280, y=300)
app.mainloop()