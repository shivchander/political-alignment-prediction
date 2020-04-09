import tweepy

from src.keys import keys
from src.bacon import Frontier, safe_lookup_users

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

        # politicians' screennames for bacon number
        self._dem_usrs = ['BernieSanders', 'AOC', 'JoeBiden']
        self._rep_usrs = ['realDonaldTrump', 'VP', 'GOP']

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
            return

    def get_bacon(self):
        """
        :return: two dicts (dem, rep) with predetermined politicians as the keys and the bacon num as the values
        """
        source = self.user_handle
        api = self.api

        dest_dem_usrs = self._dem_usrs
        dest_rep_usrs = self._rep_usrs

        try:
            # Get user ids from the user handles
            src_user = api.get_user(source)

            dem = {}
            rep = {}

            for party in (dest_dem_usrs, dest_rep_usrs):
                if party == dest_dem_usrs:
                    party_flag = 'dem'
                else:
                    party_flag = 'rep'
                for destination in party:

                    if source == destination:
                        separation = 0
                        continue

                    else:

                        dest_user = api.get_user(destination)

                        src_frontier = Frontier(src_user.id, api.friends_ids
                                                , lambda n: n.friends_count
                                                , lambda ids: safe_lookup_users(api, ids))
                        dest_frontier = Frontier(dest_user.id, api.followers_ids
                                                 , lambda n: n.followers_count
                                                 , lambda ids: safe_lookup_users(api, ids))

                        while src_frontier.covered_all() or dest_frontier.covered_all():
                            # Expand the source node's frontier first
                            nodes = src_frontier.expand_perimeter()

                            # check if any one of new nodes is on the destination's perimeter
                            if any(map(lambda n: dest_frontier.is_on_perimeter(n), nodes)):
                                # print("Found!")
                                break

                            # Copy twice with a slight pain. If you have to copy thrice, abstract!
                            nodes = dest_frontier.expand_perimeter()
                            if any(map(lambda n: src_frontier.is_on_perimeter(n), nodes)):
                                # print("Found!")
                                break

                        m = src_frontier.perimeter.intersection(dest_frontier.perimeter).pop()

                        # The man in the middle!
                        m = src_frontier.perimeter.intersection(dest_frontier.perimeter).pop()

                        separation = src_frontier.get_distance(m) + dest_frontier.get_distance(m) - 1

                    if party_flag == 'dem':
                        dem[dest_user.name] = separation
                    else:
                        rep[dest_user.name] = separation

            return dem, rep

        except tweepy.RateLimitError:
            print("""It seems we have exceeded twitter's api call limit.
                         Please come back after 15 minutes.""")
        except tweepy.TweepError as e:
            print("Something went wrong!")
            print(e)


x = Tweet('01110011shiv')
print(x.get_bacon())
