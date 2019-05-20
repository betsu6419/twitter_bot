import json
import requests
from requests_oauthlib import OAuth1Session


twitter = OAuth1Session(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
url = "https://api.twitter.com/1.1/statuses/update.json"
params = {'status':'test'}
res = twitter.post(url,params = params)
timeline = json.loads(res.text)

if res.status_code == 200:
    print ('successed')
else:
    print('error:%d' % res.status_code)