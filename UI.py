from tkinter import *
from tkinter import ttk, filedialog
import time
import os
import subprocess
import encoder, decoder


def code():
    path = get_path()
    subprocess.run(['explorer.exe', '/select,', os.path.normpath(path)])
    time.sleep(1)
    encoder.init(path)
    root.destroy()


def un_code():
    path = get_path()
    subprocess.run(['explorer.exe', '/select,', os.path.normpath(path)])
    time.sleep(1)
    text = decoder.init(path)
    new_file = path + '.txt'
    file = open(new_file, 'x', encoding='UTF8')
    file.write(text)
    file.close()
    root.destroy()


def get_path():
    files = filedialog.askopenfilenames()[0]
    return files


root = Tk(className=' Encoder Decoder')

root.configure(bg='white')

button_encode = Button(text='Encode', fg='white', bg='red', font=120, height=10, width=20, command=lambda: code())
button_decode = Button(text='Decode', fg='white', bg='blue', font=120, height=10, width=20, command=lambda: un_code())

button_encode.grid(row=0, column=0, stick='w')
button_decode.grid(row=0, column=2, stick='w')

root.grid_columnconfigure(1, minsize=1)


root.mainloop()