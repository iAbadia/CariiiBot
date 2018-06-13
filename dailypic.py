#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Daily pic functionality.

from datetime import datetime
import threading
import os
from random import randint, getrandbits
import json
from telegram import Bot

from bothelper import send_msg, send_doc, logger

# Cariii/Whatt resources
DAILY_PIC_TEXT = "Buenos dia"
DAILY_PIC_EMOJI = ["😍", "😘", "😚", "🌞", "❤", "💕"]

#############
# DAILY PIC #
#############

# Dayly pic users
DAILY_PIC_USERS = {'send': -1, 'receive': -1}
DAILY_PIC_SAVE_PATH = ".daily-pics/stash/"
DAILY_PIC_SENT_PATH = ".daily-pics/sent/"

# Daily pic helper functions
def daily_sender():
    return DAILY_PIC_USERS["send"]

def daily_receiver():
    return DAILY_PIC_USERS["receive"]

def is_daily_sender(update):
    return update.effective_chat.id == daily_sender()

# Daily pic user initialisation
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

# Check number of available pics
def pic_stats(bot, update):
    """Check sent and tobe-sent pictures"""
    if is_daily_sender(update):
        # Check number of pictures
        stash_n = len(os.listdir(DAILY_PIC_SAVE_PATH))
        sent_n = len(os.listdir(DAILY_PIC_SENT_PATH))

        # Send msg
        stats = "I've *sent " + str(sent_n) + " pictures* and "
        stats += "I still have *" + str(stash_n) + " pictures stashed*."
        send_msg(update, stats, parse_mode='markdown')

# Daily pic register/unregister functions
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


# Daily pic timing/send functions
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

def handle_daily_send(update):
    """Handle daily pic sent"""
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
    

def set_daily_send(bot):
    """Set send for next day"""
    x = datetime.today()
    # If last day of month, set to one
    try:
        y = x.replace(day=x.day+1, hour=9, minute=0, second=0, microsecond=0)
    except ValueError:
        # This handles month change (NOT YEAR CHANGE, hardly necessary tho...)
        y = x.replace(month=x.month+1, day=1, hour=8, minute=0, second=0, microsecond=0)
    delta_t = y-x

    secs=delta_t.seconds+1

    t = threading.Timer(secs, daily_send, [bot])
    t.daemon = True
    t.start()

# Daily pic local image handling functions
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

# Build daily pic caption
def build_morning():
    """Build a message based on morning-text and cariii-emojis"""

    # a's
    morning_msg = DAILY_PIC_TEXT
    morning_msg += "a" * randint(0, 10)
    morning_msg += "s "

    # Emojis
    dice = randint(0, 2)
    if dice == 0:
        # single-long
        morning_msg += DAILY_PIC_EMOJI[randint(0, len(DAILY_PIC_EMOJI) - 1)] * randint(3, 10)
    elif dice == 1:
        # couple-long-short
        morning_msg += DAILY_PIC_EMOJI[randint(0, len(DAILY_PIC_EMOJI) - 1)] * randint(6, 10)
        morning_msg += DAILY_PIC_EMOJI[randint(0, len(DAILY_PIC_EMOJI) - 1)] * randint(1, 5)
    else:
        # party
        for _ in range(randint(10, 15)):
            morning_msg += DAILY_PIC_EMOJI[randint(0, len(DAILY_PIC_EMOJI) - 1)]

    return morning_msg
