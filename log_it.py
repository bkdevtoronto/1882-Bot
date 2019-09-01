import praw
import os
import logging
from time import gmtime, strftime

fileName="1882" # Set your filename here

def tooBig(name):
    if os.path.exists(name) is True:
        return os.path.getsize(name) > 1024 * 512
    else :
        return False

def getFileName():
    i=1
    while tooBig(fileName+"_"+(str(i).zfill(3))+".log"):
        i += 1

    return fileName+"_"+(str(i).zfill(3))+".log"

# Exported functions
def log_it(logfile, s):
    f = open(logfile,"a+")
    o = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT > " + str(s)
    f.write(o + "\n")
    f.close()
    print(o)
