from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import psutil
import os
import sqlite3
import logging
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime
import sentry_sdk
from time import mktime
import feedparser
import ast
from configparser import ConfigParser

APP_CONFIG = ConfigParser()
APP_CONFIG.read("config.ini")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

adminuserid = int(APP_CONFIG.get("telegram", "admin_user_id"))
username = APP_CONFIG.get("telegram", "username")
first_name = APP_CONFIG.get("telegram", "first_name")
last_name = APP_CONFIG.get("telegram", "last_name")
bottoken = APP_CONFIG.get("telegram", "api_key")
adminchat = {
    "id": adminuserid,
    "type": "private",
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
}
ytsids = ast.literal_eval(APP_CONFIG.get("telegram", "yts_ids"))
sentry = APP_CONFIG.get("telegram", "sentry")


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Sorry, I didn't understand that command."
    )
    bot.send_message(chat_id=adminuserid, text=str(update))


def start(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        update.message.reply_text("Hi " + update.message.from_user.first_name + "!")
    else:
        update.message.reply_text(
            "I'm Tony's Bot, Nice to meet you"
            + update.message.from_user.first_name
            + "! But has Tony asked you to use me?"
        )
        bot.send_message(chat_id=adminuserid, text=str(update))


def serverstats(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        data = (
            "\nHostname : "
            + str(os.uname())
            + "\nCPU Percent : "
            + str(psutil.cpu_percent(1))
            + "\nCPU Frequency : "
            + str(psutil.cpu_freq(percpu=True))
        )
        data += (
            "Memory : "
            + str(psutil.virtual_memory())
            + "BootTime : "
            + str(psutil.boot_time())
            + "\nUsers : "
            + str(psutil.users())
        )
        update.message.reply_text(data)

    else:
        update.message.reply_text("You are not in Admin List you Hacker! XD")
        bot.send_message(chat_id=adminuserid, text=str(update))
    bot.send_message(chat_id=adminuserid, text="Over and Out!")
    # bot.send_photo(chat_id=update.message.chat_id, photo=open(str(os.path.dirname(os.path.realpath(__file__)))+'/hacker.gif', 'rb'))


def serverstatjob(bot, update):
    data = (
        "\nHostname : "
        + str(os.uname())
        + "\nCPU Percent : "
        + str(psutil.cpu_percent(1))
        + "\nCPU Frequency : "
        + str(psutil.cpu_freq(percpu=True))
    )
    data += (
        "Memory : "
        + str(psutil.virtual_memory())
        + "BootTime : "
        + str(psutil.boot_time())
        + "\nUsers : "
        + str(psutil.users())
    )
    bot.send_message(chat_id=adminuserid, text=data)
    bot.send_message(chat_id=adminuserid, text="Over and Out!")


def ytsjob(bot, update):
    for item in ytsids:
        for movies in yts(8):
            bot.send_message(chat_id=item, text=movies)
        bot.send_message(chat_id=item, text="Peaceout!")


def yts(ranking):
    url = "https://yts.am/rss/0/all/all/" + str(ranking)
    movie = {}
    movies = []
    feed = feedparser.parse(url)
    for post in feed.entries:
        timestamp = datetime.fromtimestamp(mktime(post.published_parsed)).strftime(
            "%m/%d/%Y, %H:%M:%S"
        )
        soup = BeautifulSoup(post.summary, "html.parser")
        for br in soup.findAll("br"):
            next_s = br.nextSibling
            if not (next_s and isinstance(next_s, NavigableString)):
                continue
            next2_s = next_s.nextSibling
            if next2_s and isinstance(next2_s, Tag) and next2_s.name == "br":
                text = str(next_s).strip()
                if text:
                    movie.update({next_s.split(":")[0]: next_s.split(":")[1]})
            movie.update(
                {
                    "title": post.title,
                    "url": post.links[0].href,
                    "torrent": post.links[1].href
                    if post.links[1].type == "application/x-bittorrent"
                    else "Not found",
                    "timestamp": timestamp,
                }
            )
        movies.append(
            "Title : "
            + movie["title"]
            + "\nURL : "
            + movie["url"]
            + "\nTorrent : "
            + movie["torrent"]
            + "\nTime of Upload : "
            + movie["timestamp"]
        )
    return movies


def jot(bot, update):
    if str(update["message"]["chat"]) == str(adminchat):
        print("TO be implemented")


def main():
    sentry_sdk.init(sentry)
    updater = Updater(bottoken)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("serverstats", serverstats))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("jot", jot))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    j = updater.job_queue
    job_hourly = j.run_repeating(serverstatjob, interval=86400, first=0)
    job_hourly2 = j.run_repeating(ytsjob, interval=86400, first=0)
    updater.idle()


if __name__ == "__main__":
    main()
