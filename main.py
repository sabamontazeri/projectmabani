import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

details = []
interest_list = []
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def list(update: Update, context: CallbackContext) -> None:
    if len(interest_list) == 0:
        update.message.reply_text('لیست علاقه مندی های شما خالی است')
    else:
        update.message.reply_text(interest_list[0])


def type(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("فیلم", callback_data='movie'),
            InlineKeyboardButton("سریال", callback_data='series'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    bot_welcome = f'خوش آمدید.این ربات برای پیدا کردن فیلم مورد علاقه شما طراحی شده است. برای دیدن دستورالعمل این ربات از دستور مقابل استفاده کنید:' \
                  f'\n/help'

    update.message.reply_text(text=bot_welcome)
    keyboard = [
        [
            InlineKeyboardButton("ایران", callback_data='53'),
            InlineKeyboardButton("آمریکا", callback_data='54'),
        ],
        [InlineKeyboardButton("سایر", callback_data='63')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('به فیلم چه کشوری علاقه دارید؟', reply_markup=reply_markup)

def theme(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("کمدی", callback_data='کمدی'),
            InlineKeyboardButton("اکشن", callback_data='اکشن'),
        ],
        [InlineKeyboardButton("ترسناک", callback_data='ترسناک'),InlineKeyboardButton("درام",callback_data='درام')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f" you are interested in:{query.data}")

    details.append(query.data)
    # update.message.reply_text(text=details)

def inf(update: Update, context: CallbackContext) -> None:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(f'https://www.namava.ir/search?type={details[2]}&country={details[0]}&genre={details[1]}')

    movienames = []
    film = details[3]
    elements = driver.find_elements(By.TAG_NAME, 'img')

    for element in elements:
        movienames.append(element.get_attribute('title').strip())
    movienames = movienames[:10]

    # poster link of the film:
    x = movienames.index(film)
    photo = elements[x].get_attribute('src')


    everylinks = []

    def linkfilm(driver, everylinks):
        links = driver.find_elements(By.TAG_NAME, 'a')
        for item in links:
            eachlink = item.get_attribute('href')
            everylinks.append(eachlink)
        everylinks = everylinks[4:]
        return everylinks

    links = linkfilm(driver, everylinks)

    def story(links):
        eachlink = links[movienames.index(film)]
        driver.get(eachlink)
        content = driver.find_elements(By.CLASS_NAME, 'vertical-center')
        try:
            return re.findall(".*\n", content[1].text)[2]
        except:
            pass

    def film_information(links):
        eachlink = links[movienames.index(film)]
        driver.get(eachlink)
        content = driver.find_elements(By.CLASS_NAME, 'container')
        if details[0] == '53':
            try:
                return re.findall(".*\n", content[4].text)[1]
            except:
                pass
        else:
            try:
                return re.findall(".*\n", content[4].text)[2]
            except:
                pass

    keyboard = [
        [InlineKeyboardButton("افزودن به علاقه مندی ها", callback_data=film)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=f'{details[3]}:'
                              f'\n{story(links)}'
                              f'\n{film_information(links)}', reply_markup=reply_markup)


def button_0(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f" you are interested in:{query.data}")
    interest_list.append(query.data)


# def inf(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(f'{details[3]}'
#                               f'\n')


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")

TOKEN="5063146076:AAHxSfqMCw4VCwOH4KkvYEiCixtUBpiw9-I"
bot=Bot(token=TOKEN)
PORT = int(os.environ.get('PORT', '8443'))
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('list', list))
    updater.dispatcher.add_handler(CommandHandler('theme', theme))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('type', type))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('items', items))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('inf', inf))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_0))

    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_webhook(
        listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://pyth93bot.herokuapp.com/' + TOKEN
    )
    updater.idle()

from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def items(update: Update, context: CallbackContext) -> None:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(f'https://www.namava.ir/search?type={details[2]}&country={details[0]}&genre={details[1]}')

    movienames = []
    elements = driver.find_elements(By.TAG_NAME, 'img')

    for element in elements:
        movienames.append(element.get_attribute('title').strip())
    movienames = movienames[:10]

    x = ceil(len(movienames)/2)
    keyboard = []
    for i in range(5): # for i in range(x)
        keyboard.append([])
    for i in range(5): # for i in range(x)
        for j in range(2*i, 2*i+2):
            if j < 10: #len(movienames)
                keyboard[i].append(InlineKeyboardButton(movienames[j], callback_data=movienames[j]))

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose an item:', reply_markup=reply_markup)

if __name__ == '__main__':
    main()
