"""
endorse_bot.py
author: @mbiokyle29
"""
import tweepy
import datetime
from leaderboard.leaderboard import Leaderboard
import json
import ast

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
        self.leaderboard = Leaderboard("endorsements")
        
        # config
        self.leaderboard.MEMBER_KEY = "tweet"
        self.leaderboard.MEMBER_DATA_KEY = 'tweet_data'
        self.leaderboard.SCORE_KEY = 'followers'
        self.leaderboard.DEFAULT_GLOBAL_MEMBER_DATA = True
        self.leaderboard_size = leaderboard_size
        self.leaderboard_index = 1

    def build_leaderboard(self):

        if self.last_run != None:
            time_diff = (datetime.datetime.now() - self.last_run).total_seconds()

            # 15 min update
            if time_diff >= (60 * 15):
                self.last_run = datetime.datetime.now()
                return self.get_leaderboard()
        try:
            if self.since_id != -1:
                for res in tweepy.Cursor(self.api.search, since_id=self.since_id, 
                                         q=self.query).items():

                    text = res.text
                    followers = res.author.followers_count
                    author = res.author.screen_name
                    created_at = res.created_at
                    tweet_id = res.id

                    data = {
                        'author': author,
                        'text': text,
                        'tweet_id': tweet_id
                    }

                    time_diff = datetime.datetime.now() - res.created_at

                    if time_diff.days == self.days_back:
                        self.since_id = tweet_id
                        self.add_tweet(followers, data)
                        break

                    self.add_tweet(followers, data)
            else:
                for res in tweepy.Cursor(self.api.search, since_id=self.since_id, 
                                         q=self.query).items():

                    text = res.text
                    followers = res.author.followers_count
                    author = res.author.screen_name
                    created_at = res.created_at
                    tweet_id = res.id

                    data = {
                        'author': author,
                        'text': text,
                        'tweet_id': tweet_id
                    }

                    time_diff = datetime.datetime.now() - res.created_at

                    if time_diff.days == self.days_back:
                        self.since_id = tweet_id
                        self.add_tweet(followers, data)
                        break

                    self.add_tweet(followers, data)

        except tweepy.TweepError:
            self.last_run = datetime.datetime.now()
            return self.get_leaderboard()

        self.last_run = datetime.datetime.now()
        return self.get_leaderboard()

    def add_tweet(self, followers, data):

        # check if we are at capacity
        if (self.leaderboard_index+1) == self.leaderboard_size:
            last = self.leaderboard.member_at(self.leaderboard_size)

            if last['followers'] < followers:
                self.leaderboard.remove_member('tweet_{}'.format(str(self.leaderboard_index)))
                self.leaderboard_index -= 1

            # if its less than the bottom do nothing
            else:
                return

        # add it
        self.leaderboard.rank_member('tweet_%s' % self.leaderboard_index, followers, data)
        self.leaderboard_index += 1

    def get_leaderboard(self):

        result = []
        count = self.leaderboard.total_members()

        for i in range(1,count):
            
            tweet = self.leaderboard.member_at(i)
            data = ast.literal_eval(self.leaderboard.member_data_for(tweet['tweet']))

            data['rank'] = tweet['rank']
            data['followers'] = tweet['followers']

            result.append(data)

        return result
