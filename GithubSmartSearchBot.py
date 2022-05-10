# Python Bot to search Github by repository or by user

# Licensed under the MIT license.

# TODO: deploy on heroku
# https://www.codementor.io/@karandeepbatra/part-2-deploying-telegram-bot-for-free-on-heroku-19ygdi7754

import logging

from github import Github
from settings import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

g = Github(GITHUB_ACCESS_TOKEN)

def main_menu_keyboard():
    menu_main = [[InlineKeyboardButton('Search by repo', callback_data='repo')],
                 [InlineKeyboardButton('Search by user', callback_data='user')]]
    return InlineKeyboardMarkup(menu_main)

def main_menu(bot, update):
    query = bot.callback_query
    query.answer()
    bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())


def repo_submenu(bot, update):
    query = bot.callback_query
    query.answer()
    update.user_data["Repo"] = True
    bot.callback_query.message.edit_text("Enter repo details:")

def user_submenu(bot, update):
    query = bot.callback_query
    query.answer()
    update.user_data["Repo"] = False
    bot.callback_query.message.edit_text("Enter user details:")

def main_menu_message():
  return 'Choose the search option:'

def start(update, context):
    context.user_data["Repo"] = True
    update.message.reply_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def help(update, context):    
    update.message.reply_text('You can search Github by repository or by user. Switch on the mode you need and type repository or user details')


def search(update, context):
    if context.user_data["Repo"] == True:    
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

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(repo_submenu, pattern='repo'))
    dp.add_handler(CallbackQueryHandler(user_submenu, pattern='user'))

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
