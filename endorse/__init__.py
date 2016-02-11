import argparse
import logging
import os

import tweepy
from flask import Flask, current_app, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from multiprocessing import Process
from multiprocessing.util import register_after_fork

# configure log
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s {%(levelname)s}: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(log_formatter)
log.addHandler(stream_handler)

log.info("Twitter Endrse Bot Starting")

consumer_key = os.environ['TWITTER_API_CONSUMER']
consumer_secret = os.environ['TWITTER_API_SECRET']

if consumer_key is None:
    log.warn("twitter API consumer key not set!, ($TWITTER_API_CONSUMER)")
    raise SystemExit

if consumer_secret is None:
    log.warn("twitter API consumer secret not set!, ($TWITTER_API_SECRET)")
    raise SystemExit

app = Flask(__name__)
app.config.from_object('endorse.config')
db = SQLAlchemy(app)
session = db.session

from endorse.models import Tweet

db.drop_all()
db.create_all()

from endorse.endorse_bot import EndorseBot
bot = EndorseBot(consumer_key, consumer_secret, 
                 "endorse @BernieSanders", 20, 1000, session)

def worker(bot):
    bot.work()

register_after_fork(db, db.get_engine(app).dispose)
p = Process(target=worker, args=(bot,))
p.start()
p.join()

@app.route("/")
def root():
    tweets = session.query(Tweet).order_by(desc(Tweet.followers)).all()
    return jsonify(leaderboard = [x.to_json() for x in tweets])

@app.route("/tweet", methods=['POST'])
def add_tweet():

    json = request.get_json()
    print json
    t_id = json.get('tweet_id')
    text = json.get('text')
    followers = json.get('followers')
    author = json.get('author')

    t = Tweet(t_id, text, followers, author)
    session.add(t)
    session.commit()
    return "OK  "