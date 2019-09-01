config = {

    ### Bot <======================

    "bot_username" : "1882-Bot",
        # [string, required] Your bot's username, i.e. u/{foo}

    "bot_name" : "1882Bot",
        # [string, required] The name to give your bot, i.e. {FooBot 3000}

    ### Subreddit <================

    "sub_name" : "coys",
        # [string, required] The subreddit you want to monitor, i.e. r/{foo}

    ### Flair <====================

    "moderate_flair" : True,
        ## Global setting to moderate flair <-----------------------------------
        # [bool] Set whether you want 1882-Bot to scan for unflaired submissions

    "flair_submission_reply" : "In /r/coys, we're having a trial period where we require all posts to be flaired appropriately. [You can find out more details and discuss this here](https://reddit.com/r/coys/comments/cw3n72/).",
        # [string] Auto reply body for submissions which don't have a flair
        # NB: Already has header and footer

    "flair_success_reply" : "COYS!",
        # [string] Append this to the auto-edit message to 1882-Bot's comment when a user flairs their post
        # NB: Already has body

    "flair_failure_edit" : "For more information, [see this post](https://reddit.com/r/coys/comments/cw3n72/).\n\nCOYS",
        # [string] Append message to end of autoedit to users who did not flair their post in time
        # NB: Already has body

    "flair_failure_flair_id" : "4a538d20-327a-11e8-b606-0ec2b090ed4e",
    "flair_failure_flair_text" : "Removed by 1882-Bot"
        # [string, string] Flair details when flairing to remove post for failure to flair
        # Find this at reddit.com/r/your_sub?styling=true and navigate to Post Flairs
}
