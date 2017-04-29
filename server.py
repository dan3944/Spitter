from tweepy.streaming import StreamListener
import tweepy
import json

apiKey = 'jwTBei3GYpKFKzHIpXNd9ebqn'
apiSecret = '0oh3ElCt3zq14usCfx5zwWb6BtAufsPWzADHhmFS5fhg67WLPs'
accessToken = '858396934394040320-6eFsVJLtuNI58i6XXTIAUP4s4ldsrlE'
accessTokenSecret = 'Tnn314Jj1k7Co3Qqs0cCIlwnsPEhPW3I1wivYVyL0LZGm'
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

xmlFormat = '''
<Response>
    <Say voice="alice">Tweet from %s: %s</Say>
</Response>
'''

class TweetListener(StreamListener):
    userIDs = None

    def __init__(self, userIDs):
        self.userIDs = userIDs

    def on_data(self, data):
        data = json.loads(data)

        if 'user' in data and data['user']['id_str'] in self.userIDs:
            xml = xmlFormat % (data['user']['name'], data['text'])
            print(xml, "\n")
            with open('tweet_%s.xml' % data['id'], 'w') as f:
                f.write(xml)

def follow(handles):
    userIDs = [str(api.get_user(handle).id) for handle in handles]
    listener = TweetListener(userIDs)
    stream = tweepy.Stream(auth, listener)
    stream.filter(follow = userIDs)

if __name__ == '__main__':
    follow(['realDonaldTrump', 'BarackObama', 'MBTA', 'TheEllenShow', 'heribberto'])
