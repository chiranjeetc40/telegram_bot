"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
https://cryptic-waters-99444.herokuapp.com/ | https://git.heroku.com/cryptic-waters-99444.git
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

class ProblemSolver(object):
    def __init__(self,userName):
        self.userName = userName
        self.questionSolvedBefore = 0
        self.solvedToday = 0
        self.toPay = 0
        self.message = self.userName + " Solved today " + str(self.solvedToday) + " problem so he need to pay " + str(self.toPay) + " Rs."
    
    def getLeetCodeData(self):
        api = "https://leetcode-stats-api.herokuapp.com/"
        response = requests.get(api+self.userName)
    
        self.solvedToday = response.json()['totalSolved']
    
    #This function take userName and question solved till yesterday    
    def amountToPayToday(self):
        amount = 30
        self.getLeetCodeData(userName)
        self.toPay = 0 if ((self.solvedToday - self.questionSolvedBefore) > 0) else amount
        self.questionSolvedBefore += self.solvedToday
    
    def getMessage(self):
        self.amountToPayToday()
        return self.message


def getStat():
    p1 = ProblemSolver('chiranjeetc40')
    p2 = ProblemSolver('root_08')
    return p1.getMessage() + " " +p2.getMessage()
    
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def stat(update, context):
    message = getStat()
    update.message.reply_text(message)
    
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stat", stat))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://cryptic-waters-99444.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
    
    
# grop id: -1001707646893

#https://api.telegram.org/bot5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ/sendMessage?chat_id=-1001707646893&text=Hello%20World
#https://api.telegram.org/bot5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ/getUpdates


'''
Stop crashing from bad command
'''