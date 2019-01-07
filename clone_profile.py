# -*- coding: utf-8 -*-

import tweepy
import time
import re
from access import *
from random import randint
import argparse
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
            return self.api.user_timeline(screen_name=user, count=20)
        except Exception as e:
            raise e

    def post_tweet(self, tweet_text):
        try:
            self.api.update_status(tweet_text)
            print("Successfully posted.")
        except tweepy.TweepError as e:
            print(e.reason)

    def clone_last_tweets(self, user_clone):
        tweets = self.retrieve_tweets(user_clone)[::-1]
        self.post_tweet("cloning.. @{}".format(user_clone))

        for tweet in tweets:
            # Print tweet:
            print(tweet.text)
            if tweet.text[0] != "R" and tweet.text[1] != "T":
                self.post_tweet(tweet.text)
        return True

    def delete_tweets(self):
        print("Deleting all tweets from the account @%s."
              % self.api.verify_credentials().screen_name)
        for status in tweepy.Cursor(self.api.user_timeline).items():
            try:
                self.api.destroy_status(status.id)
            except Exception as e:
                print(e)

    def print_tweets(self, tweets):
        for i in tweets:
            print(i.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--print", help="print tweets from the give profile",
                        action="store_true")
    parser.add_argument("-c", "--clone", help="clone some tweets from the give profile",
                        action="store_true")
    args = parser.parse_args()

    bot = Api()
    secs = 1
    user = input("Ingrese un usuario: ")

    if args.print:
        bot.print_tweets(bot.retrieve_tweets(user))
    elif args.clone:
        bot.clone_last_tweets(user)
    else:
        print("LA CONCHA DE TU MADRE")
