"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
https://cryptic-waters-99444.herokuapp.com/ | https://git.heroku.com/cryptic-waters-99444.git
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def getTotal(userName):
    with open("solved.txt","r") as storage:
        for each_line in storage:
            print(each_line)
            user,total = each_line.split(":")
            if(user==userName):
                return total
    return -1
    
    
class ProblemSolver(object):
    def __init__(self,userName):
        self.userName = userName
        self.questionSolvedBefore = int(getTotal(self.userName))
        self.solvedToday = 0
        self.toPay = 0
        self.message = ""
    
    def getLeetCodeData(self):
        #api = "https://leetcode-stats-api.herokuapp.com/"
        #response = requests.get(api+self.userName)
        #print(response.json())
        #self.solvedToday = response.json()['totalSolved']
        totalSolved = 8
        return totalSolved
    
    #This function take userName and question solved till yesterday    
    def amountToPayToday(self):
        amount = 30
        total = self.getLeetCodeData()
        
        self.solvedToday = total - self.questionSolvedBefore
        self.toPay = 0 if self.solvedToday>0 else amount
        self.questionSolvedBefore +=self.solvedToday
        
    def getMessage(self):
        self.amountToPayToday()
        self.message = self.userName + "\n Solved Today: " + str(self.solvedToday) + "\n Amount Payable: " + str(self.toPay) + " Rs.\n"
        print(self.userName + " Solved Total " +  str(self.questionSolvedBefore) )
        return self.message

p1 = ProblemSolver('chiranjeetc40')
p2 = ProblemSolver('root_08')

def getStat():
    return p1.getMessage() + "\n" +p2.getMessage()
    
    
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
    
    sched.start()

if __name__ == '__main__':
    main()
    
    
# grop id: -1001707646893

#https://api.telegram.org/bot5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ/sendMessage?chat_id=-1001707646893&text=Hello%20World
#https://api.telegram.org/bot5127123865:AAGcz2awrdlO0btmItQE1PFV6WWZj99SfyQ/getUpdates

@sched.scheduled_job('cron',[[p1,p2]], day_of_week='mon-sun', hour=23)
def saveData(allUsers):
    with open("solved.txt","w") as storage:
        for each_user in allUsers:
            storage.write(each_user.userName+":"+str(each_user.questionSolvedBefore)+"\n")
            

'''
Stop crashing from bad command
create fix to run on local
'''