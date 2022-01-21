import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

details = []
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


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
    driver = webdriver.Firefox(executable_path='C:\\Users\\Sportg\\Desktop\\geckodriver.exe')
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

    update.message.reply_text(text=f'{details[3]}:'
                              f'\n{story(links)}'
                              f'\n{film_information(links)}')




# def inf(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(f'{details[3]}'
#                               f'\n')


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")