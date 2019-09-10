import sys
import datahandler
from config import config
from log_it import log_it
import re
import datetime

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
                        # reply = comment.reply(config["mention_resetthecounter_reply_mod"])
                        # reply.mod.distinguish()
                        # submission.flair.select(config["mention_resetthecounter_flair_id"], config["mention_resetthecounter_flair_text"])

                        # Do widget
                        if config["mention_resetthecounter_widgetname"] is not "" :
                            # Get widget
                            widgets = r.subreddit(config["sub_name"]).widgets
                            for widget in widgets.sidebar :
                                if widget.shortName == config["mention_resetthecounter_widgetname"] :
                                    text = widget.text
                                    olddate = re.findall("\- u\/[^\s]* on (.*)\n", text)[0]
                                    record = int(re.findall("\*\*RECORD\: ([^\s]*)\sDAYS\*\*", text)[0])
                                    untildate = re.findall("\*\(until ([^\)]*)\)\*", text)[0].strip()
                                    newdate = datetime.datetime.today().strftime("%d %b %Y")

                                    d1 = datetime.datetime.strptime(olddate.strip(), "%d %b %Y")
                                    d2 = datetime.datetime.today()
                                    days_ago = abs((d2 - d1).days)

                                    if record < days_ago:
                                        record = days_ago
                                        untildate = newdate.strptime("%d %b %Y")

                                    newtext = f"**[{submission.title}](https://www.reddit.com/r/coys/comments/{submission.id})** - u/{submission.author} on {newdate}  \n*posted {days_ago} days after the one before*\n\n**RECORD: {record} DAYS**  \n*(until {untildate})*\n\n*[Why is this here?](https://www.reddit.com/r/coys/comments/7uvbp4/)*".encode("ascii")
                                    # widget.mod.update(text=newtext)
                                    r.subreddit('coys').message('Sidebar Widget Reset', f"The counter has been reset! Code for the updated sidebar is:\n\n{newtext}\n\n---  \nCOYS")
                                    log_it(logfile, "\t\tUpdated sidebar widget")
                                    break

                    else :
                        log_it(logfile, "\tUser request: ResetTheCounter https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id)
                        reply = comment.reply(config["mention_resetthecounter_reply_user"])
                        reply.mod.distinguish()
                        submission.report("Possible Counter Reset situation", "[This post has been reported](https://reddit.com/r/" + config["sub_name"] + "/comments/" + submission.id +") to u/1882-Bot as a possible infringement.\n\n[Click here to send a confirmation message](https://www.reddit.com/message/compose/?to=" + config["bot_username"] + "&message=Naughty%20fuckin%20ticket%20post!&subject=ResetTheCounter:%20" + submission.id + ") or ignore to decline.")

                    datahandler.addTo("mentions", comment.id)
    except Exception as e:
        log_it(logfile, str(e))


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
                            text = widget.text
                            olddate = re.findall("\- u\/[^\s]* on (.*)\n", text)[0]
                            record = int(re.findall("\*\*RECORD\: ([^\s]*)\sDAYS\*\*", text)[0])
                            untildate = re.findall("\*\(until ([^\)]*)\)\*", text)[0].strip()
                            newdate = datetime.datetime.today().strftime("%d %b %Y")

                            d1 = datetime.datetime.strptime(olddate.strip(), "%d %b %Y")
                            d2 = datetime.datetime.today()
                            days_ago = abs((d2 - d1).days)

                            if record < days_ago:
                                record = days_ago
                                untildate = newdate.strptime("%d %b %Y")

                            newtext = "**["+str(submission.title).encode('utf-8')+"](https://www.reddit.com/r/coys/comments/"+str(submission.id)+")** - u/"+str(submission.author)+" on "+str(newdate)+"  \n*posted "+str(days_ago)+" days after the one before*\n\n**RECORD: "+str(record)+" DAYS**  \n*(until "+str(untildate)+")*\n\n*[Why is this here?](https://www.reddit.com/r/coys/comments/7uvbp4/)*"
                            widget.mod.update(text=newtext)
                            log_it(logfile, "\t\tUpdated sidebar widget")
                            break

            #Receipt
            log_it(logfile, "\tSending receipt...")
            message.reply("Thanks " + str(message.author) + ", I've flaired the post and updated the sidebar.\n\nYou can go there by [clicking on this link](" + str(submission.permalink) + ").\n\n" + config["flair_success_reply"])
        # Mark message as read
        message.mark_read()
    except Exception as e:
        log_it(logfile, str(e))