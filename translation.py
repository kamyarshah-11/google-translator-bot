import requests
import json
import telebot
import logging
from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telebot import apihelper

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# برای ااتصال مجدد ربات به تلگرام از TOKEN اسفاده کنید
# و apihelper را پاک کنید
apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
apihelper.FILE_URL = "https://tapi.bale.ai/file/bot{0}/{1}"

with open(
    "C:\\Users\\ASUS\\Desktop\\Kamyar Documents\\coding\\python\\translation\\key.json",
    "r",
    encoding="utf-8",
) as file:
    HEADERS = json.load(file)["headers"]
    URL = json.load(file)["url"]
    BALE_TOKEN = json.load(file)["BALE_TOKEN"]

bot = telebot.TeleBot(BALE_TOKEN)


def translate(data):
    response = requests.post(URL, headers=HEADERS, json=data)

    if response.status_code != 200:
        return False

    return response.json()["result"]


def create_data(src, tgt, txt):
    return {"source": src, "target": tgt, "text": txt}


bot.infinity_polling()
    