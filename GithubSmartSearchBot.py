# Python Bot to search Github by repository (default) or by user

# Licensed under the MIT license.

# TODO: deploy on heroku
# https://www.codementor.io/@karandeepbatra/part-2-deploying-telegram-bot-for-free-on-heroku-19ygdi7754

import logging

from github import Github
from settings import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

g = Github(GITHUB_ACCESS_TOKEN)

def start(update, context):    
    update.message.reply_text('Hi, you can start your smart Github search now')


def help(update, context):    
    update.message.reply_text('You can search Github by repository (default) or by user. Switch on the mode you need and type repository or user details')


def search(update, context):    
    repos = g.search_repositories(update.message.text + ' fork:true sort:stars')

    for repo in repos[:10]:
        text = f"<a href='{repo.html_url}'>{repo.name}</a>"
        update.message.reply_text(text, parse_mode='HTML')       

def error(update, context):    
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Start the bot
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # Replace token
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    dp.add_handler(MessageHandler(Filters.text, search))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
