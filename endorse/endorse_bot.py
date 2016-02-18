"""
endorse_bot.py
author: @mbiokyle29

Changes Feb 11, 2016 by Nosreme
"""

import tweepy
from twython import TwythonStreamer
import datetime
from leaderboard.leaderboard import Leaderboard
import json

# BernieStreamer class required for access to streaming API
class BernieStreamer(TwythonStreamer):
	
	# on_success() executes when a tweet matches the query in watch_stream()
    def on_success(self, data):

    	# If user mentions '@BernieSanders'
    	for item in data['entities']['user_mentions']:
    		if item['screen_name'] == 'BernieSanders':
    			# Stores user data here for use in leaderboard, etc.
    			tweet = data['text']
    			user = data['user']['screen_name']
    			id = data['user']['id']
    			followers = data['user']['followers_count']
    			# For test with runner.py
    			print user
    			print tweet
    			
    		else:
    			pass
				
	# Returns error code if there is a problem with API connection	
    def on_error(self, status_code, data):
		print "Error"
		print status_code


class EndorseBot(object):

    def __init__(self, key, secret, oauth_token, oauth_secret, 
    			 query, days_back, leaderboard_size):
		
        self.key = key
        self.secret = secret
        self.query = query
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        
        # time stuff
        self.since_id = -1
        self.days_back = days_back

        # Create Tweepy authentication token
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

        return self.get_leaderboard()
        
# Creates an instance of the BernieStreamer class.   
    def watch_stream(self, query):
		stream = BernieStreamer(self.key, self.secret, 
								self.oauth_token, self.oauth_secret)
															
		tweets = stream.statuses.filter(track=query)
		

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
            text_data = self.leaderboard.member_data_for(tweet['tweet'])

            data = {}
            data['rank'] = tweet['rank']
            data['followers'] = tweet['followers']
            data['text'] = text_data

            result.append(data)

        return result
			