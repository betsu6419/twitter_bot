import os
import datetime
import tweepy

client = tweepy.Client(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_KEY"],
    access_token_secret=os.environ["ACCESS_SECRET"],
)

dt = datetime.datetime.now()
response = client.create_tweet(text="現在は{}".format(dt))

if response.data:
    print("successed: tweet_id={}".format(response.data["id"]))
else:
    print("error: {}".format(response.errors))
