from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib2
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def help(bot, update):
	print "Help page selected"
	bot.sendMessage(update.message.chat_id, text="To make a general search, just enter a search query. To search specifically, type 'artist, album, playlist, or track': query. Example --> artist: Dr. Dre")

def about(bot, update):
	print "About page selected"
	bot.sendMessage(update.message.chat_id, text="This bot has been created by GMCtree using Python and the Python Telegram Bot API the Python-Telegram-Bot Team")

def is_specific_search(query):
	types = ['album:', 'artist:', 'playlist:', 'track:']
	if query.split(': ')[0] in types:
		return True
	else:
		return False


def search(bot, update):
	secret = open("secret.txt", "r").read()
	message_list = (update.message.text).split(': ')

	if is_specific_search(update.message.text):
		search_type = message_list[0]
		# replace all spaces with '+' as per the Spotify Web API protocol
		search_query = message_list[1].replace(' ', '+')
		request = urllib2.Request("https://api.spotify.com/v1/search?q=" + search_query + "&type=" + search_type + "&limit=5", headers={"Authorization" : secret})
	else:
		# replace all spaces with '+' as per the Spotify Web API protocol
		search_query = message_list[0].replace(' ', '+')
		request = urllib2.Request("https://api.spotify.com/v1/search?q=" + search_query + "&limit=1", headers={"Authorization" : secret})

	print request
	contents = urllib2.urlopen(request).read()
	print contents
	bot.sendMessage(update.message.chat_id, text="Request Sent")

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

# main function needed to enable logging
def main():
	updater = Updater(str(open("telegram_token.txt", "r").read()))

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("help", help))

	dp.add_handler(CommandHandler("about", about))

	dp.add_handler(MessageHandler([Filters.text], search))

	dp.add_error_handler(error)

	# being long polling
	updater.start_polling()

	# run bot until KeyboardInterrupt event
	updater.idle()


if __name__ == '__main__':
	print "Bot is running..."
	main()
