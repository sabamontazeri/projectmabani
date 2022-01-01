url="https://api.telegram.org/bot5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c/"
import requests
from flask import Response
import json
from flask import Flask
from flask import request
import os


app = Flask(__name__)


def get_all_updates():
    response = requests.get(url + 'getUpdates')
    return response.json()


def get_last_update(allUpdates):
    return allUpdates['result'][-1]


def get_chat_id(update):
    return update['message']['chat']['id']



def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        if text == '/start':
            sendMessage(chat_id, "khosh Aadid!!")
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

