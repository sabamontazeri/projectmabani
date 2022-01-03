url="https://api.telegram.org/bot5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c/"
import requests
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup,Message,Bot
from telegram.ext import Updater,CommandHandler,CallbackQueryHandler,CallbackContext
from flask import Response
import json
from flask import Flask
from flask import request
import os

TOKEN="5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c"
bot=Bot(token=TOKEN)

app = Flask(__name__)


def get_all_updates():
    response = requests.get(url + 'getUpdates')
    return response.json()

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def get_last_update(allUpdates):
    return allUpdates['result'][-1]




def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

@app.route('/', methods=['POST', 'GET'])
def index():
    updater = Updater("TOKEN")
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome ='خوش آمدید.سینما کدام کشور را می پسندید؟'
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

        keyboard = [
            [
                InlineKeyboardButton("ایران", callback_data='1'),
                InlineKeyboardButton("انگلستان", callback_data='2'),
            ],
            [InlineKeyboardButton("آمریکا", callback_data='3')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('لطفا انتخاب کنید', reply_markup=reply_markup)
        return Response('ok', status=200)
    else:
        return "<h2>myfirstbot</h2>"


def write_json(data, filename="contactList.json"):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json(filename="contactList.json"):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data

try:
    read_json()
except:
    write_json({})
app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))