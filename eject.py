import subprocess
from sys import argv
from pygame import mixer

selected_usb = argv[-1]


def eject_usb(selected_usb):
    with open('tmp.ps1', 'w') as tpm_ps:
        tpm_ps.write("$driveEject = New-Object -comObject Shell.Application\n"
                     f'$driveEject.Namespace(17).ParseName("{selected_usb}:").InvokeVerb("Eject")')

    process = subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', './tmp.ps1'])
    if process.returncode == 0:
        mixer.init()
        mixer.music.load('eject_sound.wav')
        mixer.music.play(loops=1)


eject_usb(selected_usb)
