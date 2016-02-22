"""
endorse_bot.py
author: @mbiokyle29
"""
import tweepy
import datetime
import json
import bisect
import logging
from endorse import Tweet

log = logging.getLogger(__name__)

class EndorseBot(object):

    def __init__(self, key, secret, query, days_back, leaderboard_size, session):

        self.key = key
        self.secret = secret
        self.query = query
        
        # time stuff
        self.days_back = days_back
        self.last_run = None

        # Create authentication token
        self.auth = tweepy.OAuthHandler(self.key, self.secret)
        self.api = tweepy.API(self.auth)

        # data storage
        self.session = session
        self.leaderboard_size = leaderboard_size

    def work(self):
        
        log.info("leaderboard build starting")
        log.info("last build: %s", str(self.last_run))

        if self.last_run != None:
            
            time_diff = (datetime.datetime.now() - self.last_run).total_seconds()
            log.info("Time since last build: %i", time_diff)

            # 15 min update
            if time_diff >= (60 * 15):
                log.info("Not building, happened less than 15 mins ago")
                self.last_run = datetime.datetime.now()
                return

        try:
            for res in tweepy.Cursor(self.api.search, q=self.query).items():

                text = res.text

                # skip if a retweet
                if "RT" in text:
                    continue

                followers = res.author.followers_count
                author = res.author.screen_name
                created_at = res.created_at
                tweet_id = res.id

                if res.geo is not None:
                    geo = str(res.geo)
                else:
                    geo = "< No Geo Info >"

                # skip if its in the DB already
                if self.session.query(Tweet).get(tweet_id) is not None:
                    return

                tweet = Tweet(tweet_id, text, followers, author, geo)

                time_diff = datetime.datetime.now() - res.created_at
                if time_diff.days == self.days_back:
                    self.since_id = tweet_id
                    self.add_tweet(tweet)
                    return

                self.add_tweet(tweet)

        except tweepy.TweepError:
            log.info("Twitter useage cutoff -- sending what we have")
            self.last_run = datetime.datetime.now()
            return

        self.last_run = datetime.datetime.now()
        return

    def add_tweet(self, tweet):

        # see if we need to remove
        count = self.session.query(Tweet).count()

        if count == self.leaderboard_size:
            lowest = self.session.query(Tweet).order_by(Tweet.followers).limit(1)
            
            if lowest.followers <= tweet.followers:
                self.session.delete(lowest)
            else:
                return

        self.session.add(tweet)
        self.session.commit()
