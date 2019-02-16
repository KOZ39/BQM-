import os
import sys

import acbpy

PRESET = b'\xff\xff' + b'\x00' * 166 + b'\xf9\xcf'
HCA_LIST = []

del sys.argv[0]

if len(sys.argv) > 0:
    for argv in sys.argv:
        if os.path.isfile(argv):
            with open(argv, 'rb') as f:
                for i in acbpy.parse_binary(f):
                    HCA_LIST.append(i.binary.read())

            with open(argv, 'rb+') as f:
                data = f.read()

                for hca in HCA_LIST:
                    data = data.replace(hca, hca[:96] + PRESET * int(len(hca) / len(PRESET)))

                f.seek()
                f.write(data)
