from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def help(bot, update):
	print("Help page selected")
	bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
	bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

# main function needed to enable logging
def main():
	updater = Updater(str(open("telegram_token.txt", "r").read()))

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("help", help))

	dp.add_handler(MessageHandler([Filters.text], echo))

	dp.add_error_handler(error)

	# being long polling
	updater.start_polling()

	# run bot until KeyboardInterrupt event
	updater.idle()


if __name__ == '__main__':
	main()
