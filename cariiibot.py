#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pa' mi cari <3

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from random import randint

cariii_text = "Cari"
cariii_emoji = ["😍", "😘", "😚", "🌝", "❤", "💕"]
what_text = ["Que?", "Si?", "kdise?", "Emmmmm... que?", "No entiendo 🤔", "🤡"]

update_id = None

def main():
    global update_id
    
    # Telegram Bot Authorization Token
    bot = telegram.Bot(open('.telegram-token').read().rstrip())

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            cariii(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def cariii(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        
        # Reply to the message
        if not update.message:
            pass
        elif "cari".lower() in update.message.text.lower():
            update.message.reply_text(build_cariii())
        else:
            update.message.reply_text(build_what())

def build_cariii():
    # Build a message based on cariii-text and cariii-emojis

    # i's
    cariii_msg = cariii_text
    cariii_msg += "i" * randint(0, 10)
    cariii_msg += " "

    # Emojis
    dice = randint(0, 2)
    if dice == 0:
        # same-long
        cariii_msg += cariii_emoji[randint(0, len(cariii_emoji) - 1)] * randint(3, 10)
    elif dice == 1:
        # couple-long-short
        cariii_msg += cariii_emoji[randint(0, len(cariii_emoji) - 1)] * randint(6, 10)
        cariii_msg += cariii_emoji[randint(0, len(cariii_emoji) - 1)] * randint(1, 5)
    else:
        # party
        for x in range(randint(10, 15)):
            cariii_msg += cariii_emoji[randint(0, len(cariii_emoji) - 1)]

    return cariii_msg

def build_what():
    return what_text[randint(0, len(what_text) - 1)]

if __name__ == '__main__':
    main()