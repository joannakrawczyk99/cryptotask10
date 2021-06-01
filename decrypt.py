import cv2
from tkinter import Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np

image_display_size = 500, 350


def decrypt():
    # load the image and convert it into a numpy array
    load = Image.open("C:/Users/Aśka/PycharmProjects/medical-mask-3.png")
    load.thumbnail(image_display_size, Image.ANTIALIAS)
    load = np.asarray(load)
    load = Image.fromarray(np.uint8(load))
    render = ImageTk.PhotoImage(load)
    img = Label(app, image=render)
    img.image = render
    img.place(x=120, y=90)

    # Algorithm to decrypt the data from the image
    img = cv2.imread("C:/Users/Aśka/PycharmProjects/medical-mask-3.png")
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    decrypted_message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data)+1)/8)):
        decrypted_message.append(data[i*8:(i*8+8)])
    # join all the letters to form the message.
    decrypted_message = [chr(int(''.join(i), 2)) for i in decrypted_message]
    decrypted_message = ''.join(decrypted_message)
    message = Label(app, text=decrypted_message, bg='pink', font=("Times New Roman", 10))
    message.place(x=10, y=10)

# Defined the TKinter object app with background lavender, title Decrypt, and app size 600*600 pixels.
app = Tk()
app.configure(background='pink')
app.title("Decoding")
app.geometry('650x400')
# Add the button to call the function decrypt.
main_button = Button(app, text="Start decoding!", bg='black', fg='white', command=decrypt)
main_button.place(x=280, y=300)
app.mainloop()