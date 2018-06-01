#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Bot helper. Send functions, logging, etc.

import logging


###########
# LOGGING #
###########
LOG_SENT_MSGS = 0
LOG_SENT_DOCS = 0
LOG_INTERVAL = 3600
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def log_usage(bot, job):
    """Log Bot usage"""
    logger.info('USAGE: Sent messages: %d | Sent Docs: %d | Total sent: %d' % (
        LOG_SENT_MSGS, LOG_SENT_DOCS, LOG_SENT_MSGS+LOG_SENT_DOCS))

##################
# SEND FUNCTIONS #
##################


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
        bot.sendDocument(chat_id=chat_id, document=doc)
    else:
        # Use the update
        bot.sendDocument(chat_id=update.message.chat_id, document=doc)
