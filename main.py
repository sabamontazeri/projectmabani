import json
import requests

url = 'https://api.telegram.org/bot5053445626:AAFqMUVL1DhaQ4gUncS7PqqGDlheJQs6HiI/'

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


data = get_all_updates()
lastupdate = get_last_update(data)
sendmessage(get_chat_id(lastupdate), 'khobam')
print()


def write_json(data, filename='contactlist.json'):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)

def read_json(filename='contactlist.json'):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data


while True:
    a = get_last_update(get_all_updates())
    if a['message']['text'] == 'salam':
        sendmessage(get_chat_id(a), 'salam. khobi?')
