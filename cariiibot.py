#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pa' mi cari <3

import logging
from datetime import datetime
import threading
import os
from random import randint, getrandbits
import urllib
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram import Bot

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

# Dayly pic users
DAILY_PIC_USERS = {'send': -1, 'receive': -1}
DAILY_PIC_SAVE_PATH = ".daily-pics/stash/"
DAILY_PIC_SENT_PATH = ".daily-pics/sent/"

# LOGGING VARIABLES
LOG_SENT_MSGS = 0
LOG_SENT_DOCS = 0
LOG_INTERVAL = 3600

#######
# AUX #
#######

def daily_sender():
    return DAILY_PIC_USERS["send"]

def daily_receiver():
    return DAILY_PIC_USERS["receive"]

def is_daily_sender(update):
    return update.effective_chat.id == daily_sender()

def send_msg(update, msg, **kwargs):
    """Send text message"""

    global LOG_SENT_MSGS
    LOG_SENT_MSGS += 1
    # Markdown/HTML
    if kwargs and kwargs['parse_mode']: 
        update.message.reply_text(msg, parse_mode=kwargs['parse_mode'])
    else:
        update.message.reply_text(msg)

def send_doc(bot, update, doc, chat_id=False):
    """Send Document"""

    global LOG_SENT_DOCS
    LOG_SENT_DOCS += 1
    if chat_id:
        # Send to given chat
        bot.sendDocument(chat_id=chat_id, document = doc)
    else:
        # Use the update
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

#############
# DAILY PIC #
#############

def register_daily_pic_receive(bot, update):
    """Register new user if password checks out"""
    global DAILY_PIC_USERS
    sent_password = update.message.text.replace("/register_daily_pic_receive ", "")
    password = open('.daily-pic-passwd').read().rstrip()

    # Check if correct password
    if sent_password == password:
        if DAILY_PIC_USERS["receive"] < 0:
            # Register the user
            DAILY_PIC_USERS["receive"] = update.effective_chat.id
            # Save to file
            with open('.daily-pic-users', 'w') as f:
                json.dump(DAILY_PIC_USERS, f)
            # Send response
            send_msg(update, "You are now *registered* for *receiving* daily pics!", parse_mode='markdown')
        else:
            # There's a user already registered
            send_msg(update, "Sorry, there's already a user registered for receiving :(")
    else:
        # Wrong password
        send_msg(update, "Sorry, wrong password :)")

def register_daily_pic_send(bot, update):
    """Register new user if password checks out"""
    global DAILY_PIC_USERS
    sent_password = update.message.text.replace("/register_daily_pic_send ", "")
    password = open('.daily-pic-passwd').read().rstrip()

    # Check if correct password
    if sent_password == password:
        if DAILY_PIC_USERS["send"] < 0:
            # Register the user
            DAILY_PIC_USERS["send"] = update.effective_chat.id
            # Save to file
            with open('.daily-pic-users', 'w') as f:
                json.dump(DAILY_PIC_USERS, f)
            # Send response
            send_msg(update, "You are now *registered* for *sending* daily pics!", parse_mode='markdown')
        else:
            # There's a user already registered
            send_msg(update, "Sorry, there's already a user registered for sending :(")
    else:
        # Wrong password
        send_msg(update, "Sorry, wrong password :)")

def unregister_daily_pic_receive(bot, update):
    """Unregister receiver"""
    global DAILY_PIC_USERS
    sent_password = update.message.text.replace("/unregister_daily_pic_receive ", "")
    password = open('.daily-pic-passwd').read().rstrip()

    # Check if correct password
    if sent_password == password:
        if DAILY_PIC_USERS["receive"] == update.effective_chat.id:
            # Unregister the user
            DAILY_PIC_USERS["receive"] = -1
            # Save to file
            with open('.daily-pic-users', 'w') as f:
                json.dump(DAILY_PIC_USERS, f)
            # Send response
            send_msg(update, "You are now *unregistered* for *receiving* daily pics!", parse_mode='markdown')
        else:
            # Other user is registered
            send_msg(update, "You were not registered anyway :)")
    else:
        # Wrong password
        send_msg(update, "Sorry, wrong password :)")

def unregister_daily_pic_send(bot, update):
    """Unregister sender"""
    global DAILY_PIC_USERS
    sent_password = update.message.text.replace("/unregister_daily_pic_send ", "")
    password = open('.daily-pic-passwd').read().rstrip()

    # Check if correct password
    if sent_password == password:
        if is_daily_sender(update):
            # Unregister the user
            DAILY_PIC_USERS["send"] = -1
            # Save to file
            with open('.daily-pic-users', 'w') as f:
                json.dump(DAILY_PIC_USERS, f)
            # Send response
            send_msg(update, "You are now *unregistered* for *sending* daily pics!", parse_mode='markdown')
        else:
            # Other user is registered
            send_msg(update, "You were not registered anyway :)")
    else:
        # Wrong password
        send_msg(update, "Sorry, wrong password :)")

def init_daily_pic_users():
    """Read users file and set DAILY_PIC_USERS"""
    global DAILY_PIC_USERS
    # Check if registered users file exists
    if not os.path.isfile('.daily-pic-users'):
        register_file = open('.daily-pic-users', 'w+')
        register_file.write('{"send": -1, "receive": -1}')
        register_file.close()
        DAILY_PIC_USERS = {"send": -1, "receive": -1}
    else:
        with open('.daily-pic-users', 'r') as f:
            DAILY_PIC_USERS = json.load(f)

def handle_photo(bot, update):
    """Handle received photos"""
    logger.info("Received picture")
    if is_daily_sender(update):
        # Check if image is ment to be for daily pic use
        if update.message.caption == "daily_pic":
            # Get max resolution picture
            max_size_photo = update.message.photo[-1]
            # Save pic in stash (name will be its ID, leter used to send it from Telegram servers)
            max_size_photo.get_file().download(custom_path=DAILY_PIC_SAVE_PATH + str(max_size_photo.file_id))
            # Inform it was correctly saved
            send_msg(update, "Got it! :D")
        else:
            # Generic response, for the lolz
            send_msg(update, "Ok...")
    else:
        # Generic response, for the lolz
        send_msg(update, "Ok...")

def daily_send(bot):
    """Send a picture daily"""
    logger.info("Attempting to send daily pic")
    if daily_receiver() > 0:
        # There's a registered receiver, proceed to pick a pic and send
        daily_pic_path = get_daily_pic()
        # Check if there're images
        if daily_pic_path:
            #pic_to_send = open(DAILY_PIC_SAVE_PATH + daily_pic_path, 'rb')
            pic_to_send = str(daily_pic_path)
            bot.sendPhoto(chat_id=daily_receiver(), photo = pic_to_send, caption=build_morning())
            #pic_to_send.close()
            logger.info("Daily pic sent!")
            move_sent_pic(pic_to_send)
        else:
            # Alert sender that there're no images
            logger.warn("No daily pics :( Alerting sender!!")
            if daily_sender() != -1:
                bot.sendMessage(daily_sender(), "Hey daily sender, *YOU ARE OUT OF PICTURES!!!*", parse_mode='markdown')
    
    # Set timer for next day
    set_daily_send(bot)
    

def set_daily_send(bot):
    """Set send for next day"""
    x = datetime.today()
    # If last day of month, set to one
    try:
        y = x.replace(day=x.day+1, hour=9, minute=0, second=0, microsecond=0)
    except ValueError:
        # This handles month change (NOT YEAR CHANGE, hardly necessary tho...)
        y = x.replace(month=x.month+1, day=1, hour=9, minute=0, second=0, microsecond=0)
    delta_t = y-x

    secs=delta_t.seconds+1

    threading.Timer(secs, daily_send, [bot]).start()

def get_daily_pic():
    """Get a picture from daily pic stash"""
    # Get list of files
    pics_list = os.listdir(DAILY_PIC_SAVE_PATH)
    if pics_list != []:
        # Get the first and pic and send it
        return pics_list[0]
    else:
        return None

def move_sent_pic(pic):
    """Move sent picture to sent pictures"""
    os.rename(DAILY_PIC_SAVE_PATH + pic, DAILY_PIC_SENT_PATH + pic)

def build_morning():
    """Build a message based on morning-text and cariii-emojis"""

    # i's
    morning_msg = "Buenos dia"
    morning_msg += "a" * randint(0, 10)
    morning_msg += "s "

    # Emojis
    dice = randint(0, 2)
    if dice == 0:
        # single-long
        morning_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(3, 10)
    elif dice == 1:
        # couple-long-short
        morning_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(6, 10)
        morning_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)] * randint(1, 5)
    else:
        # party
        for _ in range(randint(10, 15)):
            morning_msg += CARIII_EMOJI[randint(0, len(CARIII_EMOJI) - 1)]

    return morning_msg

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
    # Initialise daily pic users
    init_daily_pic_users()

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
    dp.add_handler(CommandHandler("register_daily_pic_receive", register_daily_pic_receive))
    dp.add_handler(CommandHandler("register_daily_pic_send", register_daily_pic_send))
    dp.add_handler(CommandHandler("unregister_daily_pic_receive", unregister_daily_pic_receive))
    dp.add_handler(CommandHandler("unregister_daily_pic_send", unregister_daily_pic_send))


    # Handle noncommands
    dp.add_handler(MessageHandler(Filters.text, analyze_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    # log all errors
    dp.add_error_handler(error)

    # Jobs
    jq = updater.job_queue

    # Log usage
    jq.run_repeating(log_usage, LOG_INTERVAL)

    # Start the Bot
    updater.start_polling()

    # Start daily send
    bot = Bot(bot_token)
    set_daily_send(bot)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
