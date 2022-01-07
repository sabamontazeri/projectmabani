import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.chataction import ChatAction


TOKEN="5032556012:AAG0qZfT01Ni1-WNGh0AaIFVfndw9axhe0c"
bot=Bot(token=TOKEN)
updater = Updater(TOKEN)


def start(update: Update, context: CallbackContext) :

    chat_id=update.message.chat_id
    username=update.message.from_user.first_name
    userfamily=update.message.from_user.last_name
    if (userfamily==None):
        userfamily=' '
    bot.send_chat_action(chat_id,ChatAction.TYPING)
    bot.send_message(chat_id,f'سلام{userfamily}{username} \n به ربات فیلم یاب خوش آمدبد ')


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

    query.edit_message_text(text=f"Selected option: {query.data}")

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    start_command=CommandHandler('start',start)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()