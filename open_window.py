from tkinter import *
import subprocess
from sys import argv
from pygame import mixer
from watch_dog import config

disk_list = list(argv[-1])
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
font_size = config['ui']['fontSize']
text = "Select USB drive and double spacebar:"

label = Label(frame, text=text, wraplength=screen_width * 0.5)
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


root.bind('<Escape>', destroy_window)

list_box = Listbox(width=int(screen_width * 0.3), height=int(screen_height * 0.5), font=("calibri", font_size))

for el in disk_list:
    list_box.insert(0, el)

list_box.pack()
list_box.focus_set()
list_box.bind('<space>', get_disk_name)

root.mainloop()

if usb_for_eject:
    with open('tmp.ps1', 'w') as tpm_ps:
        tpm_ps.write("$driveEject = New-Object -comObject Shell.Application\n"
                     f'$driveEject.Namespace(17).ParseName("{usb_for_eject[0]}:").InvokeVerb("Eject")')

    process = subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', './tmp.ps1'])
    if process.returncode == 0:
        mixer.init()
        mixer.music.load('eject_sound.wav')
        mixer.music.play(loops=1)
