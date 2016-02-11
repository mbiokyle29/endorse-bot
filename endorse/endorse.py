#!/usr/bin/env python
"""
endore_bot.py
author: @mbiokyle29
"""

import argparse
import logging
import os

import tweepy
from flask import Flask, current_app, json
from endorse_bot import EndorseBot

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s {%(levelname)s}: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(log_formatter)
log.addHandler(stream_handler)

def main():

    log.info("Twitter Endrse Bot Starting")

    consumer_key = os.environ['TWITTER_API_CONSUMER']
    consumer_secret = os.environ['TWITTER_API_SECRET']

    if consumer_key is None:
        log.warn("twitter API consumer key not set!, ($TWITTER_API_CONSUMER)")
        return

    if consumer_secret is None:
        log.warn("twitter API consumer secret not set!, ($TWITTER_API_SECRET)")
        return

    bot = EndorseBot(consumer_key, consumer_secret, "endorses @BernieSanders", 1, 10)
    log.info("BOT: %s", str(bot))
    
    app = Flask(__name__)

    @app.route('/')
    def get_leaderboard():
        return json.dumps(bot.build_leaderboard())    

    app.run(debug=True)

if __name__ == "__main__":
    main()