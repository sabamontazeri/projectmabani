import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,ConversationHandler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
mylist=''
karbar=[]
first,second,third=range(3)
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
            InlineKeyboardButton("سریال ", callback_data='series')
        ],
        [InlineKeyboardButton("فیلم", callback_data='movie')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('فیلم یا سریال؟🎥', reply_markup=reply_markup)

    return first

def country(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard=[[
            InlineKeyboardButton("ایران🇮🇷 ", callback_data='53'),
            InlineKeyboardButton("آمریکا🇱🇷", callback_data='54'),
        ],
        [InlineKeyboardButton("هند🇮🇳", callback_data='59'),
         InlineKeyboardButton("سایر🌐", callback_data='63')],]
    reply_markup = InlineKeyboardMarkup(keyboard)


    query.edit_message_text(text="به سینمای کدام کشور علاقه دارید؟",reply_markup=reply_markup)
    karbar.append(query.data)
    return second

def theme(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("کمدی", callback_data='کمدی'),
            InlineKeyboardButton("اکشن", callback_data='اکشن'),
        ],
        [InlineKeyboardButton("ترسناک", callback_data='ترسناک'),InlineKeyboardButton("درام",callback_data='درام')],
        [InlineKeyboardButton("جنگی", callback_data='جنگی'),InlineKeyboardButton("عاشقانه",callback_data='عاشقانه')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="به کدام ژانر علاقه دارید؟🎭",reply_markup=reply_markup)
    karbar.append(query.data)
    return third

def end(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    karbar.append(query.data)
    update.callback_query.message.edit_text(text="ژانر مورد نظر شما انتخاب شد")

def inf(update: Update, context: CallbackContext) -> None:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(f'https://www.namava.ir/search?type={karbar[0]}&country={karbar[1]}&genre={karbar[2]}')

    movienames = []
    elements = driver.find_elements(By.TAG_NAME, 'img')

    for element in elements:
        movienames.append(element.get_attribute('title').strip())
    for i in movienames:
        text+=f'{i}\n'
    update.message.reply_text(text=text)



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
                 CallbackQueryHandler(country,pattern='^' + 'movie' + '$')],
                 second:[CallbackQueryHandler(theme,pattern='^' + '53' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '54' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '59' + '$'),
                         CallbackQueryHandler(theme,pattern='^' + '63' + '$')],
                 third:[CallbackQueryHandler(end,'^' + 'کمدی' + '$'),
                        CallbackQueryHandler(end,'^' + 'ترسناک' + '$'),
                        CallbackQueryHandler(end,'^' + 'جنگی' + '$'),
                        CallbackQueryHandler(end,'^' + 'درام' + '$'),
                        CallbackQueryHandler(end,'^' + 'عاشقانه' + '$'),
                        CallbackQueryHandler(end,'^' + 'اکشن' + '$')]

        },
    fallbacks = [CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('end', end))
    updater.dispatcher.add_handler(CommandHandler('inf', inf))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()