from textblob import TextBlob as tb
from tweepy.streaming import StreamListener
from twilio.rest import Client
import tweepy
import json


phoneFrom = '+16178588543'

xmlFormat = '''
<Response>
    <Say voice="alice">Tweet from %s: %s</Say>
</Response>
'''

class TweetListener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)

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

def follow(handles, phoneToCall):
    userIDs = [str(api.get_user(handle).id) for handle in handles]
    listener = TweetListener(userIDs, phoneToCall)
    stream = tweepy.Stream(auth, listener)
    stream.filter(follow = userIDs)

def call(phoneTo, tweet):
    xml = xmlFormat % (tweet['user']['name'], tweet['text'])
    print(xml)
    with open('tweet_%s.xml' % tweet['id'], 'w') as f:
        f.write(xml)
    # TODO: upload xml to aws bucket
    client.calls.create(to=phoneTo, from_=phoneFrom, url='https://s3.amazonaws.com/twinty/test.xml') # TODO: add url


if __name__ == '__main__':
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    # twitter info
    apiKey = authInfo['twitter_api_key']
    apiSecret = authInfo['twitter_api_secret']
    accessToken = authInfo['twiter_access_token']
    accessTokenSecret = authInfo['twitter_access_secret']
    auth = tweepy.OAuthHandler(apiKey, apiSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    # twilio info
    account_sid = authInfo['twilio_acct_sid']
    auth_token = authInfo['9708b8d521dff44151d866bbd7b41498']
    client = Client(account_sid, auth_token)

    with open('users.json') as f:
        handleToNumbers = json.loads(f.read())

    userIDs = [str(api.get_user(handle).id) for handle in handleToNumbers.keys()]
    tweepy.Stream(auth, TweetListener()).filter(follow = userIDs)
