import numpy as np
import cv2

DELIMITER = "$t3G4##"

def to_binary(data):
    """Convert `data` to binary format as string"""
    if type(data) == str:
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [ format(i, "08b") for i in data ]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        raise TypeError("Error in binary conversion!!")


def encode(image, plaintext):
    # read the image
    img = cv2.imread(image)
    # maximum bytes to encode
    n_bytes = img.shape[0] * img.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)
    if len(plaintext) > n_bytes:
        raise ValueError("Error!! Insufficient bytes, need bigger image or less data.")

    # stopping criteria
    plaintext += DELIMITER
    data_index = 0
    # convert data to binary
    binary_pt = to_binary(plaintext)
    # size of data to hide
    data_len = len(binary_pt)

    for row in img:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_binary(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # red pixel bit
                pixel[0] = int(r[:-1] + binary_pt[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # green pixel bit
                pixel[1] = int(g[:-1] + binary_pt[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # blue pixel bit
                pixel[2] = int(b[:-1] + binary_pt[data_index], 2)
                data_index += 1
            # if data is encoded
            if data_index >= data_len:
                break
    return img

def decode(image):
    print("[+] Decoding...")
    # read the image
    img = cv2.imread(image)
    decoded_message = ""
    for row in img:
        for pixel in row:
            r, g, b = to_binary(pixel)
            decoded_message += r[-1]
            decoded_message += g[-1]
            decoded_message += b[-1]

    # split by 8-bits
    all_bytes = [decoded_message[i: i + 8] for i in range(0, len(decoded_message), 8)]
    # convert from bits to characters
    pt = ""
    for byte in all_bytes:
        pt += chr(int(byte, 2))
        if pt[-5:] == DELIMITER:
            break
    return pt[:-5]


def encrypt():
    image_name = input("Enter image name(with extension): ")
    image = cv2.imread(image_name)

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Error...Data is empty!!')

    filename = input("Enter the name of new encoded image(with extension): ")
    encoded_image = encode(image,data)
    cv2.imwrite(filename, encoded_image)

def decrypt():
    image_name = input("Enter the name of the steganographed image that you want to decode (with extension) :")
    image = cv2.imread(image_name)  # read the image using cv2.imread()

    print("The Steganographed image is as shown below: ")
    text = decode(image)
    return text

def main():
    while True:
        print("\n#################################")
        choice = int(input("Welcome to Steganographer\n"
                           "MENU\n"
                           "1.Encode message in image\n"
                           "2.Decode image\n"
                           "3.Exit"
                           "\nEnter your choice: "))
        if choice == 1:
            print("\nEncoding....")
            encrypt()

        elif choice == 2:
            print("\nDecoding....")
            print("Decoded message is " + decode_text())
        else:
            return

if __name__ == "__main__":
    main()