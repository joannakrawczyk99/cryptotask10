from PIL import Image

import key
import monoalphabetic_encryption
import monoalphabetic_decryption


def convertData(img):
    """
    Converting encoding data into binary values using ascii characters.
    :param data: encoding data
    :return: binary values
    """
    dataset = []
    for i in img:
        dataset.append(format(ord(i), '08b'))
    return dataset

def modifyPixel(pix, data):
    """
    Extrating pixels and modyfing them.
    :param pix: pixels
    :param data: 8-bit binary data
    """
    datalist = convertData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def putPixel(new_image, message_to_encode):
    """
    Putting modified pixels into the new image.
    :param new_image: new image
    :param message_to_encode: message that will be encoded
    """
    w = new_image.size[0]
    (x, y) = (0, 0)
    for pix in modifyPixel(new_image.getdata(), message_to_encode):
        new_image.putpixel((x, y), pix)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encode(encryption=None):
    """
    Encoding data into an image.
    """

    key_to_encrypt = {'a': 'q', 'b': 'v', 'c': 'x', 'd': 'z', 'e': 'y', 'f': 'w', 'g': 'u', 'h': 't', 'i': 's',
                      'j': 'r',
                      'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l', 'p': 'k', 'r': 'j', 's': 'i', 't': 'h',
                      'u': 'g', 'w': 'f',
                      'y': 'e', 'z': 'd', 'x': 'c', 'v': 'b', 'q': 'a',
                      'A': 'Q', 'B': 'V', 'C': 'X', 'D': 'Z', 'E': 'Y', 'F': 'W', 'G': 'U', 'H': 'T', 'I': 'S',
                      'J': 'R', 'K': 'P',
                      'L': 'O', 'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'R': 'J', 'S': 'I', 'T': 'H', 'U': 'G',
                      'W': 'F', 'Y': 'E',
                      'Z': 'D', 'X': 'C', 'V': 'B', 'Q': 'S',
                      '1': '5', '2': '9', '3': '8', '4': '7', '5': '6', '6': '4', '7': '3', '8': '2', '9': '1',
                      '.': ',', ',': '.', ':': ';', ';': ':', '?': '!', '!': '?', '-': '_', '_': '-', '(': ')',
                      ')': '(',
                      '%': '$', '$': '%', ' ': '&', '&': ' ', '+': '*', '*': '+'}
    entered_image = input("Image name with extension: ")
    img = Image.open(entered_image, 'r')

    message = input("Message that you want to be encoded: ")
    if (len(message) == 0):
        raise ValueError('Empty message!')

    e1 = monoalphabetic_encryption.Encryption(key_to_encrypt, message)
    encrypted_message = e1.encrypt()

    new_image = img.copy()
    putPixel(new_image, encrypted_message)

    new_image_name = input("New image name with extension: ")
    new_image.save(new_image_name, str(new_image_name.split(".")[1].upper()))

def decode(decryption=None):
    """
    Decoding data from the image.
    :return: decoded message
    """

    key_to_encrypt = {'a': 'q', 'b': 'v', 'c': 'x', 'd': 'z', 'e': 'y', 'f': 'w', 'g': 'u', 'h': 't', 'i': 's',
                      'j': 'r',
                      'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l', 'p': 'k', 'r': 'j', 's': 'i', 't': 'h',
                      'u': 'g', 'w': 'f',
                      'y': 'e', 'z': 'd', 'x': 'c', 'v': 'b', 'q': 'a',
                      'A': 'Q', 'B': 'V', 'C': 'X', 'D': 'Z', 'E': 'Y', 'F': 'W', 'G': 'U', 'H': 'T', 'I': 'S',
                      'J': 'R', 'K': 'P',
                      'L': 'O', 'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'R': 'J', 'S': 'I', 'T': 'H', 'U': 'G',
                      'W': 'F', 'Y': 'E',
                      'Z': 'D', 'X': 'C', 'V': 'B', 'Q': 'S',
                      '1': '5', '2': '9', '3': '8', '4': '7', '5': '6', '6': '4', '7': '3', '8': '2', '9': '1',
                      '.': ',', ',': '.', ':': ';', ';': ':', '?': '!', '!': '?', '-': '_', '_': '-', '(': ')',
                      ')': '(',
                      '%': '$', '$': '%', ' ': '&', '&': ' ', '+': '*', '*': '+'}

    k1 = key.Key(key_to_encrypt)
    reversed_key = k1.createReverseKey()

    entered_image = input("Image name with extension: ")
    img = Image.open(entered_image, 'r')

    decoded_message = ''
    data_from_image = iter(img.getdata())

    while (True):
        pixels = [value for value in data_from_image.__next__()[:3] +
                  data_from_image.__next__()[:3] +
                  data_from_image.__next__()[:3]]

        binary = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binary += '0'
            else:
                binary += '1'

        decoded_message += chr(int(binary, 2))
        d1 = monoalphabetic_decryption.Decryption(reversed_key, decoded_message)
        message = d1.decrypt()
        if (pixels[-1] % 2 != 0):
            return message

def main():
    a = int(input("What do you want to do?\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
    elif (a == 2):
        print("Decoded message:  " + decode())
    else:
        raise Exception("Wrong input! :(")

if __name__ == '__main__':
    main()