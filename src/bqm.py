import os
import sys

import acbpy

PRESET = b'\xff\xff' + b'\x00' * 166 + b'\xf9\xcf'

del sys.argv[0]

if len(sys.argv) > 0:
    for argv in sys.argv:
        if os.path.isfile(argv):
            hcaList = []

            with open(argv, 'rb') as f:
                for i in acbpy.parse_binary(f):
                    hcaList.append(i.binary.read())

            with open(argv, 'rb+') as f:
                data = f.read()

                for hca in hcaList:
                    data = data.replace(hca, hca[:96] + PRESET * int(len(hca) / len(PRESET)))

                f.seek(0)
                f.write(data)
