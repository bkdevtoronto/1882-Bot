# pip install beautifulsoup4
import requests
from log_it import log_it
import re
from bs4 import BeautifulSoup
from config import config


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
            log_it(logfile, "Error - received " + str(r.status_code) + " response code")
    else :
        log_it(logfile, "Error - could not connect")

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
            log_it(logfile, "Error - received " + str(r.status_code) + " response code")
    else :
        log_it(logfile, "Error - could not connect")


def messages_respond(r, message, logfile):
    # log_it(logfile, "\tChecking requests...")
    try :
        if message.subject.lower() == "stats":
            log_it(logfile, "\t\tStats Request - responding...")
            pattern = re.compile(r"([\[\]\(\*\|])")

            retmsg = "Hey **" + str(message.author) + "**,  \n\nHere are the latest stats for the sidebar:\n\n"
            retmsg = retmsg + "#Table\n\n" + pattern.sub(r"\\\1", get_table()) + "\n\n---\n\n"
            retmsg = retmsg + "#Scorers\n\n" + pattern.sub(r"\\\1", get_scorers()) + "\n\n --- \n\n COYS!"
            message.reply(retmsg)
            message.mark_read()
    except Exception as e:
        log_it(logfile, "Error: " + str(e))
