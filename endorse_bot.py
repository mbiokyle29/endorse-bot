#!/usr/bin/env python
"""
endore_bot.py
author: @mbiokyle29
"""

import argparse
import logging as log
import tweepy
import os

log.basicConfig(logLevel=log.INFO)

def main():

    log.info("Twitter Endrse Bot Starting")
    parser = argparse.ArgumentParser(
        description = (" Twitter Endorse Bot"),
    )

    # Authentication details. To  obtain these visit dev.twitter.com
    consumer_key = os.environ['TWITTER_API_CONSUMER']
    consumer_secret = os.environ['TWITTER_API_SECRET']

    if consumer_key is None:
        log.warn("twitter API consumer key not set!, ($TWITTER_API_CONSUMER)")
        return

    if consumer_secret is None:
        log.warn("twitter API consumer secret not set!, ($TWITTER_API_SECRET)")
        return

    # Create authentication token
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    # get followers

if __name__ == "__main__":
    main()