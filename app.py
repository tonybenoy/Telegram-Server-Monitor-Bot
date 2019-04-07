from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
import psutil
import os

adminuserid = "You numeric user id"
username = "tonybenoy"
first_name = "Your First name"
last_name = "Your lastname"
bottoken = 'Your token'

chat= {
            'id': adminuserid,
            'type': 'private',
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
def start(bot, update):
	update.message.reply_text("I'm a bot, Nice to meet you!")

def test(bot,update):
	update["message"]["chat"]["username"]
	if str(update["message"]["chat"]) == str(chat):
		data="Hostname : "+str(os.uname())+"\nCPU Percent : "+str(psutil.cpu_percent(1))+"\nCPU Frequenct : "+str(psutil.cpu_freq(percpu=True))
		update.message.reply_text(data)
	else:
		update.message.reply_text("You are not in Admin List you Hacker! XD")
		
	
def main():
	updater = Updater(bottoken)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('test',test))
	start_handler = CommandHandler('start', start)
	dp.add_handler(start_handler)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

