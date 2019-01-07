# -*- coding: utf-8 -*-

import tweepy
import time
import re
from access import *
from random import randint
import threading


class Api(object):
    def __init__(self):
        super(Api, self).__init__()
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # Return API access:
        self.api = tweepy.API(auth)

    def get_user(self, user):
        return self.api.get_user(user)

    def retrieve_tweets(self, user, count=10):
        try:
            # print(len(list(tweepy.Cursor(self.api.user_timeline, id=user.id).items())))
            return self.api.user_timeline(screen_name=user, count=20)
        except Exception as e:
            raise e

    def clone_last_tweets(self, user_clone):
        tweets = self.retrieve_tweets(user_clone)[::-1]
        for tweet in tweets:
            # Print tweet:
            print(tweet.text)
            if tweet.text[0] != "R" and tweet.text[1] != "T":
                try:
                    self.api.update_status(tweet.text)
                    print("Successfully posted.")
                except tweepy.TweepError as e:
                    print(e.reason)
        return True

    def delete_tweets(self):
        print("Deleting all tweets from the account @%s."
              % self.api.verify_credentials().screen_name)
        for status in tweepy.Cursor(self.api.user_timeline).items():
            try:
                self.api.destroy_status(status.id)
            except Exception as e:
                print(e)


bot = Api()

secs = 1
user = bot.get_user(input("Ingrese un usuario: "))
tweets = bot.retrieve_tweets(user)
for i in tweets:
    print(i.text)
# threading.Thread(target=bot.clone_last_tweets(user.screen_name))
