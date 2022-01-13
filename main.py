import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,ConversationHandler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
karbar=[]
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