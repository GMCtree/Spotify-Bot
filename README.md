# Spotify Bot

***NOTE: The bot is currently hosted on Heroku***

## Table of Contents
[Introduction](#intro)  
[Usage](#use)  
[Running the Bot](#run)  
  * [Local](#local)
  * [Heroku](#heroku)  
  
[Running the Unit Tests](#tests)

<a id = "intro"></a>
## Introduction
This is a Telegram bot that has the ability to make calls to the Spotify API to satisfy user requests. This bot is wrtten in Python and is being developed with the [Telegram Bot API](https://core.telegram.org/bots/api) provided by the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) team. The documentation for the API that I used is located [here](https://python-telegram-bot.org/)

<a id = "use"></a>
## Usage
To use the bot, you will first need to create a [Telegram](https://telegram.org/) account. Once you do that, you can call the bot from anywhere by calling the bot with @spotify_telegram_bot.

To make a search, call the bot and type. The bot will respond with an option to grab the top result of either a track, artist, album or playlist and you can click which you would like to get a Spotify link to the item.

<a id = "run"></a>
## Running the Bot
<a id = "local"></a>
### Local
To run the bot on your local machine, go into the config.json file and switch the "prod" value to "false". Then, you can run the bot just by typing the following:
```
python3 spotify_bot.py
```
After that, the bot should be running and will receive requests as long as it is running.

<a id = "heroku"></a>
### Heroku
To run the bot locally using Heroku, create a .env file using the format KEY=VALUE, where KEY is the key to access the VALUE, and the VALUE is you Telegram API key. You should also follow the same format for your Spotify Developer client ID and client secret keys.
Example:
```
TELEGRAM_KEY=YOUR_API_KEY
CLIENT_ID=YOUR_CLIENT_ID
CLIENT_SECRET=YOUR_SECRET_KEY
```

You can then access this value by using:
```
os.environ["TELEGRAM_KEY"]
os.environ["CLIENT_ID"]
os.environ["CLIENT_SECRET"]
```
To run the bot, just type:
```
heroku local
```
And then the bot will accept requests.

To host the bot on Heroku, first create a free account on [Heroku](https://www.heroku.com/). After doing that, follow the instructions to set up your bot on your Heroku repo. After doing that, go to your config variables in Heroku (located under 'Settings') and make sure to add the environment variables that you created in your .env file to here as well. If the bot ran correctly using Heroku locally, then it should run fine when hosted.

<a id = "tests"></a>
## Running the Unit Tests
The unit tests have been written using the Python 3 `unittest` library. To run the unit tests, run the following in your terminal:
```
python3 tests.py
```

This will run the unit tests and will let you know if all of them passed or not. If you would like more visibility into which tests pass and which ones did not, run the tests with the `-v` argument like so:
```
python3 tests.py -v
```

This will tell you the results of each of the tests individually as opposed to only telling you if all of them passed or not.

