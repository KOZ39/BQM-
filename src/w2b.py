import os
import subprocess
import shutil

import acbpy

PRESET = b'\xff\xff' + b'\x00' * 166 + b'\xf9\xcf'

WELROD_SIZE = os.path.getsize('Welrod.acb.bytes')
BRENMK_SIZE = os.path.getsize('BrenMK.acb.bytes')

shutil.copy2('Welrod.acb.bytes', 'SonicAudioTools/Welrod.acb')

subprocess.call(['SonicAudioTools/AcbEditor.exe', 'SonicAudioTools/Welrod.acb'])

with open('BrenMK.acb.bytes', 'rb') as f:
    for i in acbpy.parse_binary(f):
        if i.track.cue_id < 14:   
            with open(f'SonicAudioTools/Welrod/{str(i.track.cue_id).zfill(5)}.{i.extension}', 'wb') as s:
                s.write(i.binary.read())
        else:
            with open(f'SonicAudioTools/Welrod/{str(i.track.cue_id+1).zfill(5)}.{i.extension}', 'wb') as s:
                s.write(i.binary.read())

with open('SonicAudioTools/Welrod/00014.hca', 'rb+') as f:
    data = f.read()
    f.seek(0)
    f.write(data[:96] + (PRESET * int((WELROD_SIZE - BRENMK_SIZE) / len(PRESET)))[:-256])

subprocess.call(['SonicAudioTools/AcbEditor.exe', 'SonicAudioTools/Welrod'])

shutil.copy2('SonicAudioTools/Welrod.acb', 'SonicAudioTools/Welrod.acb.bytes')
