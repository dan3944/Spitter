from textblob import TextBlob as tb
from tweepy.streaming import StreamListener
from twilio.rest import Client
from urllib.request import urlopen
from boto.s3.key import Key
import boto.s3
import tweepy
import json
import time

phoneFrom = '+16178588543'

xmlTemplate = '''
<Response>
    <Say voice="%s">Tweet from %s: %s</Say>
</Response>
'''

class TweetListener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        handleToNumbers = getUsersJson()

        if 'user' not in data:
            return

        data['user']['screen_name'] = data['user']['screen_name'].upper()

        if data['user']['screen_name'] in handleToNumbers.keys():
            phonesToCall = handleToNumbers[data['user']['screen_name']]

            # detect emotion
            blob = tb(data['text'])
            polarity = blob.sentiment.polarity  # the negativity or positivity of the tweet, on a -1 to 1 scale
            voice = 'alice' if polarity > 0 else 'man'

            for phoneNum in phonesToCall:
                call(phoneNum, data, voice)

def call(phoneTo, tweet, voice):
    xml = xmlTemplate % (voice, tweet['user']['name'], tweet['text'])
    print(xml)
    k = Key(bucket)
    k.key = 'tweet_%s.xml' % tweet['id']
    k.content_type = 'text/xml'
    k.set_contents_from_string(xml)
    k.set_acl('public-read')
    client.calls.create(to=phoneTo, from_=phoneFrom, method='GET',
            url='https://s3.amazonaws.com/twinty/tweet_%s.xml' % tweet['id'])

def getUsersJson():
    return json.loads(urlopen('https://s3.amazonaws.com/twinty/users.json').read().decode())


if __name__ == '__main__':
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    # twitter info
    auth = tweepy.OAuthHandler(authInfo['twitter_api_key'], authInfo['twitter_api_secret'])
    auth.set_access_token(authInfo['twiter_access_token'], authInfo['twitter_access_secret'])
    api = tweepy.API(auth)

    # twilio info
    client = Client(authInfo['twilio_acct_sid'], authInfo['twilio_auth_token'])
    userIDs = set(str(api.get_user(handle).id) for handle in getUsersJson().keys())

    # aws info
    conn = boto.connect_s3(authInfo['aws_access_key'], authInfo['aws_secret_key'])
    bucket = conn.get_bucket('twinty')

    stream = tweepy.Stream(auth, TweetListener())
    stream.filter(follow = userIDs, async = True)

    while True:
        time.sleep(5)
        newUserIDs = set(str(api.get_user(handle).id) for handle in getUsersJson().keys())

        if newUserIDs != userIDs:
            stream.disconnect()
            stream.filter(follow = newUserIDs, async = True)
