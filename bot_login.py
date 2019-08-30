import praw
import os
from log_it import log_it

def bot_login():
    log_it("Startup...")
    try:
        r = praw.Reddit('1882bot', user_agent="1882-Bot")
    except:
        log_it("Failed to log in!")
    return r
