import logging
import os
from configparser import ConfigParser
from functools import cache

import psutil
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


@cache
def get_app_config(section: str, key: str) -> str:
    APP_CONFIG = ConfigParser()
    APP_CONFIG.read("config.ini")
    return APP_CONFIG.get(section=section, option=key)


def get_adminuserid() -> int:
    return int(get_app_config("telegram", "admin_user_id"))


def send_message_to_admin(message: str, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=get_adminuserid(), text=message)


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )
    send_message_to_admin(str(update), context)


def start(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) == str(get_adminuserid()):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hi {update.effective_user.full_name} !",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"I'm Tony's Bot, Nice to meet you{update.effective_user.first_name}!"
            f",But has {get_app_config('telegram', 'first_name')} asked you to use me?",
        )
        send_message_to_admin(str(update), context)


def serverstats(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) == str(get_adminuserid()):
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
        send_message_to_admin(data, context)

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not in Admin List you Hacker! XD",
        )
        send_message_to_admin(str(update), context)


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
    send_message_to_admin(data, context)


def main():
    updater = Updater(get_app_config("telegram", "api_key"))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("serverstats", serverstats))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), unknown))
    updater.start_polling()
    j = updater.job_queue
    j.run_repeating(serverstatjob, interval=86400, first=10)
    updater.idle()


if __name__ == "__main__":
    main()
