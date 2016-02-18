import argparse
import logging
import os

import tweepy
import twython
from flask import Flask, current_app, json
# from task_factory import make_celery
from endorse_bot import EndorseBot

consumer_key = 'o5hyMS62DK9t5s7hHUwzkFDb1'
consumer_secret = 'd4eeRwTSsShrGTNr8q9LeRc7SXk08wXeUnrh3K3CTSraGBQYL6'
oauth_token = '4750356026-716zs4OoqCt1ap4tslSQQE1ZmT3YUQ53k1WinH4'
oauth_secret = 'nvqp8teoY9dOb2ngAjogfanfoXQfVwDDwgL1TtMpK1ast'

bot = EndorseBot(consumer_key, consumer_secret, oauth_token, oauth_secret, "endorses @BernieSanders", 1, 10)

# print bot.build_leaderboard()

print bot.watch_stream('bernie, sanders, endorse')