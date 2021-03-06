"""
A Twitter bot written in Python using Tweepy. 
It will like and retweet tweets that contain single or multiple keywords and hashtags.
"""

# Built-in/Generic Imports
import os
import logging
from time import sleep

# Library Imports
import tweepy

# Own modules
from config import *

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

def initialize_api():
    api = create_api()
    return api

def get_tweets(api):
    # Exclude retweets from search to avoid repeats
    if run_continuously:
        tweets = tweepy.Cursor(api.search,
                        q=search_keywords + " -filter:retweets", 
                        count=100,
                        result_type=result_type,
                        monitor_rate_limit=True, 
                        wait_on_rate_limit=True,
                        lang="en").items()
    else:
        tweets = tweepy.Cursor(api.search,
                        q=search_keywords + " -filter:retweets",
                        count=100,
                        result_type=result_type,
                        monitor_rate_limit=True, 
                        wait_on_rate_limit=True,
                        lang="en").items(number_of_tweets)
    return tweets

def process_tweets(api, tweets):
    for tweet in tweets:
        tweet = api.get_status(tweet.id)
        logger.info(f"Processing tweet: {tweet.text}")

        # Ignore tweet if it is from myself or if it is a reply to a tweet
        if tweet.user.id != api.me().id or tweet.in_reply_to_status_id is not None:

            if retweet_tweets:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        logger.info("Retweeted now")
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        raise e
                else:
                    logger.info("Has been retweeted previously")

            if like_tweets:    
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                        logger.info("Favorited now")
                    except Exception as e:
                        logger.error("Error on favorite", exc_info=True)
                        raise e
                else:
                    logger.info("Has been favorited previously")

        # Delay in between processing tweets
        sleep(delay)


if __name__ == "__main__":
    api = initialize_api()
    tweets = get_tweets(api)
    process_tweets(api, tweets)
