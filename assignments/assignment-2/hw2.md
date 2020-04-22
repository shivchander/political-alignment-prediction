# User Manual

# User Manual

Table of contents
=================

<!--ts-->
   * [Getting Started](#getting-started)
        * [Requirements](#requirements)
            * [Twitter API Dev](#twitter-api-developer-account)
            * [System Requirements](#system-requirements)
        * [Installation]()
            * [Cloning the repo](#cloning-the-repo)
            * [Dataset](#dataset)
            * [Libraries](#libraries)
   * [Model](#model)
        * [Using Pre-Trained Model](#using-pre-trained-model)
        * [Train Your Own Model](#training-your-own-model)
   * [Making Predictions](#making-predictions)
   * [FAQ]()
   * [Further Questions]()     
<!--te-->

Getting Started
===============

## Requirements

### Twitter API Developer Account

> In order to use Twitter’s API, we have to create a developer account on the Twitter apps site.

1. Log in or make a Twitter account at [Twitter.com](https://twitter.com/)

2. Apply for a twitter developer account [here](https://developer.twitter.com/en/application/use-case)

    ![](assets/ss1.png)

3. Make sure you select a student account

    ![](assets/ss2.png)
    
4. Add account details. Click on continue.

5. Describe in your own words what you are building. Click on continue.

6. Submit application.

7. Check your email associated with your twitter and click Confirm your email.

8. On the welcome screen, click on Create an app.

9. Fill out your App details and click on Create (its at the bottom of the page). Make sure you don’t try to make a appName that is already taken.

10. First, click on Keys and tokens. Second, click on create to get access token and access token secret.

    ![](assets/ss3.png)
    
    > Save your API key, API secret key, Access token, and Access token secret somewhere safe.

11. Replace the keys in the [keys.py](src/keys.py)
    
    ```python
    keys = dict(consumer_key="<consumer key>",
            consumer_secret="<consumer secret>",
            access_token='<access token>',
            access_token_secret='<access token secret>'
            )
    ```
    

### System Requirements

* A decent Multi-Core CPU (4+ cores)
* macOS or any Linux Distros
* [Python 3.7](https://www.python.org/downloads/release/python-370/)

## Installation

### Cloning the Repo

```bash
$ git clone https://github.com/shivchander/political-alignment-prediction.git
```

### Dataset

Download the dataset from kaggle.com using your kaggle account

[Link to download the dataset](https://www.kaggle.com/kapastor/democratvsrepublicantweets)

Save the CSV files under a new directory dataset/

### Libraries

> All the required libraries are in [requirements.txt](requirements.txt), simply run this file to install all the requirements

```bash
$ pip3 install -r requirements.txt
```

Model
=====

> There is a pre-trained model, one could just use that to make the predictions. Or you could train your own model using you own dataset

## Using Pre-Trained Model

The model config and weights are saved under [model/](model/)

To use these models, make sure the path to the file is correct under [src/main.py](src/main.py)

```python
json_file = open('model/model.json', 'r')
loaded_model.load_weights("model/model.h5")
```

## Training your own Model

Use the ipynb notebook and the intructions from it to train your own model

> Download the .h5 file and .json file and save them under model/

Making Predictions
==================

To make final predictions, run the following commands. The code takes twitter handle as an input and outputs the results in form of:

```bash
[tweet_score, tweet_prediction, retweet_score, rt_prediction, favtweet_score, ft_prediction, weighted_score, final_prediction]
```

To run the program, use this:

```bash
$ python3 main.py <twitter handle>
```

Sample Result:

```bash
$ python3 main.py RepMarkTakai
...
User                    RepMarkTakai 
tweet_score             0.874494	
tweet_prediction        democrat	
retweet_score           0.939216	
retweet prediction      democrat	
liked_tweet_score       0.841564	
liked_tweet_prediction  democrat	
weighted_score          0.892207	
final_prediction        democrat	
```


Further Questions
=================

If you need assistance using Deep Pollster or have any further questions:

Contact us:

> [Shivchander Sudalairaj](mailto:sudalasr@mail.uc.edu)
>
> [Sagar Panwar](mailto:panwarsr@mail.uc.edu)

If there is a bug in our code, raise an issue on our [Github Repo](https://github.com/shivchander/political-alignment-prediction)



  

