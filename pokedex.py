#functions tied to help menu
import os
import pathlib

fileDir = pathlib.Path(__file__).parent.resolve()
dirSplit = str(fileDir).split(os.path.split(fileDir)[1])[0][-1]

def readme():
    os.startfile(str(fileDir)+dirSplit+'readme.pdf')

def contribute():
    os.startfile(str(fileDir)+dirSplit+'contribute.pdf')