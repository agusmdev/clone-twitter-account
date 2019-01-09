# -*- coding: utf-8 -*-

import tweepy
import time
import re
import requests
from access import *
from random import randint
import argparse
import threading


class Api(object):
    def __init__(self):
        super(Api, self).__init__()
        try:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            # Return API access:
            self.api = tweepy.API(auth, wait_on_rate_limit=True,
                                  wait_on_rate_limit_notify=True, compression=True)

            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            raise Exception('Error! Failed to get request token.')

    def get_user(self, user):
        return self.api.get_user(user)

    def retrieve_tweets(self, user, count=10, include_rts=False):
        try:
            return self.api.user_timeline(screen_name=user, count=20,
                                          include_rts=include_rts)
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
        self.post_tweet("@{} is going to be cloned".format(user_clone))

        for tweet in tweets:
            # Print tweet:
            print(tweet.text)
            self.post_tweet(tweet.text)

    def delete_tweets(self):
        print("Deleting all tweets from the account @".
              format(self.api.verify_credentials().screen_name))
        for status in tweepy.Cursor(self.api.user_timeline).items():
            try:
                self.api.destroy_status(status.id)
            except Exception as e:
                print(e)

    def print_tweets(self, tweets):
        for i in tweets:
            print(i.text+"\n")

    def follow_all_users(self, user):
        for page in tweepy.Cursor(self.api.followers_ids, screen_name=user).pages():
            [self.api.create_friendship(id=i) for i in page]

    def update_profile_photo(self, user):
        user = self.get_user(user)
        image_url = user.profile_image_url[:63]+user.profile_image_url[70:]
        img_data = requests.get(image_url).content

        with open('last_cloned_profile.jpg', 'wb') as handler:
            handler.write(img_data)

        self.api.update_profile_image("./last_cloned_profile.jpg")

        print("Successfully changed profile photo, you used @{} photo".
              format(user.screen_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--print", help="print tweets from the given profile",
                        action="store_true")
    parser.add_argument("-c", "--clone", help="clone some tweets from the given profile",
                        action="store_true")
    parser.add_argument("-d", "--delete", help="delete all tweets from the account",
                        action="store_true")
    parser.add_argument("-f", "--follow", help="follow all users from the given profile",
                        action="store_true")
    parser.add_argument("-up", help="update profile photo using the profile photo \
                                     from the given profile",
                        action="store_true")
    parser.add_argument("--user", help="provide user to clone from the command line",
                        action="store", type=str)
    args = parser.parse_args()

    bot = Api()
    secs = 1

    if args.user:
        user = args.user
    else:
        user = input("Give some public profile please\n")

    if args.print:
        bot.print_tweets(bot.retrieve_tweets(user))
    if args.clone:
        bot.clone_last_tweets(user)
    if args.follow:
        bot.follow_all_users(user)
    if args.delete:
        print("This will be developed soon..")
    if args.up:
        bot.update_profile_photo(user)
    if len(set(vars(args).values())) == 1:
        print("No flags given, nothing to do")
