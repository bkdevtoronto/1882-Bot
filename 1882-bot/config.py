config = {

    ### Settings <=================

    # Set your log and data directories (local with trailing slash)
    "logDirectory" : "logs/",
    "dataDirectory" : "data/",

    ### Bot <======================

    # [string, required] Your bot's username, i.e. u/{foo}
    "bot_username" : "1882-Bot",

    # [string, required] The name to give your bot, i.e. {FooBot 3000}
    "bot_name" : "1882Bot",

    ### Subreddit <================

    # [string, required] The subreddit you want to monitor, i.e. r/{foo}
    "sub_name" : "coys",

    ### cURL/Stat Checks <=========

    ## Global setting to check for external data <--------------------------
    # [bool] Set whether you want 1882-Bot to respond to stat request
    "reply_curl" : True,

    # Check on https://www.theguardian.com/football/premierleague/table for your team's name
    "curl_club_name" : "Spurs",

    # Modify this for your team's BBC stat page
    "curl_stat_url" : "https://www.bbc.com/sport/football/teams/tottenham-hotspur/top-scorers",

    ### Flair <====================

    ## Global setting to moderate flair <-----------------------------------
    # [bool] Set whether you want 1882-Bot to scan for unflaired submissions
    "moderate_flair" : True,

    # [string] Auto reply body for submissions which don't have a flair
    # NB: Already has header and footer
    "flair_submission_reply" : "In /r/coys, all posts need to be flaired appropriately. [You can find out more details here](https://reddit.com/r/coys/comments/cw3n72/).",

    # [string] Append this to the auto-edit message to 1882-Bot's comment when a user flairs their post
    # NB: Already has body
    "flair_success_reply" : "COYS!",

    # [string] Append message to end of autoedit to users who did not flair their post in time
    # NB: Already has body
    "flair_failure_edit" : "For more information, [see this post](https://reddit.com/r/coys/comments/cw3n72/).\n\nCOYS",

    "flair_failure_flair_id" : "4a538d20-327a-11e8-b606-0ec2b090ed4e",
    # [string, string] Flair details when flairing to remove post for failure to flair
    # Find this at reddit.com/r/your_sub?styling=true and navigate to Post Flairs
    "flair_failure_flair_text" : "Removed by 1882-Bot",

    # [bool] Set whether you want 1882-Bot to scan for mentions
    "moderate_mentions" : True,
    "mention_resetthecounter_reply_mod" : "Thanks for the heads up, I'll update the sidebar. You're welcome.\n\nCOYS",
    "mention_resetthecounter_reply_user" : "Thanks for the heads up, I'll alert the mods.\n\nCOYS",
    "mention_resetthecounter_flair_id" : "4b9c8952-7168-11e8-833e-0e6be7fce3be",
    "mention_resetthecounter_flair_text" : "Reset the Counter",
    "mention_resetthecounter_widgetname" : "Ticket Question Free Since...",

    "prematchthread_flair_id" : "3e7c5ad6-327a-11e8-a1d2-0ea44711638e",
    "prematchthread_flair_text" :  "PreMatch Thread"
}
