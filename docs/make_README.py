import fileinput
import os
from shutil import copyfile

there = os.path.dirname(os.path.realpath(__file__))

src = "readme.rst"
dst = "../README.rst"
copyfile(src, dst)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()

for line in fileinput.input(dst, inplace=1):
    splitted = line.rstrip().split('.. include:: ')
    if len(splitted) == 2:
        line = read_file(os.path.join(there, splitted[1]))
        print line
    else:
        print line.rstrip()
