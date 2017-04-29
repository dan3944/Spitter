from textblob import TextBlob as tb
from tweepy.streaming import StreamListener
from twilio.rest import Client
from flask import Flask
import tweepy
import json

# twitter info
apiKey = 'jwTBei3GYpKFKzHIpXNd9ebqn'
apiSecret = '0oh3ElCt3zq14usCfx5zwWb6BtAufsPWzADHhmFS5fhg67WLPs'
accessToken = '858396934394040320-6eFsVJLtuNI58i6XXTIAUP4s4ldsrlE'
accessTokenSecret = 'Tnn314Jj1k7Co3Qqs0cCIlwnsPEhPW3I1wivYVyL0LZGm'
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# twilio info
account_sid = "ACc4bd56b82a463f76094cf22dfcc0e7a3"
auth_token = "01a0ecc27726f2f049d6d9318bcc7bfd"
client = Client(account_sid, auth_token)
phoneFrom = '+16178588543'

xmlFormat = '''
<Response>
    <Say voice="alice">Tweet from %s: %s</Say>
</Response>
'''

# twitter_handle -> [phone_number]
users = {
    'realDonaldTrump' : ['+16098656527'],
    'BarackObama' : ['+16098656527'],
    'TheEllenShow' : ['+16098656527'],
    'heribberto' : ['+16098656527'],
}

class TweetListener(StreamListener):
    userIDs = None
    phoneToCall = None

    def __init__(self, userIDs, phoneToCall):
        self.userIDs = userIDs
        self.phoneToCall = phoneToCall

    def on_data(self, data):
        data = json.loads(data)

        if 'user' in data and data['user']['id_str'] in self.userIDs:
            call(self.phoneToCall, data)

            xml = xmlFormat % (data['user']['name'], data['text'])
            print(xml, "\n")
            with open('tweet_%s.xml' % data['id'], 'w') as f:
                f.write(xml)
            # detect emotion
            blob = tb(data['text'])
            sent = blob.sentiment
            polarity = sent.polarity  # the negativity or positivity of the tweet, on a -1 to 1 scale
            if polarity > 0:
                print('feeling positive! %s', polarity)
            else:
                print('feeling negative! %s', polarity)

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
    client.calls.create(to=phoneTo, from_=phoneFrom, url='https://s3.amazonaws.com/twinty/test.xml') # TODO: add url

@app.route('/receive_text')
def receiveText():
    # add to or remove from users
    pass

if __name__ == '__main__':
    follow(['realDonaldTrump', 'BarackObama', 'MBTA', 'TheEllenShow', 'heribberto'], 'Twinty5', '+16098656527')
