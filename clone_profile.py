# -*- coding: utf-8 -*-

import tweepy
import requests
from access import *
import argparse


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
            raise Exception('Error! Failed to get request token, please complete \
                            access file')

    def get_user(self, user):
        return self.api.get_user(user)

    def retrieve_tweets(self, user, count=20, include_rts=False):
        try:
            return self.api.user_timeline(screen_name=user, count=count,
                                          include_rts=include_rts)
        except Exception as e:
            raise e

    def post_tweet(self, tweet_text):
        try:
            self.api.update_status(tweet_text)
            print("Successfully posted.")
        except tweepy.TweepError as e:
            print(e.reason)

    def clone_last_tweets(self, user_clone, quantity):
        tweets = self.retrieve_tweets(user_clone, quantity)[::-1]
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

    def follow_users(self, user, quantity):
        print("Following {} users from {}".format(quantity, user))
        for page in tweepy.Cursor(self.api.followers_ids, screen_name=user).pages():
            size = min(len(page), quantity)

            [self.api.create_friendship(id=page[i]) for i in range(size)]

            if len(page) > quantity:
                print("Followed {} users".format(quantity))
                return
            else:
                print("Followed {} users".format(len(page)))
                quantity -= len(page)

    def save_profile_photo(self, user):
        try:
            image_url = user.profile_image_url[:63]+user.profile_image_url[70:]
            img_data = requests.get(image_url).content

            with open('profile_photo.jpg', 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            raise e

    def save_profile_banner(self, user):
        try:
            image_url = user.profile_banner_url
            img_data = requests.get(image_url).content

            with open('banner_photo.jpg', 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            raise e

    def update_profile(self, user):
        print("Updating your profile....")
        user = self.get_user(user)
        user_data = {
                     "name": user.name,
                     "location": user.location,
                     "url": user.url,
                     "description": user.description,
                     "profile_link_color": user.profile_link_color,
                     }
        self.save_profile_photo(user)
        self.save_profile_banner(user)

        self.api.update_profile_image("./profile_photo.jpg")
        self.api.update_profile_banner("./banner_photo.jpg")
        self.api.update_profile(**user_data)

        print("Successfully update your profile, using @{} profile".
              format(user.screen_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--print", help="print N tweets from the given profile",
                        type=int)
    parser.add_argument("-c", "--clone", help="clone N tweets from the given profile",
                        type=int)
    parser.add_argument("-d", "--delete", help="delete all tweets from the authenticated account",
                        action="store_true")
    parser.add_argument("-f", "--follow", help="follow N users from the given profile [slow]",
                        type=int)
    parser.add_argument("-up", help="update profile data using the profile cloning \
                         the given profile",
                        action="store_true")
    parser.add_argument("--user", help="provide user to clone from the command line",
                        action="store", type=str)
    parser.add_argument("--export", help="sav",
                        action="store", type=str)
    args = parser.parse_args()

    bot = Api()

    if args.user:
        user = args.user
    else:
        user = input("Give some public profile please\n")

    if args.print:
        bot.print_tweets(bot.retrieve_tweets(user, args.print))
    if args.clone:
        bot.clone_last_tweets(user, args.clone)
    if args.follow:
        bot.follow_users(user, args.follow)
    if args.delete:
        bot.delete_tweets()
    if args.up:
        bot.update_profile(user)
