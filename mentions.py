import sys
import datahandler
from config import config
from log_it import log_it

def messages_mentions(r, message, logfile):
    log_it(logfile, "Checking mentions...")
    try:
        history = datahandler.get("mentions")
        mods = r.subreddit(config["sub_name"]).moderator()

        for message in r.inbox.mentions(limit=30):
            # Get important variables
            comment = r.comment(id=message.id)
            message = comment.body.split("\n")[0].split(" ")[1:]
            submission = r.submission(id=comment.link_id[3:])
            request = message[0].lower()

            if comment.subreddit.display_name.lower() == config["sub_name"].lower() and comment.id not in history :
                if request == "resetthecounter" :
                    if comment.author in mods:
                        log_it(logfile, "\tMod request: ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                        reply = comment.reply(config["mention_resetthecounter_reply_mod"])
                        reply.mod.distinguish()
                        submission.flair.select(config["mention_resetthecounter_flair_id"], config["mention_resetthecounter_flair_text"])
                    else :
                        log_it(logfile, "\tUser request: ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                        reply = comment.reply(config["mention_resetthecounter_reply_user"])
                        reply.mod.distinguish()
                        submission.report("Possible Counter Reset situation")

                    datahandler.addTo("mentions", comment.id)
    except Exception as e:
        log_it(logfile, str(e))
