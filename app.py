import ast
import logging
import os
from configparser import ConfigParser
from datetime import datetime
from time import mktime
from typing import Dict, List

import feedparser
import psutil
from bs4 import BeautifulSoup, NavigableString, Tag
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

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


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )
    context.bot.send_message(chat_id=adminuserid, text=str(update))


def start(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) == str(adminuserid):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hi " + update.effective_user.full_name + "!",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"I'm Tony's Bot, Nice to meet you{update.effective_user.first_name}!"
            ",But has {first_name} asked you to use me?",
        )
        context.bot.send_message(chat_id=adminuserid, text=str(update))


def serverstats(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) == str(adminuserid):
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
        context.bot.send_message(chat_id=update.effective_chat.id, text=data)

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not in Admin List you Hacker! XD",
        )
        context.bot.send_message(chat_id=adminuserid, text=str(update))
    context.bot.send_message(chat_id=adminuserid, text="Over and Out!")


def serverstatjob(context: CallbackContext) -> None:
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
    context.bot.send_message(chat_id=adminuserid, text=data)
    context.bot.send_message(chat_id=adminuserid, text="Over and Out!")


def ytsjob(context: CallbackContext) -> None:
    for item in ytsids:
        for movies in yts(8):
            context.bot.send_message(chat_id=item, text=movies)
        context.bot.send_message(chat_id=item, text="Peaceout!")


def yts(ranking: float) -> List[Dict[str, str]]:
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


def main():
    updater = Updater(bottoken)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("serverstats", serverstats))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), unknown))
    updater.start_polling()
    j = updater.job_queue
    j.run_repeating(serverstatjob, interval=20, first=10)
    j.run_repeating(ytsjob, interval=10, first=10)
    updater.idle()


if __name__ == "__main__":
    main()
