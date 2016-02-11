import argparse
import logging
import os

import tweepy
from flask import Flask, current_app, json
from endorse_bot import EndorseBot

consumer_key = os.environ['TWITTER_API_CONSUMER']
consumer_secret = os.environ['TWITTER_API_SECRET']
    
bot = EndorseBot(consumer_key, consumer_secret, "endorses @BernieSanders", 1, 10)
print bot.build_leaderboard()