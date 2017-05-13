from uuid import uuid4

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InputTextMessageContent, InlineQueryResultArticle
import urllib.request
import logging
import json
import sys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def help(bot, update):
    print ("Help page selected")
    bot.sendMessage(update.message.chat_id, text = "To search for a song on Spotify, just call the bot by typing @spotify_telegram_bot and then typing your query. Then, just select what category you would like to search under!")

def about(bot, update):
    print ("About page selected")
    bot.sendMessage(update.message.chat_id, text = "This bot has been created by GMCtree using Python and the Python Telegram Bot API the Python-Telegram-Bot Team")

def no_results(response):
    return all(not response[_type + "s"]['items'] for _type in types)

def search(query, query_type):
    print("Search attempted")

    search_query = query.lower().strip().replace(' ', '%20')
    api_base_url = "https://api.spotify.com/v1/search?q="
    search_types = {
    'track' : api_base_url + search_query + "&type=track&limit=1",
    'artist' : api_base_url + search_query + "&type=artist&limit=1",
    'album' : api_base_url + search_query + "&type=album&limit=1",
    'playlist' : api_base_url + search_query + "&type=playlist&limit=1"
    }

    search_url = search_types[query_type]

    print("Search URL created")
    request = urllib.request.Request(search_url)
    content_data = json.loads(urllib.request.urlopen(request).read())
    #TODO: make check for no results

    result = content_data[query_type + 's']['items'][0]['external_urls']['spotify']

    return result

# main function to handle all inline queries
def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    # each new value will show up in the response to the user
    results.append(InlineQueryResultArticle(id=uuid4(),
        title='Track',
        input_message_content=InputTextMessageContent(search(query, 'track'))))

    results.append(InlineQueryResultArticle(id=uuid4(),
        title='Artist',
        input_message_content=InputTextMessageContent(search(query, 'artist'))))

    results.append(InlineQueryResultArticle(id=uuid4(),
        title='Album',
        input_message_content=InputTextMessageContent(search(query, 'album'))))

    results.append(InlineQueryResultArticle(id=uuid4(),
        title='Playlist',
        input_message_content=InputTextMessageContent(search(query, 'playlist'))))

    update.inline_query.answer(results)

def error(bot, update, error):
   logger.warn('Update "%s" caused error "%s"' % (update, error))

# main function needed to enable logging
def main():
    with open("telegram_token.txt", "r") as f:
       token = str(f.read()).rstrip()

    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("about", about))

#       dp.add_handler(MessageHandler(Filters.text, search))

    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)

    # begin long polling
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print ("Bot is running...")
    main()
