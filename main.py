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


def get_last_update(allUpdates):
    return allUpdates['result'][-1]


def get_chat_id():
    return update.message.chat.id


def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response


@app.route('/', methods=['POST', 'GET'])
def index():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
          Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
          """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
# new AliBzh 067577
    elif 'new' in text:
        contacts = read_json()
        username = msg['message']['from']['username']
        if username not in contacts.keys():
            contacts[username] = []
        mokhatab = text.split(maxsplit=1)[1]
        contacts[username].append(mokhatab)
        write_json(contacts)
    elif text == 'list':
        contacts = read_json()
        username = msg['message']['from']['username']
        if username not in contacts.keys():
            sendMessage(chat_id, 'shoma mokhatabi nadarid')
        else:
            for mokhatab in contacts[username]:
                sendMessage(chat_id, mokhatab)
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

