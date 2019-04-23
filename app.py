from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import psutil
import os
import sqlite3
import logging
from configparser import ConfigParser
APP_CONFIG = ConfigParser()
APP_CONFIG.read('config.ini')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

adminuserid = int(APP_CONFIG.get("telegram","admin_user_id"))
username = APP_CONFIG.get("telegram","username")
first_name = APP_CONFIG.get("telegram","first_name")
last_name = APP_CONFIG.get("telegram","last_name") 
bottoken = APP_CONFIG.get("telegram","api_key")
adminchat = {
    'id': adminuserid,
    'type': 'private',
     'username': username,
     'first_name': first_name,
'last_name': last_name
}
print(adminchat)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command.")
    bot.send_message(chat_id=adminuserid, text=str(update))


def start(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        print(bot)
        update.message.reply_text(
            "Hi "+update.message.from_user.first_name+"!")
    else:
        update.message.reply_text("I'm a Tony's Bot, Nice to meet you" +
                                  update.message.from_user.first_name+"! But has Tony asked you to use me?")
        bot.send_message(chat_id=adminuserid, text=str(update))

def serverstats(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        data = "Hostname : " + str(os.uname())
        update.message.reply_text(data)
        data = "CPU Percent : " + str(psutil.cpu_percent(1))
        update.message.reply_text(data)
        data = "CPU Frequenct : " + str(psutil.cpu_freq(percpu=True))
        update.message.reply_text(data)
        data = "Memory : "+str(psutil.virtual_memory())
        update.message.reply_text(data)
        data = "BootTime : " + str(psutil.boot_time())
        update.message.reply_text(data)
        data = "Users : " + str(psutil.users())
        update.message.reply_text(data)
    else:
        update.message.reply_text("You are not in Admin List you Hacker! XD")
        bot.send_message(chat_id=adminuserid, text=str(update))
        #bot.send_photo(chat_id=update.message.chat_id, photo=open(str(os.path.dirname(os.path.realpath(__file__)))+'/hacker.gif', 'rb'))


def serverstatjob(bot, update):
    data = "Hostname : " + str(os.uname())
    bot.send_message(chat_id=adminuserid, text=data)
    data = "CPU Percent : " + str(psutil.cpu_percent(1))
    bot.send_message(chat_id=adminuserid, text=data)
    data = "CPU Frequenct : " + str(psutil.cpu_freq(percpu=True))
    bot.send_message(chat_id=adminuserid, text=data)
    data = "Memory : "+str(psutil.virtual_memory())
    bot.send_message(chat_id=adminuserid, text=data)
    data = "BootTime : " + str(psutil.boot_time())
    bot.send_message(chat_id=adminuserid, text=data)
    data = "Users : " + str(psutil.users())
    bot.send_message(chat_id=adminuserid, text=data)

def jot(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        print("TO be implemented")


def main():
    updater = Updater(bottoken)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('serverstats', serverstats))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('jot', jot))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    j = updater.job_queue
    job_hourly = j.run_repeating(serverstatjob, interval=86400, first=0)
    updater.idle()


if __name__ == '__main__':
    main()
