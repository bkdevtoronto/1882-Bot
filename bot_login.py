import praw
import os
import sys
from log_it import log_it
from config import config

def bot_login(logfile):
    try:
        r = praw.Reddit('mybot', user_agent=config["bot_username"])
    except:
        log_it(logfile, "Failed to log in!")
        return False
    return r
