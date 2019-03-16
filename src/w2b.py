import os
import subprocess
import shutil
import sys

import acbpy

PRESET = b'\xff\xff' + b'\x00' * 166 + b'\xf9\xcf'

WELROD_SIZE = os.path.getsize('Welrod.acb.bytes')
BRENMK_SIZE = os.path.getsize('BrenMK.acb.bytes')

MEIPASS = getattr(sys, '_MEIPASS') if hasattr(sys, '_MEIPASS') else '.'

shutil.copy2('Welrod.acb.bytes', f'{MEIPASS}/SonicAudioTools/Welrod.acb')

subprocess.call([f'{MEIPASS}/SonicAudioTools/AcbEditor.exe', f'{MEIPASS}/SonicAudioTools/Welrod.acb'])

with open('BrenMK.acb.bytes', 'rb') as f:
    for i in acbpy.parse_binary(f):
        if i.track.cue_id < 14:
            with open(f'{MEIPASS}/SonicAudioTools/Welrod/{str(i.track.cue_id).zfill(5)}.{i.extension}', 'wb') as s:
                s.write(i.binary.read())
        else:
            with open(f'{MEIPASS}/SonicAudioTools/Welrod/{str(i.track.cue_id+1).zfill(5)}.{i.extension}', 'wb') as s:
                s.write(i.binary.read())

with open(f'{MEIPASS}/SonicAudioTools/Welrod/00014.hca', 'rb+') as f:
    data = f.read()
    f.seek(0)
    f.write(data[:96] + (PRESET * int((WELROD_SIZE - BRENMK_SIZE) / len(PRESET)))[:-256])

subprocess.call([f'{MEIPASS}/SonicAudioTools/AcbEditor.exe', f'{MEIPASS}/SonicAudioTools/Welrod'])

shutil.copy2(f'{MEIPASS}/SonicAudioTools/Welrod.acb', f'{os.getcwd()}/Welrod (1).acb.bytes')