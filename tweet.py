import os
import json
import requests
import datetime
from requests_oauthlib import OAuth1Session


twitter = OAuth1Session(os.environ["CONSUMER_KEY"],os.environ["CONSUMER_SECRET"],os.environ["ACCESS_KEY"],os.environ["ACCESS_SECRET"])
url = "https://api.twitter.com/1.1/statuses/update.json"
dt = datetime.datetime.now()
params = {'status':"現在は{0:%Y%m%d}".format(dt)}
res = twitter.post(url,params = params)
timeline = json.loads(res.text)

if res.status_code == 200:
    print ('successed')
else:
    print('error:%d' % res.status_code)