from tkinter import *
import subprocess
import codecs
from time import sleep
from sys import argv

disk_list = []
disks = argv[-1]

for i in disks:
    disk_list.append(i)

usb_for_eject = []

root = Tk()
root.attributes("-topmost", True)
root.lift()

# Create Frame
frame = Frame(root)
frame.pack(side=TOP, fill=BOTH, expand=YES)

screen_width = frame.master.winfo_screenwidth()
screen_height = frame.master.winfo_screenheight()
w = screen_width * 0.6
h = screen_height * 0.4

# Center the window
x = (screen_width / 2) - (w / 2)
y = (screen_height / 2) - (h / 2)
frame.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Adjust frame properties
frame.master.overrideredirect(True)  # Set no border or title
frame.config(bg="#fff")

# Create text label
font_size = 30
text = "Выберите флешку:"

label = Label(frame, text=text, wraplength=screen_width * 0.8)
label.pack(side=TOP, expand=YES)
label.config(bg="#fff", justify=CENTER, font=("calibri", font_size))

# Set transparency
root.wait_visibility(root)  # Needed for linux (and must come after overrideredirect)
root.attributes('-alpha', 0.8)


def destroy_window(event):
    root.destroy()


def get_disk_name(event):
    if list_box.get(ANCHOR):
        global usb_for_eject
        usb_for_eject.clear()
        usb_for_eject.append(list_box.get(ANCHOR))
        root.destroy()


root.bind('<Alt-q>', destroy_window)

list_box = Listbox(width=(int(screen_width * 0.5)), height=(int(screen_height * 0.5)))

for el in disk_list:
    list_box.insert(0, el)

list_box.pack()
list_box.focus_set()

list_box.bind('<space>', get_disk_name)

root.mainloop()
subprocess.run(['python', 'eject.py', f'{usb_for_eject[0]}'], shell=True)
