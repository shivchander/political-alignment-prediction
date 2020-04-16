from src.twitter import Tweet
from nltk.tokenize.casual import TweetTokenizer
from wordcloud import STOPWORDS
import numpy as np
import nltk as nlp
import sys
import os
import re
from keras.preprocessing import sequence
from keras.models import model_from_json
import nltk
nltk.download('punkt')
nltk.download('wordnet')

STOPWORDS.add("rt")
STOPWORDS.add("s")
STOPWORDS.add("u")
STOPWORDS.add("amp")
STOPWORDS.add("th")
STOPWORDS.add("will")
STOPWORDS.add("t")
STOPWORDS.add("m")

__author__ = 'Shivchander Sudalairaj'

json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("model/model.h5")
lemma = nlp.WordNetLemmatizer()
tokenizer = TweetTokenizer(reduce_len=True)
max_review_length = 50


def clean_input(tweet):
    tweet = re.sub(r'http\S+', '', tweet) #remove links
    tweet = re.sub("[^a-zA-Z]", " ", tweet) #remove all characters except letters
    tweet = tweet.lower() #convert all words to lowercase
    tweet = nltk.word_tokenize(tweet) #split sentences into word
    tweet = [word for word in tweet if not word in STOPWORDS] #remove the stopwords
    tweet = [lemma.lemmatize(word) for word in tweet] #identify the correct form of the word in the dictionary
    tweet = " ".join(tweet)
    return tweet


def convert_input(tweet):
    tweet = clean_input(tweet)
    # tokenizing
    tweet = tokenizer.tokenize(tweet)
    # converting tweet tokens to freq dist ranks
    terms = [term for term, count in fdist.most_common(top_words)]
    encoded_tweet = [terms.index(term) if term in terms else 0 for term in tweet]
    tweet_arr = np.array([encoded_tweet])
    padded_tweet = sequence.pad_sequences(tweet_arr, maxlen=max_review_length)
    return padded_tweet


def predict_tweet(tweet):
    tweet = convert_input(tweet)
    prediction = loaded_model.predict(tweet)
    # print(prediction)
    return prediction


def make_predictions(tweets):
    dem_sum_score = 0
    dem_count = 0
    rep_sum_score = 0
    rep_count = 0
    for t in tweets:
        res = predict_tweet(t)
        if res > 0.5:
          party = 'Democrat'
          dem_sum_score += float(res)
          dem_count += 1
        else:
          party = 'Republican'
          rep_sum_score += 1 - float(res)
          rep_count += 1
    y = [rep_sum_score/100, dem_sum_score/100]
    return max(y), np.argmax(np.asarray(y))


def get_final_predictions(screenname):
    x = Tweet(screenname)
    tweets = x.get_tweets()
    retweets = x.get_retweets()
    favtweets = x.get_favtweets()
    tweet_score, t_party = make_predictions(tweets)
    retweet_score, rt_party = make_predictions(retweets)
    favtweet_score, ft_party = make_predictions(favtweets)
    weighted_score = 0.5*tweet_score+0.35*retweet_score+0.15*favtweet_score
    party_score = sum([t_party, rt_party, ft_party])/3
    if party_score > 0.5:
        party = 'democrat'
    else:
        party = 'republican'
    return [tweet_score, t_party, retweet_score, rt_party, favtweet_score, ft_party, weighted_score, party]


if __name__ == '__main__':
    print(get_final_predictions(sys.argv[1]))
