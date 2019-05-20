import json
import requests
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = 's4FZwy1aieqrKgtoTboNspWhr'
CONSUMER_SECRET = 'eY0FbosbIqYb7DZVV1O69grpgfCk4h3vrigacNfLxGHXUv8zwi'
ACCESS_KEY = '215197125-3XyBAy5RJ4AzwbVPSCxMGmER4ngUUNKETYWF7Iuz'
ACCESS_SECRET = '4om8aE97NIFzhVU7cPf7Uloi0SQzYEPxE1CTFWMF5O5sN'

twitter = OAuth1Session(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
url = "https://api.twitter.com/1.1/statuses/update.json"
params = {'status':'test'}
res = twitter.post(url,params = params)
timeline = json.loads(res.text)

if res.status_code == 200:
    print ('successed')
else:
    print('error:%d' % res.status_code)