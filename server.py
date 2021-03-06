from textblob import TextBlob as tb
from tweepy.streaming import StreamListener
from twilio.rest import Client
from urllib.request import urlopen
from datetime import datetime
from boto.s3.key import Key
import boto.s3
import tweepy
import json
import time
import multiprocessing

phoneFrom = '+16178588543'

xmlTemplate = '''
<Response>
    <Say voice="%s">Tweet from %s: %s</Say>
</Response>
'''

class TweetListener(StreamListener):
    bucket = None
    client = None
    usersJson = None
    lastUpdatedUsers = 0

    def __init__(self, bucket, client):
        self.bucket = bucket
        self.client = client

    def on_data(self, data):
        data = json.loads(data)

        if 'user' not in data:
            return

        if time.time() - self.lastUpdatedUsers > 5:
            self.usersJson = getUsersJson()

        data['user']['screen_name'] = data['user']['screen_name'].upper()

        if data['user']['screen_name'] in self.usersJson.keys():
            phonesToCall = self.usersJson[data['user']['screen_name']]

            # detect emotion
            blob = tb(data['text'])
            polarity = blob.sentiment.polarity  # the negativity or positivity of the tweet, on a -1 to 1 scale
            voice = 'alice' if polarity > 0 else 'man'

            for phoneNum in phonesToCall:
                self.call(phoneNum, data, voice)

    def call(self, phoneTo, tweet, voice):
        xml = xmlTemplate % (voice, tweet['user']['name'], tweet['text'])
        print(xml)
        k = Key(self.bucket)
        k.key = 'tweet_%s.xml' % tweet['id']
        k.content_type = 'text/xml'
        k.set_contents_from_string(xml)
        k.set_acl('public-read')
        self.client.calls.create(to=phoneTo, from_=phoneFrom, method='GET',
                url='https://s3.amazonaws.com/twinty/tweet_%s.xml' % tweet['id'])

def getUsersJson():
    return json.loads(urlopen('https://s3.amazonaws.com/twinty/users.json').read().decode())


def listenWithExceptionHandler(auth, userIDs, bucket, client):
    print("Starting Twitter listener.")
    try:
        tweepy.Stream(auth, TweetListener(bucket, client)).filter(follow = userIDs)
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(str(e))
        listenWithExceptionHandler(auth, userIDs, bucket, client)


if __name__ == '__main__':
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    # twitter info
    auth = tweepy.OAuthHandler(authInfo['twitter_api_key'], authInfo['twitter_api_secret'])
    auth.set_access_token(authInfo['twiter_access_token'], authInfo['twitter_access_secret'])
    api = tweepy.API(auth)

    # twilio info
    client = Client(authInfo['twilio_acct_sid'], authInfo['twilio_auth_token'])
    # userIDs = set(str(api.get_user(handle).id) for handle in getUsersJson().keys())
    userIDs = set(str(user.id) for user in api.lookup_users(screen_names = getUsersJson().keys()))
    # print(userIDs)
    # raise SystemExit

    # aws info
    conn = boto.connect_s3(authInfo['aws_access_key'], authInfo['aws_secret_key'])
    bucket = conn.get_bucket('twinty')

    process = multiprocessing.Process(target=listenWithExceptionHandler, args=(auth, userIDs, bucket, client))
    process.start()

    while True:
        time.sleep(5)
        # newUserIDs = set(str(api.get_user(handle).id) for handle in getUsersJson().keys())
        newUserIDs = set(str(user.id) for user in api.lookup_users(screen_names = getUsersJson().keys()))

        # if someone has followed someone new who no one has followed before
        if newUserIDs != userIDs:
            userIDs = newUserIDs
            process.terminate()
            process = multiprocessing.Process(target=listenWithExceptionHandler, args=(auth, userIDs, bucket, client))
            process.start()
