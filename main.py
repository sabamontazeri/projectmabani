import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,ConversationHandler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
karbar=[]
mylist=''
first,second=range(2)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    bot_welcome = f'/help خوش آمدید.این ربات برای پیدا کردن فیلم مورد علاقه شما طراحی شده است. برای دیدن دستورالعمل این ربات از دستور مقابل استفاده کنید: '

    update.message.reply_text(text=bot_welcome)
    keyboard = [
        [
            InlineKeyboardButton("سربال ", callback_data='series')
        ],
        [InlineKeyboardButton("فیلم", callback_data='movie')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('فیلم یا سریال؟', reply_markup=reply_markup)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="انتخاب شد!")
    karbar.append(query.data)

    return first

def country(update: Update, context: CallbackContext):
    keyboard=[[
            InlineKeyboardButton("ایران🇮🇷 ", callback_data='53'),
            InlineKeyboardButton("آمریکا", callback_data='54'),
        ],
        [InlineKeyboardButton("هند", callback_data='59'),
         InlineKeyboardButton("سایر", callback_data='63')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('کشور مورد نظر خود را انتخاب کنید:', reply_markup=reply_markup)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="کشور انتخاب شد!")
    karbar.append(query.data)
    return second

def theme(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("کمدی", callback_data='comedy'),
            InlineKeyboardButton("اکشن", callback_data='action'),
        ],
        [InlineKeyboardButton("ترسناک", callback_data='horror'),InlineKeyboardButton("درام",callback_data='dramatic')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('کشور مورد نظر خود را انتخاب کنید:', reply_markup=reply_markup)

    query = update.callback_query
    query.answer()
    query.edit_message_text(text="کشور انتخاب شد!")
    karbar.append(query.data)

def end(update: Update, context: CallbackContext):

    for i in karbar:
        mylist+=f'{i} \n'
    update.message.reply_text(text=mylist)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f" you are interested in:{query.data}")
    details.append(query.data)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")
def suggesting(update: Update, context: CallbackContext):

    driver = webdriver.Chrome(executable_path='C:\\Users\\SABA\\Desktop\\chromedriver.exe')
    driver.get(f'https://www.namava.ir/search?type={karbar[0]}&country={karbar[1]}&genre={karbar[2]}')

    movienames = []
    elements = driver.find_elements(By.TAG_NAME, 'img')

    for element in elements:
        movienames.append(element.get_attribute('title').strip())
    print(movienames)

    # poster link of the film:
    x = movienames.index(film)
    photo = elements[x].get_attribute('src')
    print(photo)


everylinks = []
def linkfilm(driver, everylinks):
    links = driver.find_elements(By.TAG_NAME, 'a')
    for item in links:
        eachlink = item.get_attribute('href')
        everylinks.append(eachlink)
    everylinks = everylinks[4:]
    return everylinks


def story(links):
    eachlink = links[movienames.index(film)]
    driver.get(eachlink)
    content = driver.find_elements(By.CLASS_NAME, 'vertical-center')
    try:
        print(re.findall(".*\n", content[1].text)[2])
    except:
        pass



def film_information(links):
    eachlink = links[movienames.index(film)]
    driver.get(eachlink)
    content = driver.find_elements(By.CLASS_NAME, 'container')
    if karbar[1] == '53':
        try:
            print(re.findall(".*\n", content[4].text)[1])
        except:
            pass
    else:
        try:
            print(re.findall(".*\n", content[4].text)[2])
        except:
            pass

TOKEN="5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c"
bot=Bot(token=TOKEN)
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler=ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={first:[CallbackQueryHandler(country,pattern='^' + 'series' + '$'),
                 CallbackQueryHandler(country,pattern='^' + 'film' + '$')],
                 second:[CallbackQueryHandler(theme,pattern='^' + '53' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '54' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '59' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '63' + '$')]

        },
    fallbacks = [CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('end', end))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()