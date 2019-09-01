import praw
import sys
import time
from datetime import datetime, timedelta
from config import config
from log_it import log_it

def messages_flair(r, message, logfile) :
    subject = message.subject.split()
    submission = r.submission(id=subject[1])
    if submission is None :
        log_it(logfile, "\tCouldn't find submission!")
        message.reply("We couldn't find your post. Try clicking on the submission link again, but ensure you keep the subject line the same!")
    elif submission.link_flair_text is None :
        log_it(logfile, "\tStill no flair, responding...")
        message.reply("We couldn't see your new flair. Please wait a bit and try again.")
    elif submission.link_flair_text[0:7] == "Removed" or submission.selftext == '[deleted]' :
        # Post has been removed
        log_it(logfile, "\tPost was removed already")
    else:
        # Unremove
        log_it(logfile, "\tFlair suggestion worked! Approving post and removing comment...")
        submission.mod.approve()
        # Remove comment
        for top_level_comment in submission.comments:
            if top_level_comment.author == config["bot_username"] :
                top_level_comment.mod.undistinguish()
                top_level_comment.mod.remove()
                log_it(logfile, "\t\tRemoved message from https://reddit.com/r/"+config["sub_name"]+"/comments/" + submission.id)

        #Receipt
        log_it(logfile, "\tSending receipt...")
        message.reply("Thanks " + str(message.author) + ", I've approved your post!\n\nYou can go there by [clicking on this link](" + str(submission.permalink) + ").\n\n" + config["flair_success_reply"])
    # Mark message as read
    message.mark_read()

def messages_comment(r, comment, logfile) :
    if comment.body[0:27] == "**Please flair your post!**" :
        submission = r.submission(id=comment.submission)
        if (submission.link_flair_text is not None and submission.link_flair_text[0:7] == "Removed") or submission.selftext == '[deleted]':
            # Submission removed or deleted. Undistinguish and remove comment, then approve the submission!
            comment.mod.undistinguish()
            comment.mod.remove()
            submission.mod.approve()
        elif submission.link_flair_text is not None:
            # Submission has been flaired!
            comment.mod.undistinguish()
            comment.mod.remove()
            log_it(logfile, "\tRemoved message from https://reddit.com/r/"+config["sub_name"]+"/comments/" + submission.id)
        elif datetime.now() - timedelta(hours=1) > datetime.fromtimestamp(submission.created_utc) :
            # It's been longer than an hour. Give it a flair and edit the comment...
            new_comment = comment.body + "\n\n---\n\nEDIT: This post has been **removed** because the user forgot to flair their post! Please remember to flair in future.\n\n" + config["flair_failure_edit"]
            submission.flair.select(config["flair_failure_flair_id"], config["flair_failure_flair_text"])
            comment.edit(new_comment)
            comment.mod.approve()
            log_it(logfile, "\tPost never flaired: https://reddit.com/r/"+config["sub_name"]+"/comments/" + submission.id)
        else :
            log_it(logfile, "\tComment still valid: https://reddit.com/r/"+config["sub_name"]+"/comments/" + submission.id)
