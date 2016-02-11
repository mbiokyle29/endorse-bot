"""
endorse_bot.py
author: @mbiokyle29
"""
import tweepy
import datetime
import json
import bisect
import logging

log = logging.getLogger(__name__)

class EndorseBot(object):

    def __init__(self, key, secret, query, days_back, leaderboard_size):

        self.key = key
        self.secret = secret
        self.query = query
        
        # time stuff
        self.since_id = -1
        self.days_back = days_back
        self.last_run = None

        # Create authentication token
        self.auth = tweepy.OAuthHandler(self.key, self.secret)
        self.api = tweepy.API(self.auth)

        # data storage
        self.leaderboard = []
        self.leaderboard_size = leaderboard_size

    def __repr__(self):
        return "<EndorseBot| query:{} | daysback: {}| size: {}>".format(
            self.query, self.days_back, self.leaderboard_size)

    def build_leaderboard(self):
        
        log.info("leaderboard build starting")
        log.info("last build: %s", str(self.last_run))

        if self.last_run != None:
            
            time_diff = (datetime.datetime.now() - self.last_run).total_seconds()
            log.info("Time since last build: %i", time_diff)

            # 15 min update
            if time_diff >= (60 * 15):
                log.info("Not building, happened less than 15 mins ago")
                self.last_run = datetime.datetime.now()
                return self.leaderboard
        try:
            if self.since_id != -1:
                for res in tweepy.Cursor(self.api.search, since_id=self.since_id, 
                                         q=self.query).items():

                    text = res.text

                    if "RT" in text:
                        continue

                    followers = res.author.followers_count
                    author = res.author.screen_name
                    created_at = res.created_at
                    tweet_id = res.id

                    tweet = {
                        'followers': followers,
                        'author': author,
                        'text': text,
                        'tweet_id': tweet_id
                    }

                    time_diff = datetime.datetime.now() - res.created_at

                    if time_diff.days == self.days_back:
                        self.since_id = tweet_id
                        self.add_tweet(tweet)
                        break

                    self.add_tweet(tweet)
            else:
                for res in tweepy.Cursor(self.api.search, since_id=self.since_id, 
                                         q=self.query).items():

                    text = res.text
                    followers = res.author.followers_count
                    author = res.author.screen_name
                    created_at = res.created_at
                    tweet_id = res.id

                    tweet = {
                        'followers': followers,
                        'author': author,
                        'text': text,
                        'tweet_id': tweet_id
                    }

                    time_diff = datetime.datetime.now() - res.created_at

                    if time_diff.days == self.days_back:
                        self.since_id = tweet_id
                        self.add_tweet(tweet)
                        break

                    self.add_tweet(tweet)

        except tweepy.TweepError:
            log.info("Twitter useage cutoff -- sending what we have")
            self.last_run = datetime.datetime.now()
            return self.leaderboard

        self.last_run = datetime.datetime.now()
        return self.leaderboard

    def add_tweet(self, tweet):

        # check if we are at capacity
        if len(self.leaderboard) == self.leaderboard_size:
            last = self.leaderboard[0]

            if last['followers'] < tweet['followers']:
                self.leaderboard.pop(0)

            # if its less than the bottom do nothing
            else:
                return

        # add it
        index_to_add = bisect.bisect(self.leaderboard, tweet['followers'])
        self.leaderboard.insert(index_to_add, tweet)

