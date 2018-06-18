#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pa' mi cari <3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram import Bot

from bothelper import send_msg, send_doc, logger, LOG_INTERVAL, log_usage
from cariii import kawaii, animals, pistoleros, build_cariii, build_what
from dailypic import (register_daily_pic_receive, register_daily_pic_send,
                      unregister_daily_pic_receive, unregister_daily_pic_send,
                      is_daily_sender, init_daily_pic_users, set_daily_send,
                      handle_daily_send, pic_stats, pic_time)

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


######################
# HANDLE NONCOMMANDS #
######################

def analyze_text(bot, update):
    """Analyze noncommand text and decide what to do"""
    reply = ''
    if 'cari'.lower() in update.message.text.lower():
        reply = build_cariii()
    else:
        reply = build_what()

    send_msg(update, reply)

def handle_photo(bot, update):
    """Handle received photos"""
    logger.info("Received picture")
    if is_daily_sender(update):
        handle_daily_send(update)
    else:
        # Generic response, for the lolz
        send_msg(update, "Ok...")

########
# MAIN #
########

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
    dp.add_handler(CommandHandler("pic_stats", pic_stats))
    dp.add_handler(CommandHandler("pic_time", pic_time))



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
