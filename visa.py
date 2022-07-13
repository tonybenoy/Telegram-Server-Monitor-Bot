# flake8: noqa

import datetime
import re
from typing import List, Tuple

import bs4
import requests
from telegram import Update
from telegram.ext import CallbackContext


def persist_cookie_for_visa(update: Update, context: CallbackContext):
    context.user_data["cookie"] = "".join(context.args)
    from app import get_adminuserid

    if update.effective_user.id == get_adminuserid():
        context.bot_data["cookie"] = "".join(context.args)
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie Persisted for bot"
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie Persisted"
        )


def visa_debug_true(update: Update, context: CallbackContext):
    context.bot_data["debugVisaJob"] = True
    context.bot.send_message(chat_id=update.effective_user.id, text="Set to True")


def visa_debug_false(update: Update, context: CallbackContext):
    context.bot_data["debugVisaJob"] = False
    context.bot.send_message(chat_id=update.effective_user.id, text="Set to False")


def check_slot(update: Update, context: CallbackContext):
    cookie = context.user_data["cookie"]
    if not cookie:
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie not found"
        )
    slots, worked = run_visa_slots(cookie)
    if not worked:
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie expired"
        )
    slots = "\n".join([slot.strftime("%m/%d/%Y") for slot in slots])
    context.bot.send_message(
        chat_id=update.effective_user.id, text=f"Available Slots:{slots} "
    )


def check_my_slots(update: Update, context: CallbackContext):
    startDate = datetime.date.today()
    endDate = datetime.datetime.strptime("2022/08/19", "%Y/%m/%d").date()
    cookie = context.user_data["cookie"]
    if not cookie:
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie not found"
        )
    slots, worked = run_visa_slots(cookie)
    if not worked:
        context.bot.send_message(
            chat_id=update.effective_user.id, text="Cookie expired"
        )
    for slot in slots:
        if slot > startDate and slot < endDate:
            context.bot.send_message(
                chat_id=update.effective_user.id,
                text=f"Available Slot:{slot.strftime('%m/%d/%Y')}",
            )


def run_visa_slots(cookie: str) -> Tuple[List, bool]:
    url = "https://broneering.mfa.ee/en"
    cookies = {"Cookie": cookie}
    payload = ""
    from app import get_app_config

    proxies = {
        "http": f"http://scraperapi:{get_app_config('proxy','APIKEY')}@proxy-server.scraperapi.com:8001"
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "https://broneering.mfa.ee/en/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="103", ".Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
    }
    response = requests.request(
        "GET",
        url,
        data=payload,
        headers=headers,
        allow_redirects=True,
        cookies=cookies,
        proxies=proxies,
    )
    bs = bs4.BeautifulSoup(response.text, "html.parser")
    script = bs.find_all("script")[-1]
    dates = re.findall("\d\d\d\d/\d\d/\d\d", str(script))
    if not dates:
        return [], False
    check_dates = []
    for date in dates:
        date_time_obj = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        if date_time_obj.year == 2022 and date_time_obj.month in (7, 8):
            check_dates.append(date_time_obj)
    return check_dates, True


def check_slots_periodically(context: CallbackContext) -> None:
    from app import send_message_to_admin

    if context.bot_data["debugVisaJob"]:
        send_message_to_admin("Yes it's working", context)
    cookie = context.bot_data["cookie"]
    if not cookie:
        send_message_to_admin("Cookie not found", context)
    slots, worked = run_visa_slots(cookie)
    if not worked:
        send_message_to_admin("Cookie expired", context)

    startDate = datetime.date.today()
    endDate = datetime.datetime.strptime("2022/08/19", "%Y/%m/%d").date()
    for slot in slots:
        if slot > startDate and slot < endDate:
            send_message_to_admin(
                f"Available Slot:{slot.strftime('%m/%d/%Y')}", context
            )
    if context.bot_data["debugVisaJob"]:
        send_message_to_admin("Yes it's working,completed", context)
