#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pa' mi cari <3

import logging
from random import randint
import urllib, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Cariii/Whatt resources
CARIII_TEXT = "Cari"
CARIII_EMOJI = ["😍", "😘", "😚", "🌝", "❤", "💕"]
WHAT_TEXT = ["Que?", "Si?", "kdise?", "Emmmmm... que?", "No entiendo 🤔", "🤡"]

# GYPHY resources
GIPHY_API_KEY = open('.giphy-api-key').read().rstrip()
GIPHY_API = 'https://api.giphy.com'
GIPHY_RAND_ENDP = '/v1/gifs/random'
KAWAII_TAG = 'kawaii'
KAWAII_RATING = 'PG-13'


# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

############
# COMMANDS #
############

def error(bot, update, error):
    """Logs any error"""
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    """Welcome message"""
    # TODO: Think a better welcome msg
    update.message.reply_text('Hola Cari!')

def help(bot, update):
    """Send help message"""
    # TODO: Write help
    update.message.reply_text('No puedo ayudarte :(')

def kawaii(bot, update):
    """Send kawaii GIF"""
    url = (GIPHY_API + GIPHY_RAND_ENDP + '?'
           'api_key=' + GIPHY_API_KEY + '&'
           'tag=' + KAWAII_TAG + '&'
           'rating=' + KAWAII_RATING)
    try:    
        # Get GIF url
        response = urllib.urlopen(url)
        json_response = json.loads(response.read())
        gif_url = json_response['data']['image_url']

        # Send GIF
        bot.sendDocument(chat_id=update.message.chat_id, document = gif_url)
    except:
        # Some error happended, can's send GIF
        update.message.reply_text('Me he quedado sin GIFs por ahora, lo siento :(')


################
# TEXT REPLIES #
################

def analyze_text(bot, update):
    """Analyze noncommand text and decide what to do"""
    reply = ''
    if 'cari'.lower() in update.message.text.lower():
        reply = build_cariii()
    else:
        reply = build_what()

    update.message.reply_text(reply)

def build_cariii():
    """Build a message based on cariii-text and cariii-emojis"""

    # i's
    cariii_msg = CARIII_TEXT
    cariii_msg += "i" * randint(0, 10)
    cariii_msg += " "

    # Emojis
    dice = randint(0, 2)
    if dice == 0:
        # single-long
        cariii_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(3, 10)
    elif dice == 1:
        # couple-long-short
        cariii_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(6, 10)
        cariii_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(1, 5)
    else:
        # party
        for _ in range(randint(10, 15)):
            cariii_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)]

    return cariii_msg

def build_what():
    """Build what message based on what_text"""
    return WHAT_TEXT[randint(0, len(WHAT_TEXT) - 1)]

def main():
    """Set up and start Bot"""

    # Read Bot Token
    bot_token = open('.telegram-token').read().rstrip()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("kawaii", kawaii))

    # Handle noncommands
    dp.add_handler(MessageHandler(Filters.text, analyze_text))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
