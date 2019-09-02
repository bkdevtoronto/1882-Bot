# Dependencies
import praw
import sys
import time
from datetime import datetime, timedelta

from config import config
from bot_login import bot_login
from log_it import log_it, getFileName

import flair
import mentions

# Get logfile for this session
logfile=getFileName()

# Get the posts and stuff
def get_posts(r):
    try:
        for submission in r.subreddit(config["sub_name"]).new(limit=30):
            if submission.link_flair_text is None and config["moderate_flair"] is True:
                comment = submission.reply("**Please flair your post!**\n\n" + config["flair_submission_reply"] + "\n\nOnce you've flaired your post, [send **" + config["bot_name"] + "** a message by clicking here.](https://www.reddit.com/message/compose/?to=" + config["bot_username"] + "&message=Post%20has%20been%20flaired!&subject=Flaired:%20" + submission.id + "). *Don\'t change the subject line so that **" + config["bot_name"] + "** knows what to do!*")
                comment.mod.distinguish(sticky=True)
                submission.mod.remove()
                log_it(logfile, "\tAlerted no-flair on https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
    except Exception as e:
        log_it(logfile, e)



# Check messages for updated posts
def check_messages(r):
    try:
        # Only select unread messages
        for message in r.inbox.unread(limit=None):
            # Flair
            subject = message.subject.split()
            if config["moderate_flair"] is True and subject[0] == "Flaired:":
                flair.messages_flair(r, message, logfile)

        if config["moderate_mentions"] is True:
            mentions.messages_mentions(r, message, logfile)

    except Exception as e:
        log_it(logfile, str(e))


# Check old messages for posts that have since been flaired correctly
def check_comments(r):
    try:
        for comment in r.redditor(config["bot_username"]).comments.new(limit=100):
            if comment.removed is not True and comment.approved is not True:
                if config["moderate_flair"] is True :
                    flair.messages_comment(r, comment, logfile)
    except Exception as e:
        log_it(logfile, str(e))


# Do it every 60 seconds
if __name__ == "__main__":

    while True:
        try:
            r = bot_login(logfile)

            if r is not False :
                log_it(logfile, "Checking submissions...")
                get_posts(r)

                log_it(logfile, "Checking inbox...")
                check_messages(r)

                log_it(logfile, "Checking comments...")
                check_comments(r)

                log_it(logfile, "Finished task!\n---------------------------\n")

        except Exception as e:
            log_it(logfile, str(e))

        time.sleep(60)

    sys.exit()
