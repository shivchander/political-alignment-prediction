from src.twitter import Tweet
from keras.models import model_from_json


__author__ = 'Shivchander Sudalairaj'


def get_model():
    """
    :return: trained model
    """
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model.h5")
    return loaded_model


class Predictor:
    def __init__(self, user_handle):
        self.user_handle = user_handle
        self.tweeter = Tweet(user_handle)
        self.model = get_model()

    def get_tweet_score(self):
        tweets = self.tweeter.get_tweets()


if __name__ == '__main__':
    ...

