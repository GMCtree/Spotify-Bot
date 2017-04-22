from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import logging
import json
import sys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# contains all types of content as outlined in Spotify Web API
types = ['album', 'artist', 'playlist', 'track']

def help(bot, update):
	print ("Help page selected")
	bot.sendMessage(update.message.chat_id, text = "To make a general search, just enter a search query. To search specifically, type 'artist, album, playlist, or track': query. Example --> artist: Dr. Dre")

def about(bot, update):
	print ("About page selected")
	bot.sendMessage(update.message.chat_id, text = "This bot has been created by GMCtree using Python and the Python Telegram Bot API the Python-Telegram-Bot Team")

def check_search_type(query):
	if query.split(': ')[0] in types:
		return True
	else:
		return False

def format_and_send(bot, update, content_data, is_specific_search, search_type = None):
	bot_response = "Click this link to open the "

	# if user has made a specific search
	if is_specific_search:
		# add 's' to be able to access value in Spotify response JSON
		bot.sendMessage(update.message.chat_id, text = bot_response + search_type + " " + content_data[search_type + 's']['items'][0]['external_urls']['spotify'])
	# if user has made a general search
	else:
		for cur_type in types:
			bot.sendMessage(update.message.chat_id, text = bot_response + cur_type + " " + content_data[cur_type + 's']['items'][0]['external_urls']['spotify'])

def no_results(response):
    return all(not response[_type + "s"]['items'] for _type in types)

def search(bot, update):
	message_list = (update.message.text).split(': ')

	is_specific_search = check_search_type(update.message.text)

	if is_specific_search:
		print ("Specific search selected")
		search_type = message_list[0]
		# replace all spaces with '%20' as per the Spotify Web API protocol
		search_query = message_list[1].lower().strip().replace(' ', '%20')
		request = urllib.request.Request("https://api.spotify.com/v1/search?q=" + search_query + "&type=" + search_type + "&limit=1")
	else:
		print ("General search selected")
		# replace all spaces with '%20' as per the Spotify Web API protocol
		search_query = message_list[0].lower().strip().replace(' ', '%20')
		request = urllib.request.Request("https://api.spotify.com/v1/search?q=" + search_query + "&type=artist,album,playlist,track&limit=1")

	try:
            print ("Search query attempted")
            content_data = json.loads(urllib.request.urlopen(request).read())
            is_no_results = False
#TODO: make no_results work for specific search as well
            if is_specific_search != True:
                is_no_results = no_results(content_data)
            if is_no_results:
                print("No results found")
                bot.sendMessage(update.message.chat_id, text = "No results found :(")
            else:
                # make proper call to function based on search type
                if is_specific_search:
                        format_and_send(bot, update, content_data, is_specific_search, search_type)
                else:
                        format_and_send(bot, update, content_data, is_specific_search)
                print ("Search query successful")
	except urllib.request.HTTPError as e:
		print ("Search query failed")
		print (e.code)
		print (e.read())

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

	dp.add_handler(MessageHandler(Filters.text, search))

	dp.add_error_handler(error)

	# begin long polling
	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	print ("Bot is running...")
	main()
