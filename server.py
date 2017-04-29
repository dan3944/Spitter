# from textblob import TextBlob as tb
from tweepy.streaming import StreamListener
from twilio.rest import Client
from boto.s3.key import Key
import boto.s3
import tweepy
import json

phoneFrom = '+16178588543'

xmlTemplate = '''
<Response>
    <Say voice="alice">Tweet from %s: %s</Say>
</Response>
'''

class TweetListener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        handleToNumbers = getUsersJson()

        if 'user' in data and data['user']['screen_name'] in handleToNumbers.keys():
            phonesToCall = handleToNumbers[data['user']['screen_name']]
            
            for phoneNum in phonesToCall:
                call(phoneNum, data)

            # # detect emotion
            # blob = tb(data['text'])
            # sent = blob.sentiment
            # polarity = sent.polarity  # the negativity or positivity of the tweet, on a -1 to 1 scale
            # if polarity > 0:
            #     print('feeling positive! %s', polarity)
            # else:
            #     print('feeling negative! %s', polarity)

def call(phoneTo, tweet):
    xml = xmlTemplate % (tweet['user']['name'], tweet['text'])
    print(xml)
    k = Key(bucket)
    k.key = 'tweet_%s.xml' % tweet['id']
    k.set_contents_from_string(xml)
    k.set_acl('public-read')
    client.calls.create(to=phoneTo, from_=phoneFrom, method='GET',
            url='https://s3.amazonaws.com/twinty/tweet_%s.xml' % tweet['id'])

def getUsersJson():
    with open('users.json') as f:
        tmp = f.read()
    return json.loads(tmp)


if __name__ == '__main__':
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    # twitter info
    auth = tweepy.OAuthHandler(authInfo['twitter_api_key'], authInfo['twitter_api_secret'])
    auth.set_access_token(authInfo['twiter_access_token'], authInfo['twitter_access_secret'])
    api = tweepy.API(auth)

    # twilio info
    client = Client(authInfo['twilio_acct_sid'], authInfo['twilio_auth_token'])
    userIDs = [str(api.get_user(handle).id) for handle in getUsersJson().keys()]

    # aws info
    conn = boto.connect_s3(authInfo['aws_access_key'], authInfo['aws_secret_key'])
    bucket = conn.get_bucket('twinty')

    tweepy.Stream(auth, TweetListener()).filter(follow = userIDs)
