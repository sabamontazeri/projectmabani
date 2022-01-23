import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,ConversationHandler
import requests
import re
from bs4 import BeautifulSoup
import os

global xt
xt=''
global fave
fave=[]
global dict
dict = {}
first,second,third,fourth,five=range(5)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    global karbar
    global chat_id
    chat_id=update.message.chat_id
    if chat_id not in dict.keys():
        dict[chat_id]=[]
    karbar = []
    """Sends a message with three inline buttons attached."""
    bot_welcome = f'/help خوش آمدید.این ربات برای پیدا کردن فیلم مورد علاقه شما طراحی شده است. برای دیدن دستورالعمل این ربات از دستور مقابل استفاده کنید: '

    update.message.reply_text(text=bot_welcome)
    keyboard = [
        [
            InlineKeyboardButton("لیست علاقه مندی ها ", callback_data='favorite')
        ],
        [InlineKeyboardButton("فیلم و سریال", callback_data='movie')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('گزینه مورد نظر شما کدام است؟🎥', reply_markup=reply_markup)

    return first

def country(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard=[[
            InlineKeyboardButton("ایران🇮🇷 ", callback_data='53')]]
    reply_markup = InlineKeyboardMarkup(keyboard)


    query.edit_message_text(text="به سینمای کدام کشور علاقه دارید؟",reply_markup=reply_markup)
    karbar.append(query.data)
    return third

def theme(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("کمدی", callback_data='comedy'),
            InlineKeyboardButton("اکشن", callback_data='action'),
        ],
        [InlineKeyboardButton("ترسناک", callback_data='horror'),InlineKeyboardButton("خانوادگی",callback_data='family')],
        [InlineKeyboardButton("مستند", callback_data='documentary'),InlineKeyboardButton("عاشقانه",callback_data='romance')],
        [InlineKeyboardButton("انیمیشن", callback_data='animated'),
         InlineKeyboardButton("تاریخی", callback_data='historic')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="به کدام ژانر علاقه دارید؟🎭",reply_markup=reply_markup)
    karbar.append(query.data)
    return second

def end(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    karbar.append(query.data)
    update.callback_query.message.edit_text(text="ژانر مورد نظر شما انتخاب شد")
def button(update: Update, context: CallbackContext) -> None:
    global film
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"گزینه مورد نظر: {query.data}")
    global fl
    global film
    fl=query.data
    if not fl.isalpha():
        film=fl
    else:
        if fl=='yes':
            if film not in dict[chat_id]:
                dict[chat_id].append(film)



def list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    global movienames
    page = requests.get(f'https://www.televika.com/tag/{karbar[1]}')
    soup = BeautifulSoup(page.text, 'html.parser')
    movienames=[]
    b=soup.find_all('img',class_='ds-media_image lazyload lazyloading')
    for item in b:
        movienames.append(item['title'])
    movienames = movienames[3:13]


    keyboard = []
    for i in range(5):
        keyboard.append([])
    for i in range(5):
        for j in range(2 * i, 2 * i + 2):
            if j < 10:
                try:
                    keyboard[i].append(InlineKeyboardButton(movienames[j], callback_data=movienames[j]))
                except:
                    pass
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text('یک فیلم را انتخاب کنید:', reply_markup=reply_markup)
    global everylinks
    global linkss
    linkss=[]
    everylinks=[]
    links=soup.find_all('a',class_='overlay--transparent')
    for i in range(len(links)):
        eachlink=links[i]['href']
        everylinks.append(eachlink)
    for i in everylinks:
        if i not in linkss:
            linkss.append(i)
    linkss=linkss[3:13]
    return fourth

def story(update: Update, context: CallbackContext):
    eachlink=linkss[movienames.index(film)]
    link=requests.get(eachlink)
    soups=BeautifulSoup(link.text,'html.parser')
    stories=soups.find_all('p',class_='toTruncate ps-relative short-description')
    if not stories==[] :
        s=stories[0]
        keyboard = [[InlineKeyboardButton("👍", callback_data='👍'), InlineKeyboardButton("👎", callback_data='👎')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=s.text,reply_markup=reply_markup)




def actors(update: Update, context: CallbackContext):
    eachlink=linkss[movienames.index(film)]
    link=requests.get(eachlink)
    soups=BeautifulSoup(link.text,'html.parser')
    actors=soups.find_all('div',class_="actors-item is-iran")
    x=''
    for item in actors:
        if not item.text=='':
            x+=f'{item.text}\n'
    lines = x.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]

    string_without_empty_lines = ""
    for line in non_empty_lines:
        string_without_empty_lines += line + "\n"

    print(string_without_empty_lines)
    keyboard = [[InlineKeyboardButton("👍", callback_data='👍'), InlineKeyboardButton("👎", callback_data='👎')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=string_without_empty_lines,reply_markup=reply_markup)
def crews(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    eachlink=linkss[movienames.index(film)]
    link=requests.get(eachlink)
    soups=BeautifulSoup(link.text,'html.parser')
    crews=soups.find_all('div',class_="other-crew_img")
    jobs=soups.find_all('h3',class_="crew-title other-crew_name truncate")
    mytext=''
    listt=[]
    for job in jobs:
        listt.append(job.text)
    for div in crews:
        for img in div.find_all('img', alt=True):
            t=img['alt']
            listt.append(t)
    for i in range(int(len(listt)*0.5)):
        mytext+=f'{listt[i]}:{listt[i+int(len(listt)*0.5)]}\n'
    bot.send_message(chat_id=chat_id,text=mytext)


def photourl(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    eachlink = linkss[movienames.index(film)]
    link = requests.get(eachlink)
    soups = BeautifulSoup(link.text, 'html.parser')
    photos = soups.find_all('img', class_="ds-media_image lazyload lazyloading")
    print(photos[0]['data-src'])
    keyboard = [[InlineKeyboardButton("👍", callback_data='👍'), InlineKeyboardButton("👎", callback_data='👎')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendPhoto(chat_id=chat_id,photo=photos[0]['data-src'],caption='پوستر فیلم مورد نظر شما📺:')
    update.message.reply_text('آیا این فیلم را می پسندید؟', reply_markup=reply_markup)
def favorite(update: Update, context: CallbackContext):
    keyboard=[[InlineKeyboardButton("yes", callback_data='yes'),InlineKeyboardButton("no", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('آیا این فیلم را می پسندید؟', reply_markup=reply_markup)

    dict[chat_id].append(film)
def showlist(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    text=''
    if dict[chat_id]==[]:
        query.edit_message_text(text=f"در حال حاضر فیلم مورد علاقه ای ندارید")
    else:
        for i in dict[chat_id]:
            text+=f'{i}\n'
        query.edit_message_text(text=text)

def butt(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    answ=query.data
    if answ=='yes':
        fave.append(film)
    else:
        pass
def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("/photourl پوستر را به شما میدهد\n/story داستان را به شما میدهد\n/crews عوامل را به شما میدهد\n /actors پوستر را به شما میدهد\n /showlist لیست علاقه مندی را به شما میدهد")
karbar=[]
TOKEN="5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c"
bot=Bot(token=TOKEN)
PORT = int(os.environ.get('PORT', '8443'))
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler=ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={first:[CallbackQueryHandler(theme,pattern='^' + 'movie' + '$'),
                 CallbackQueryHandler(showlist,pattern='^' + 'favorite' + '$')],
                 second:[    CallbackQueryHandler(country, '^' + 'comedy' + '$'),
                            CallbackQueryHandler(country, '^' + 'horror' + '$'),
                            CallbackQueryHandler(country, '^' + 'documentary' + '$'),
                            CallbackQueryHandler(country, '^' + 'family' + '$'),
                            CallbackQueryHandler(country, '^' + 'romance' + '$'),
                            CallbackQueryHandler(country, '^' + 'action' + '$'),
                             CallbackQueryHandler(country, '^' + 'animated' + '$'),
                             CallbackQueryHandler(country, '^' + 'historic' + '$')],
                 third:[CallbackQueryHandler(list,pattern='^' + '53' + '$')],

        },
    fallbacks = [CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('end', end))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('story', story))
    updater.dispatcher.add_handler(CallbackQueryHandler(butt))
    updater.dispatcher.add_handler(CommandHandler('photourl',photourl))

    updater.dispatcher.add_handler(CommandHandler('actors', actors))
    updater.dispatcher.add_handler(CommandHandler('crews', crews))
    updater.dispatcher.add_handler(CommandHandler('favorite', favorite))

    updater.dispatcher.add_handler(CommandHandler('showlist', showlist))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_webhook(
        listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://pyth93bot.herokuapp.com/' + TOKEN
    )

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()