import tkinter as tk
from tkinter import filedialog
from PIL import Image

def encode():
    input_image_path = filedialog.askopenfilename(title="Select Image")
    if not input_image_path:
        return
    image = Image.open(input_image_path)
    encoded_image = image.copy()
    message = message_entry.get()
    keyword = keyword_entry.get()

    if len(keyword) == 0:
        tk.messagebox.showerror("Error", "Please enter a keyword")
        return

    if len(message) == 0:
        tk.messagebox.showerror("Error", "Please enter a message")
        return

    pixel_list = list(encoded_image.getdata())
    encoded_pixel_list = []

    message = keyword + " " + message

    binary_message = ''.join(format(ord(char), '08b') for char in message)

    if len(binary_message) > len(pixel_list) * 3:
        tk.messagebox.showerror("Error", "Message is too large for the image")
        return

    message_index = 0

    for pixel in pixel_list:
        if message_index < len(binary_message):
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            red = red & 0xFE | int(binary_message[message_index])
            message_index += 1
            if message_index < len(binary_message):
                green = green & 0xFE | int(binary_message[message_index])
                message_index += 1
            if message_index < len(binary_message):
                blue = blue & 0xFE | int(binary_message[message_index])
                message_index += 1

            encoded_pixel_list.append((red, green, blue))
        else:
            encoded_pixel_list.append(pixel)

    encoded_image.putdata(encoded_pixel_list)
    save_path = filedialog.asksaveasfilename(title="Save Image As", filetypes=[("PNG files", "*.png")])
    if save_path:
        encoded_image.save(save_path)

    tk.messagebox.showinfo("Success", "Message encoded successfully")


def decode():
    input_image_path = filedialog.askopenfilename(title="Select Image")
    if not input_image_path:
        return
    image = Image.open(input_image_path)
    keyword = keyword_entry.get()

    if len(keyword) == 0:
        tk.messagebox.showerror("Error", "Please enter a keyword")
        return

    pixel_list = list(image.getdata())

    extracted_binary_message = ""

    for pixel in pixel_list:
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]

        extracted_binary_message += str(red & 1)
        extracted_binary_message += str(green & 1)
        extracted_binary_message += str(blue & 1)

    extracted_message = ""
    binary_chunks = [extracted_binary_message[i:i + 8] for i in range(0, len(extracted_binary_message), 8)]

    for binary_chunk in binary_chunks:
        if binary_chunk == "00000000":
            break
        extracted_message += chr(int(binary_chunk, 2))

    keyword_length = len(keyword)
    extracted_keyword = extracted_message[:keyword_length]

    if extracted_keyword != keyword:
        tk.messagebox.showerror("Error", "Incorrect keyword")
        return

    extracted_message = extracted_message[keyword_length + 1:]

    tk.messagebox.showinfo("Decoded Message", extracted_message)


root = tk.Tk()
root.title("Steganography")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

message_label = tk.Label(frame, text="Message:")
message_label.grid(row=0, column=0, sticky="w")

message_entry = tk.Entry(frame)
message_entry.grid(row=0, column=1, padx=5, pady=5)

keyword_label = tk.Label(frame, text="Keyword:")
keyword_label.grid(row=1, column=0, sticky="w")

keyword_entry = tk.Entry(frame)
keyword_entry.grid(row=1, column=1, padx=5, pady=5)

encode_button = tk.Button(frame, text="Encode", command=encode)
encode_button.grid(row=2, column=0, columnspan=2, pady=10)

decode_button = tk.Button(frame, text="Decode", command=decode)
decode_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
