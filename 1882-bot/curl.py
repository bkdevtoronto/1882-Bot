# pip install beautifulsoup4
import requests
from log_it import log_it
import re
from bs4 import BeautifulSoup
from config import config

def prematch_thread(r, logfile, url="https://www.bbc.com/sport/football/49719155"):
    if not url:
        url = 'https://www.bbc.com/sport/football/49719155'

    r = requests.get(url)
    if r :
        if r.status_code is 200 :
            try:
                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                fixture = soup.find("div", class_="fixture__wrapper")
                teams = fixture.find_all("abbr", class_="fixture__team-name-trunc")
                content = []
                for para in soup.find("div", id="story-body").find_all(["p", "h3"]):
                    if para.name == "p":
                        content.append(str(para.get_text().strip()))
                    elif para.name == "h3" :
                        content.append("##"+str(para.get_text().strip()))

                teams = [teams[0].get_text().strip(), teams[1].get_text().strip()]
                time = str(fixture.find("span", class_="fixture__number--time").get_text().strip())
                date = str(soup.find("time", class_="fixture__date").get_text().strip()).title()
                comp = str(soup.find("div", class_="fixture_date-time-wrapper").find("span", class_="fixture__title").get_text().strip()).title()

                title = "Pre-Match Thread: " + teams[0] + " v " + teams[1] + ", " + comp + " (" + date + ")"
                body = "#" + teams[0] + " vs " + teams[1]
                body += "\n\n##" + comp + ", " + date + " at " + time
                body += "\n\n" + ("\n\n".join(content))

                return [title, body]

            except Exception as e:
                log_it("\tCould not post thread: " + str(e))
                return False
        else :
            log_it(logfile, "\tCould not post thread: " + str(r.status_code) + " response code")
            return False
    else :
        log_it(logfile, "\tCould not post thread: could not connect")
        return False

def get_table():
    url = 'https://www.theguardian.com/football/premierleague/table'
    r = requests.get(url)

    if r:
        if r.status_code is 200:
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            table = soup.find("table", class_="table--football")
            retdata = ["Pos|Club|P|GD|Pts", "--:|:--|:-:|:-:|:-:"]
            for row in table.find("tbody").find_all("tr"):
                # Store in array
                cells = row.find_all("td")
                club_pos = str(cells[0].get_text().strip().replace("\n", ""))
                club_name = str(cells[1].get_text().strip().replace("\n", ""))
                club_played = str(cells[2].get_text().strip().replace("\n", ""))
                club_gd = str(cells[8].get_text().strip().replace("\n", ""))
                club_pts = str(cells[9].get_text().strip().replace("\n", ""))

                if club_name == config["curl_club_name"]:
                    club_name = "**" + club_name + "**"

                retdata.append("|".join([club_pos, club_name, club_played, club_gd, club_pts]))

            return "  \n".join(retdata)
        else :
            log_it(logfile, "\tCould not get table: " + str(r.status_code) + " response code")
            return False
    else :
        log_it(logfile, "\tCould not get table: could not connect")
        return False

def get_scorers():
    url = config["curl_stat_url"]
    r = requests.get(url)

    if r:
        if r.status_code is 200:
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            retdata = ["Player|G|A|MpG|S|%", ":--|:-:|:-:|:-:|:-:|:-:"]
            for row in soup.find_all("div", class_="top-player-stats__body"):
                pl_name = row.find("h2").get_text().strip()
                pl_goals = row.find("span", class_="top-player-stats__goals-scored-number").get_text().strip()
                pl_assists = row.find("span", class_="top-player-stats__assists-number").get_text().strip()
                pl_minspergoal = re.sub("[^0-9]", "", row.find("p", class_="top-player-stats__mins-per-goal").get_text().strip())
                pl_minsplayed = re.sub("[^0-9]", "", row.find("p", class_="top-player-stats__mins-played").get_text().strip())
                pl_shotstotal = row.find("span", class_="shots-total").get_text().strip()
                pl_shotratio = re.sub("[^0-9]", "", row.find("span", class_="percentage-goals-on-target").get_text().strip())

                retdata.append("|".join([pl_name, pl_goals, pl_assists, pl_minspergoal, pl_minsplayed, pl_shotstotal, pl_shotratio]))

            return "  \n".join(retdata) + "\n\n" + "**G**oals, **A**ssists, **M**ins **p**er **G**oal, **S**hots, shot-goal **%**\n\nFigures for all competitions"

        else :
            log_it(logfile, "\tCould not get scorers: " + str(r.status_code) + " response code")
            return False
    else :
        log_it(logfile, "\tCould not get scorers: could not connect")
        return False


def messages_respond(r, message, logfile):
    if message.subject.lower() == "stats":
        log_it(logfile, "\tStats Request - responding...")
        pattern = re.compile(r"([\[\]\(\*\|])")

        retmsg = "Hey **" + str(message.author) + "**,  \n\nHere are the latest stats for the sidebar:\n\n"
        retmsg = retmsg + "#Table\n\n" + pattern.sub(r"\\\1", get_table()) + "\n\n---\n\n"
        retmsg = retmsg + "#Scorers\n\n" + pattern.sub(r"\\\1", get_scorers()) + "\n\n --- \n\n COYS!"
        message.reply(retmsg)
        message.mark_read()
    elif message.subject.split(": ")[0].strip().lower() == "prematchthread" :
        log_it(logfile, "\tPrematch Thread - posting...")
        url = message.subject.split(": ")[1].strip()
        post = prematch_thread(r, logfile, url)
        if not post:
            log_it(logfile, "\tCould not post thread!")
        else :
            submission = r.subreddit(config["sub_name"]).submit(post[0], selftext=post[1], flair_id=config["prematchthread_flair_id"], flair_text=config["prematchthread_flair_text"])
            submission.mod.sticky()
            message.reply("Hey **" + str(message.author) + "**,\n\nI've posted the thread! Check it out here: https://reddit.com/r/" + config["sub_name"] + "/comments/" + str(submission) + "/-/")
            message.mark_read()
