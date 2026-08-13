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
    config = json.load(file)
    HEADERS = config["headers"]
    URL = config["url"]
    BALE_TOKEN = config["BALE_TOKEN"]

bot = telebot.TeleBot(BALE_TOKEN)


@bot.message_handler(commands=["start"])
def start_menu(message):
    text = "به ربات ترجمه گر گوگل خوش آمدید"
    text += "\nاز منوی زیر زبان مورد نظر خود را برای ترجمه انتخواب کنید"

    markup = InlineKeyboardMarkup()

    en_button = InlineKeyboardButton("English 🇬🇧", callback_data="en")
    ja_button = InlineKeyboardButton("Japanese 🇯🇵", callback_data="ja")
    ru_button = InlineKeyboardButton("Russian 🇷🇺", callback_data="ru")
    ar_button = InlineKeyboardButton("Arabic 🇸🇦", callback_data="ar")
    ea_button = InlineKeyboardButton("spanish 🇪🇸", callback_data="es")
    de_button = InlineKeyboardButton("German 🇩🇪", callback_data="de")
    zh_button = InlineKeyboardButton("Chinese 🇨🇳", callback_data="zh")
    it_button = InlineKeyboardButton("italic 🇮🇹", callback_data="it")

    markup.add(en_button, de_button)
    markup.add(ea_button, ru_button)
    markup.add(ar_button, it_button)
    markup.add(ja_button, zh_button)

    bot.send_message(message.chat.id, text=text, reply_markup=markup)
    return


@bot.callback_query_handler(func=lambda call: True)
def call_handeling(call):
    data = call.data

    if data == "start":
        start_menu(call.message)
        return

    languages = {
        "en": ("انگلیسی", "en"),
        "ja": ("ژاپنی", "ja"),
        "ru": ("روسی", "ru"),
        "ar": ("عربی", "ar"),
        "es": ("اسپانیایی", "es"),
        "de": ("آلمانی", "de"),
        "zh": ("چینی", "zh"),
        "it": ("ایتالیایی", "it"),
    }

    if data not in languages:
        bot.answer_callback_query(call.id, "گزینه نامعتبر است.")
        return

    lang_name, target = languages[data]

    bot.send_message(
        call.message.chat.id,
        f"متن مورد نظر خود را برای ترجمه به *{lang_name}* ارسال کنید.",
        parse_mode="Markdown",
    )

    bot.register_next_step_handler(
        call.message, lambda message, target=target: send_result(message, target)
    )


def send_result(message, target):
    data = create_data(src="fa", tgt=target, txt=message.text)
    res = translate(data=data)

    if res == False:
        bot.send_message(message.chat.id, "خطایی پیش امده لطفا بعدا تلاش کنید❌")
        return

    bot.reply_to(
        message,
        res,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="start")
        ),
    )
    return


def translate(data):
    response = requests.post(URL, headers=HEADERS, json=data)

    if response.status_code != 200:
        return False

    return response.json()["result"]


def create_data(src, tgt, txt):
    return {"source": src, "target": tgt, "text": txt}


bot.infinity_polling()
