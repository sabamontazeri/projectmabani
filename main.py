import json
import requests
import os

url = 'https://api.telegram.org/bot5053445626:AAFqMUVL1DhaQ4gUncS7PqqGDlheJQs6HiI/'

from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
def get_all_updates():
    response = requests.get(url + 'getupdates')
    return response.json()

def get_last_update(allupdates):
    return allupdates['result'][-1]

def get_chat_id(update):
    return update['message']['chat']['id']

def sendmessage(chat_id, text):
    senddata = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendmessage', senddata)
    return response


# data = get_all_updates()
# lastupdate = get_last_update(data)
# sendmessage(get_chat_id(lastupdate), 'khobam')
# print()

@app.route('/', methods=['POST', 'GET'])
def index():
    msg = request.get_json()
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        if text == '/start':
            sendmessage(chat_id, 'khosh amadid')
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
                sendmessage(chat_id, 'shoma mokhatabi ndarid')
            else:
                for mokhatab in contacts[username]:
                    sendmessage(chat_id, mokhatab)
        return Response('ok', status=200)
    else:
        return '<h1>salam</h1>'

def write_json(data, filename='contactlist.json'):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)

def read_json(filename='contactlist.json'):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data


# while True:
#     a = get_last_update(get_all_updates())
#     if a['message']['text'] == 'salam':
#         sendmessage(get_chat_id(a), 'salam. khobi?')
write_json({})
app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))