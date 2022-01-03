import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("ایران", callback_data='iran'),
            InlineKeyboardButton("آمریکا", callback_data='USA'),
        ],
        [InlineKeyboardButton("انگلستان", callback_data='england')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('به فیلم چه کشوری علاقه دارید؟', reply_markup=reply_markup)

def theme(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("کمدی", callback_data='comedy'),
            InlineKeyboardButton("اکشن", callback_data='action'),
        ],
        [InlineKeyboardButton("ترسناک", callback_data='horror'),InlineKeyboardButton("درام",callback_data='dramatic')],
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


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")

TOKEN="5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c"
bot=Bot(token=TOKEN)
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('theme', theme))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()