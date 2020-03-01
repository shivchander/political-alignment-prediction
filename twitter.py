import tweepy
import time
import sys

from keys import keys

__author__ = 'Shivchander Sudalairaj'


class Tweet:
    def __init__(self, user_handle):
        """
        :param user_handle: twitter username without '@' symbol
        :return: class method
        """
        self._consumer_key = keys['consumer_key']
        self._consumer_secret = keys['consumer_secret']
        self._access_token = keys['access_token']
        self._access_token_secret = keys['access_token_secret']

        # configure OAUTH
        self.auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        self.auth.set_access_token(self._access_token, self._access_token_secret)

        # set up tweepy client
        self.api = tweepy.API(
            self.auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True,
            timeout=60,
            compression=True
        )

        self.user_handle = user_handle

    def get_friends(self):
        """
        :return: array containing the IDs of users being followed by self.
        """

        try:
            # get friends ids
            friends_ids = []
            for friend in tweepy.Cursor(self.api.friends_ids, screen_name=self.user_handle).pages():
                friends_ids.append(friend)

            # get twitter handles
            friends_handles = [user.screen_name for user in self.api.lookup_users(user_ids=friends_ids)]
            return friends_handles

        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return []

    def get_followers(self):
        """
        :return: array containing the IDs of users following self.
        """
        try:
            # get friends ids
            followers_ids = []
            for follower in tweepy.Cursor(self.api.followers_ids, id=self.user_handle).pages():
                followers_ids.append(follower)

            # get twitter handles
            followers_handles = [user.screen_name for user in self.api.lookup_users(user_ids=followers_ids)]
            return followers_handles

        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return []

    def get_tweets(self, limit=100):
        """
        :param limit: max limit of tweets
        :return: array containing the tweets from self.user_handle
        """
        try:
            tweets = []
            for obj in tweepy.Cursor(self.api.user_timeline, screen_name=self.user_handle,
                                     include_rts=False, tweet_mode='extended').items(limit):
                if len(tweets) < limit:
                    tweets.append(obj.full_text)
                else:
                    break
            return tweets

        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return []

    def get_retweets(self, limit=100):
        """
        :param limit: max limit of tweets
        :return: array containing the retweets from self.user_handle
        """

        try:
            retweets = []
            for obj in tweepy.Cursor(self.api.user_timeline, screen_name=self.user_handle,
                                     include_rts=True, tweet_mode='extended').items():
                if obj.full_text.startswith('RT'):
                    if len(retweets) < limit:
                        retweets.append(obj.full_text)
                    else:
                        break
            return retweets

        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return []

    def get_favtweets(self, limit=100):
        """
        :param limit: max limit of tweets
        :return: array containing the tweets favorite-ed by self.user_handle
        """

        try:
            favtweets = []
            for obj in tweepy.Cursor(self.api.favorites, id=self.user_handle).items(limit):
                if len(favtweets) < limit:
                    favtweets.append(obj.text)
                else:
                    break
            return favtweets

        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return []

    def get_location(self):
        """
        :return: location of the self
        """
        try:
            print(self.api.get_user(screen_name=self.user_handle).location)
        except tweepy.TweepError:
            print('Oops somethings not right, good luck figuring out what')
            return None
