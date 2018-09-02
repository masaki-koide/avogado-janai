import json
import tweepy
import os
import logging

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def favorite_avogado_tweet(event, context):    
    recent_favorited_tweet = api.favorites(api.me().screen_name)[0].id

    for tweet in tweepy.Cursor(api.search, q='アボガド exclude:retweets', lang='ja').items(100):
        if tweet.id == recent_favorited_tweet:
            break

        exclude_words = ['アボカド', 'アボガド6', 'アボガド６']
        if not any([word in tweet.text for word in exclude_words]):
            try:
                api.create_favorite(tweet.id)
            except Exception as e:
                logger.error(e)
                return {
                    "message": e,
                    "event": event
                }

    return {
        "message": "Success!",
        "event": event
    }
