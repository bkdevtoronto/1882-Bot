import sys
import datahandler
from config import config
from log_it import log_it
import re
import datetime

def generate_widget(submission, original):
    olddate = re.findall("\- by u\/[^\s]* on (.*)", original)[0]
    newdate = datetime.datetime.today().strftime("%d %b %Y")

    record = int(re.findall("\*\*RECORD\: ([^\s]*)\sDAYS\*\*", original)[0])
    untildate = re.findall("\*\(until ([^\)]*)\)\*", original)[0].strip()

    author = "[deleted]" if (submission.author is None) else submission.author

    d1 = datetime.datetime.strptime(olddate.strip(), "%d %b %Y")
    d2 = datetime.datetime.today()
    days_ago = abs((d2 - d1).days)

    if record < days_ago:
        record = days_ago
        untildate = newdate.strptime("%d %b %Y")

    newtext = "[" + submission.title + "]"
    newtext = newtext + "(https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id + ")"
    newtext = newtext + " - by u/" + str(author)
    newtext = newtext + " on " + newdate
    newtext = newtext + "  \n*posted " + str(days_ago) + " days after the one before*"
    newtext = newtext + "  \n\n**RECORD: " + str(record) + " DAYS**"
    newtext = newtext + "  \n*(until " + untildate + ")*"
    newtext = newtext + "  \n\n*[Why is this here?](https://reddit.com/r/coys/comments/7uvbp4/)*  "

    pattern = re.compile(r"([\[\]\(\*])")
    msgtext = pattern.sub(r"\\\1", newtext)

    return newtext, msgtext


def messages_mentions(r, message, logfile, mods, history):
    # Get important variables
    comment = r.comment(id=message.id)
    msgtext = comment.body.split("\n")[0].split(" ")[1:]
    submission = r.submission(id=comment.link_id[3:])
    request = msgtext[0].lower()

    # Execute
    if comment.subreddit.display_name.lower() == config["sub_name"].lower() and comment.id not in history :
        if request == "resetthecounter" :
            if comment.author in mods:
                log_it(logfile, "\tMod request: ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                reply = comment.reply(config["mention_resetthecounter_reply_mod"])
                reply.mod.distinguish()
                submission.flair.select(config["mention_resetthecounter_flair_id"], config["mention_resetthecounter_flair_text"])

                # Do widget
                if config["mention_resetthecounter_widgetname"] is not "" :
                    # Get widget
                    widgets = r.subreddit(config["sub_name"]).widgets
                    for widget in widgets.sidebar :
                        if widget.shortName == config["mention_resetthecounter_widgetname"] :
                            # Update and execute
                            newtext = generate_widget(submission, widget.text)
                            widget.mod.update(text=newtext[0])
                            log_it(logfile, "\t\tUpdated sidebar widget")

                            # Send message for legacy sidebar
                            msgtext = "Sidebar Widget update text:  \n\n---\n\n" + newtext[0]
                            r.subreddit(config["sub_name"]).message("Sidebar Widget", newtext[1])
                            break

            else :
                log_it(logfile, "\tUser request: ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                reply = comment.reply(config["mention_resetthecounter_reply_user"])
                submission.report("Possible Counter Reset situation", "[This post has been reported](https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id +") to u/1882-Bot as a possible infringement.\n\n[Click here to send a confirmation message](https://www.reddit.com/message/compose/?to=" + config["bot_username"] + "&message=Naughty%20fuckin%20ticket%20post!&subject=ResetTheCounter:%20" + submission.id + ") or ignore to decline.")
                reply.mod.distinguish()

            datahandler.addTo("mentions", comment.id)
            log_it(logfile, "\t\tUpdated 'Mentions' list data: comment ID " + str(comment.id))



def message_resetthecounter(r, message, logfile) :
    try:
        mods = r.subreddit(config["sub_name"]).moderator()
        subject = message.subject.split()
        submission = r.submission(id=subject[1])

        if submission is None :
            log_it(logfile, "\tCouldn't find submission!")
            message.reply("We couldn't find your post. Try clicking on the submission link again, but ensure you keep the subject line the same!")
        else:
            if comment.author in mods:
                log_it(logfile, "\tMod message to ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                submission.flair.select(config["mention_resetthecounter_flair_id"], config["mention_resetthecounter_flair_text"])

                # Do widget
                if config["mention_resetthecounter_widgetname"] is not "" :
                    # Get widget
                    widgets = r.subreddit(config["sub_name"]).widgets
                    for widget in widgets.sidebar :
                        if widget.shortName == config["mention_resetthecounter_widgetname"] :
                            # Update and execute
                            newtext = generate_widget(submission, widget.text)
                            widget.mod.update(text=newtext[0])
                            log_it(logfile, "\t\tUpdated sidebar widget")

                            # Send message for legacy sidebar
                            msgtext = "Sidebar Widget update text:  \n\n---\n\n" + newtext[0]
                            r.subreddit(config["sub_name"]).message("Sidebar Widget", newtext[1])
                            break

            #Receipt
            log_it(logfile, "\tSending receipt...")
            message.reply("Thanks " + str(message.author) + ", I've flaired the post and updated the sidebar.\n\nYou can go there by [clicking on this link](" + str(submission.permalink) + ").\n\n" + config["flair_success_reply"])
        # Mark message as read
        message.mark_read()
    except Exception as e:
        log_it(logfile, str(e))
