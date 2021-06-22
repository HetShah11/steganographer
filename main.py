import numpy as np
from PIL import Image

def encode(src, message, dest):
    '''
    :param src: source path of the image file
    :param message: message to be encrypted
    :param dest: destination of encrypted file
    :return: none
    '''
    # opening the image for reading
    img = Image.open(src, 'r')
    width, height = img.size
    data_arr = np.array(list(img.getdata()))
    # checking mode of img if its RGB or RGBA
    # n is the no. of bytes in a pixel
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # calculating total_pixels
    total_pixels = len(data_arr)//n

    # adding a delimiter to show end of message
    message += '$t3g0'
    # converting message to binary
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    # checking the required pixels are available or not
    if req_pixels < total_pixels:
        print("Error message cannot be steganographed due to size constraints!")
        return
    else:
        index = 0
        # iterating over the image pixels
        for pix in range(total_pixels):
            # iterating over the color bytes (R, G, B) of each pixel
            for byte in range(3):
                if req_pixels > index:
                    # editing the last bit with b_message
                    data_arr[pix][byte] = int(bin(data_arr[pix][byte])[2:9] + b_message[index], 2)
                    index += 1
        # reshaping the new data
        en_data = data_arr.reshape(height, width, n)
        # creating new image from en_data
        en_img = Image.fromarray(en_data.astype('uint8'), mode=img.mode)
        en_img.save(dest)
        print("Image Encoded Successfully")

def Decode(src):
    '''
    :param src: source path of file to be decrypted
    :return: decrypted message
    '''
    # opening the image for reading
    img = Image.open(src, 'r')
    width, height = img.size
    data_arr = np.array(list(img.getdata()))
    # checking mode of img if its RGB or RGBA
    # n is the no. of bytes in a pixel
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # calculating total_pixels
    total_pixels = len(data_arr) // n

    message = ""
    b_message = []
    # iterating over the image pixels
    for pix in range(total_pixels):
        # iterating over the color bytes (R, G, B) of each pixel
        for byte in range(3):
            b_message.append(bin(data_arr[pix][byte])[2:][-1])

    # making groups of 8
    b_message = [b_message[i:i + 8] for i in range(0, len(b_message), 8)]
    # converting it into ASCII again
    for i in range(len(b_message)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(b_message[i], 2))
    # checking the presence of delimiter
    if "$t3g0" in message:
        print("Successfully Decrypted \nThe Message is - ", message[:-5])
    else:
        print("No Hidden Message Found")