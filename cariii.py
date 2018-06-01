#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Cariii, anims, kawaii and pistoleros functionality.

import os
from random import randint, getrandbits
import urllib
import json
from telegram import Bot

from bothelper import send_msg, send_doc, logger

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

# COMMANDS
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