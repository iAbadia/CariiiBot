#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pa' mi cari <3

import logging
from random import randint, getrandbits
import urllib
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job

# Cariii/Whatt resources
CARIII_TEXT = "Cari"
CARIII_EMOJI = ["😍", "😘", "😚", "🌝", "❤", "💕"]
WHAT_TEXT = ["Que?", "Si?", "?", "Emmmmm... que?", "No entiendo 🤔", "🤡"]

# GYPHY resources
GIPHY_API_KEY = open('.giphy-api-key').read().rstrip()
GIPHY_API = 'https://api.giphy.com'
GIPHY_RAND_ENDP = '/v1/gifs/random'
GIPHY_RATING = 'PG-13'
KAWAII_TAG = 'kawaii'
ANIMALITOS_TAG = 'animals'

# LOGGING VARIABLES
LOG_SENT_MSGS = 0
LOG_SENT_DOCS = 0
LOG_INTERVAL = 3600

#######
# AUX #
#######
def send_msg(update, msg, **kwargs):
    """Send text message"""

    global LOG_SENT_MSGS
    LOG_SENT_MSGS += 1
    # Markdown/HTML
    if kwargs and kwargs['parse_mode']: 
        update.message.reply_text(msg, parse_mode=kwargs['parse_mode'])
    else:
        update.message.reply_text(msg)

def send_doc(bot, update, doc):
    """Send Document"""

    global LOG_SENT_DOCS
    LOG_SENT_DOCS += 1
    bot.sendDocument(chat_id=update.message.chat_id, document = doc)

def log_usage(bot, job):
    """Log Bot usage"""

    global LOG_SENT_DOCS, LOG_SENT_MSGS, log_thread
    logger.info('USAGE: Sent messages: %d | Sent Docs: %d | Total sent: %d' %(LOG_SENT_MSGS, LOG_SENT_DOCS, LOG_SENT_MSGS+LOG_SENT_DOCS))

class GiphyRandomRequest(object):

    def __init__(self, api_key, tag, rating, query):
        if not api_key:
            logger.warn('GiphyRandomRequest: No API key provided')
            return
        self.api_key = api_key
        self.tag = tag
        self.rating = rating

        if query:
            self.query()
    
    def query(self):
        url = GIPHY_API + GIPHY_RAND_ENDP + '?'
        # Check for API key
        if not self.api_key:
            logger.warn('GiphyRandomRequest<query()>: No API key provided')
            return
        # Add API key
        url += 'api_key=' + self.api_key + '&'
        # Add tag if provided
        if self.tag:
            url += 'tag=' + self.tag + '&'
        # Add rating if provided
        if self.rating:
            url += 'rating=' + self.rating + '&'
        # Indicate JSON
        url += 'fmt=json'

        # Do the query
        try:    
            # Get GIF url
            response = urllib.urlopen(url)
            self.gif_json = json.loads(response.read())
        except:
            # Some error happended, can's send GIF
            logger.error('GiphyRandomRequest<query>: Error ocurred while requesting GIF.')

    def get_gif_url(self):
        if self.gif_json:
            return self.gif_json['data']['image_url']
        else:
            return None

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
    welcome_message = 'Hola Cari!'
    send_msg(update, welcome_message)

def help(bot, update):
    """Send help message"""
    # TODO: Write help
    help_msg = 'Prueba un comando!\n  /kawaii\n  /anims\n  /pistoleros'
    send_msg(update, help_msg, parse_mode='markdown')

def kawaii(bot, update):
    """Send kawaii GIF"""
    # Get GIF url
    gif_url = GiphyRandomRequest(GIPHY_API_KEY, 
                                 KAWAII_TAG, 
                                 GIPHY_RATING, 
                                 True).get_gif_url()
    # Check if you got the url
    if gif_url:
        # Send GIF
        send_doc(bot, update, gif_url)
    else:
        # Some error happended, can's send GIF
        send_msg(update, 'Me he quedado sin GIFs por ahora, lo siento :(')

def animals(bot, update):
    """Send animals GIF"""
    cutefunny = ''
    # Cute or funny
    if bool(getrandbits(1)):
        # Cute!
        cutefunny = 'cute'
    else:
        # Funny!
        cutefunny = 'funny'
    # Get GIF url
    gif_url = GiphyRandomRequest(GIPHY_API_KEY, 
                                 cutefunny + '+' + ANIMALITOS_TAG, 
                                 GIPHY_RATING, 
                                 True).get_gif_url()
    # Check if you got the url
    if gif_url:
        # Send GIF
        send_doc(bot, update, gif_url)
    else:
        # Some error happended, can's send GIF
        send_msg(update, 'Me he quedado sin GIFs por ahora, lo siento :(')

def pistoleros(bot, update):
    """Send the archifamous Pistoleros del Eclipse vid"""
    pistoleros_url = 'https://www.youtube.com/watch?v=8VRRI2FkRl8'
    send_msg(update, pistoleros_url)


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

    send_msg(update, reply)

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
    dp.add_handler(CommandHandler("anims", animals))
    dp.add_handler(CommandHandler("pistoleros", pistoleros))



    # Handle noncommands
    dp.add_handler(MessageHandler(Filters.text, analyze_text))

    # log all errors
    dp.add_error_handler(error)

    # Jobs
    jq = updater.job_queue

    # Log usage
    jq.run_repeating(log_usage, LOG_INTERVAL)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
