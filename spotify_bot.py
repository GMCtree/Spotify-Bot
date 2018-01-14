import os, urllib.request, logging, json, sys, auth
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InputTextMessageContent, InlineQueryResultArticle

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def help(bot, update):
    print ("Help page selected")
    bot.sendMessage(update.message.chat_id, text = "To search for a song on Spotify, just call the bot by typing @spotify_telegram_bot and then typing your query. Then, just select what category you would like to search under!")

def about(bot, update):
    print ("About page selected")
    bot.sendMessage(update.message.chat_id, text = "This bot has been created by GMCtree using Python and the Python Telegram Bot API created by the Python-Telegram-Bot Team")

def get_thumbnail(response):
    # check if images exist for search query
    if 'images' in response and len(response['images']) > 0:
        image = response['images'][0]
        thumbnail = image['url']
        thumbnail_width = image['width']
        thumbnail_height = image['height']
        return (thumbnail, thumbnail_width, thumbnail_height)
    else:
        return (None, None, None)

def search(query, query_type, auth_token):
    # replace all spaces with %20 as per Spotify Web API
    search_query = query.lower().strip().replace(" ", "%20")
    api_base_url = "https://api.spotify.com/v1/search?q="
    search_types = {
        "track" : api_base_url + search_query + "&type=track&limit=1",
        "artist" : api_base_url + search_query + "&type=artist&limit=1",
        "album" : api_base_url + search_query + "&type=album&limit=1",
        "playlist" : api_base_url + search_query + "&type=playlist&limit=1"
    }

    search_url = search_types[query_type]

    request = urllib.request.Request(search_url)
    request.add_header("Authorization", "Bearer " + auth_token)

    try:
        content_data = json.loads(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as err:
        if err.code == 400:
            print("Looks like you have a bad request. Have you checked to make sure your header is correct?")
            print(err.read())
        elif err.code == 401:
            print("Your authorization token is incorrect or expired. Please request a new one")
            print(err.read())
        else:
            print(err.read())

    if len(content_data[query_type + 's']['items']) == 0:
        return None
    else:
        response = content_data[query_type + 's']['items'][0]
        spotify_link = response['external_urls']['spotify']
        (thumbnail, thumbnail_width, thumbnail_height) = get_thumbnail(response)
        return (spotify_link, thumbnail, thumbnail_width, thumbnail_height)

def is_empty_query(query):
    return True if query == '' else False

def check_no_results(results):
    return True if len(results) == 0 else False

# main function to handle all inline queries
def inlinequery(bot, update):

    print("New query started")
    query = update.inline_query.query
    results = list()
    types = ['Track', 'Artist', 'Album', 'Playlist']

    auth_token = auth.get_auth_token()

    # if empty query, return blank results to prevent unnecessary Spotify API calls
    if is_empty_query(query):
        return results
    else:
    # each new value will show up in the response to the user
        for _type in types:
            response = search(query, _type.lower(), auth_token)
            if response is not None:
                results.append(InlineQueryResultArticle(id=uuid4(),
                        title=_type,
                        input_message_content=InputTextMessageContent(response[0]),
                        thumb_url=response[1],
                        thumb_width=response[2],
                        thumb_height=response[3]))

    # if there are no results, tell user
    if check_no_results(results):
        results.append(InlineQueryResultArticle(id=uuid4(),
                title="No results found",
                input_message_content=InputTextMessageContent("No results found")))

    update.inline_query.answer(results)

def error(bot, update, error):
   logger.warn('Update "%s" caused error "%s"' % (update, error))

# main function needed to enable logging
def main():

    # Check to see which environment to use by reading from config file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        if not config["prod"]:
            with open("telegram_token.json", "r") as token_file:
                token = json.load(token_file)["token"]
        else:
            token = os.environ["TELEGRAM_KEY"]

    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("about", about))

    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)

    # begin long polling
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print ("Bot is running...")
    main()
