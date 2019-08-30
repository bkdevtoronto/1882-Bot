# Add in your subreddit here:
_SUBREDDIT_ = "your_subreddit"

# Dependencies
import praw
import sys
import time
from datetime import datetime, timedelta

from bot_login import bot_login
from log_it import log_it

# Get the posts and stuff
def get_posts(r):
    try:
        for submission in r.subreddit(_SUBREDDIT_).new(limit=30):
            if submission.link_flair_text is None :
                reply = '''**Please flair your post!**

In /r/coys, we're having a trial period where we require all posts to be flaired appropriately. [You can find out more details and discuss this here](https://www.reddit.com/r/coys/comments/cw3n72/psa_sub_flairs_test/).

Once you've flaired your post, [send **1882-Bot** a message by clicking here.](https://www.reddit.com/message/compose/?to=1882-Bot&message=Post%20has%20been%20flaired!&subject=Flaired:%20''' + submission.id + '). *Don\'t change the subject line so that **1882-Bot** knows what to do!*'
                comment = submission.reply(reply)
                comment.mod.distinguish(sticky=True)
                submission.mod.remove()
                log_it("\nAlerted no-flair on: '" + str(submission.title) + "' (by " + str(submission.author) + " - " + str(submission.permalink) + ")" )
    except Exception as e:
        log_it(e)



# Check messages for updated posts
def check_messages(r):
    try:

        # Only select unread messages
        for message in r.inbox.unread(limit=None):
            subject = message.subject.split()
            if(subject[0] == "Flaired:"):
                submission = r.submission(id=subject[1])
                if submission is None :
                    log_it("\tCouldn't find submission!")
                    message.reply("We couldn't find your post. Try clicking on the submission link again, but ensure you keep the subject line the same!")
                elif submission.link_flair_text is None :
                    log_it("\tStill no flair, responding...")
                    message.reply("We couldn't see your new flair. Please wait a bit and try again")
                elif submission.link_flair_text[0:7] == "Removed" or submission.selftext == '[deleted]' :

                    # Post has been removed
                    log_it("\tPost was removed already")
                else:

                    # Unremove
                    log_it("\tFlair suggestion worked! Approving post and removing comment...")
                    submission.mod.approve()

                    # Remove comment
                    for top_level_comment in submission.comments:
                        if top_level_comment.author == "1882-Bot" :
                            top_level_comment.mod.undistinguish()
                            top_level_comment.mod.remove()
                            log_it("\t\tRemoved message from '" + submission.title[0:30] + "'...: https://reddit.com/r/coys/comments/" + submission.id)

                    #Receipt
                    log_it("\tSending receipt...")
                    message.reply('''Thanks " + str(message.author) + ", I've approved your post!

You can go there by [clicking on this link](" + str(submission.permalink) + ").

COYS!''')


                # Mark message as read
                message.mark_read()
    except Exception as e:
        log_it(str(e))


# Check old messages for posts that have since been flaired correctly
def check_comments(r):
    try:
        for comment in r.redditor('1882-Bot').comments.new(limit=100):
            if comment.removed is not True and comment.approved is not True:
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
                        log_it("\tRemoved message from '" + submission.title[0:30] + "'...: https://reddit.com/r/coys/comments/" + submission.id)
                    elif datetime.now() - timedelta(hours=1) > datetime.fromtimestamp(submission.created_utc) :

                        # It's been longer than an hour. Give it a flair and edit the comment...
                        new_comment = comment.body + '''

---

EDIT: This post has been **removed** because the user forgot to flair their post! Please remember to flair in future. For more information, [see this post](https://reddit.com/r/coys/comments/cw3n72/).

COYS'''
                        submission.flair.select("4a538d20-327a-11e8-b606-0ec2b090ed4e", "Removed by 1882-Bot")
                        comment.edit(new_comment)
                        comment.mod.approve()
                        log_it("\tPost never flaired: '" + submission.title[0:30] + "'...: https://reddit.com/r/coys/comments/" + submission.id)
                    else :
                        log_it("\tComment still valid: '" + submission.title[0:30] + "'...: https://reddit.com/r/coys/comments/" + submission.id)
    except Exception as e:
        log_it(str(e))


# Do it every 60 seconds (turned off because cron)
if __name__ == "__main__":

    # while True:
    try:
        r = bot_login()

        log_it("Checking submissions...")
        get_posts(r)

        log_it("Checking inbox...")
        check_messages(r)

        log_it("Checking comments...")
        check_comments(r)
        log_it("Finished task!")

        # time.sleep(60)
    except Exception as e:
        log_it(e)

    sys.exit()
