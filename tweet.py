import os
import json
import requests
from requests_oauthlib import OAuth1Session


twitter = OAuth1Session(consumer_key=os.environ["CONSUMER_KEY"],
                  consumer_secret=os.environ["CONSUMER_SECRET"],
                  access_token_key=os.environ["ACCESS_TOKEN_KEY"],
                  access_token_secret=os.environ["ACCESS_TOKEN_SECRET"])
url = "https://api.twitter.com/1.1/statuses/update.json"
params = {'status':'test'}
res = twitter.post(url,params = params)
timeline = json.loads(res.text)

if res.status_code == 200:
    print ('successed')
else:
    print('error:%d' % res.status_code)