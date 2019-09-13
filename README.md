<h1 align="center">Welcome to 1882Bot 🐓</h1>

> <p align="center">reddit bot built in python for r/coys.<br /> 1882-Bot will action upon user submissions and messages and is a work in progress.</p>

## ✨ Demo

Example comments and messages:

<p align="center">
  <img width="700" align="center" src="https://i.imgur.com/878og9x.png" alt="comments and messages"/>
</p>

Generated output in console:

<p align="center">
  <img width="700" src="https://i.imgur.com/MGj0BvR.png" alt="cli output 1"/>
  
  <img width="700" src="https://i.imgur.com/Ufo6xyv.png" alt="cli output 2"/>
</p>

## 🌌 Features

**1882-Bot** can do the following as of `1.1`:

* Action upon submissions based on flair (remove/approve, comment)
* Generate message link for auto-action
* Read inbox, act upon subject lines
* Respond to messages, audit self comments

**1882-Bot** also has a super-easy self-edit configuration file that you can find at `config.py`

## 🚀 Usage

Make sure you have [npx](https://www.npmjs.com/package/npx) installed (`npx` is shipped by default since npm `5.2.0`)

### ⚫ Step 1: Install PRAW

If you don't already have PRAW (Python reddit API Wrapper) installed, you should install them using your preferred method or via the command line:

    $ pip install praw

### ⚫ Step 2: Clone the repository

Clone using your preferred method or via the command line:

    $ git clone https://github.com/bkdevtoronto/1882-Bot

### ⚫ Step 3: Add your own configuration to `praw.ini`

Open up `praw.ini` to add in the following:

* Your bot's username and password
* Your app's secret and key

If you don't have an app, you can create one by visiting [reddit/prefs/apps](https://www.reddit.com/prefs/apps). Ensure it is created as a script type in your bot's account.

### ⚫ Step 3: Add your details to `config.py`

Open up `config.py` to configure the bot to your specifications.

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/bkdevtoronto/1882bot/issues) if you want to contribute.

## Author

👤 **Ben Kahan**

- Github: [@bkdevtoronto](https://github.com/bkdevtoronto)
- Reddit: [u/magicwings](https://reddit.com/u/magicwings)
