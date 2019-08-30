import praw
import os
import logging
from time import gmtime, strftime

logging.basicConfig(filename="1882.log", filemode="a", level=logging.INFO)

def log_it(s):
    o = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT > " + s
    logging.info(o)
    print(o)
