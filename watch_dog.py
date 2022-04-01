import subprocess
from keyboard import add_hotkey, wait
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


open_window_hotkey = config['openWindowHotkey']
disk_list = []
label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def open_window(disk_list):
    subprocess.run(['python', 'open_window.py', f'{disk_list}'], shell=True)


def check_usb():
    for i in label:
        try:
            open(i + ':/', 'r')
        except Exception as e:
            # error = 2  =>not found
            # error = 13 =>permission denied (exist!)
            if e.errno == 13 and i not in ['C', 'D']:
                disk_list.append(i)

    str_disk_list = ''.join(disk_list)
    open_window(str_disk_list)
    disk_list.clear()


def main():
    add_hotkey(open_window_hotkey, check_usb)
    wait()


if __name__ == '__main__':
    main()
