from flask import Flask
from twilio.rest import Client
import json
import tweepy

app = Flask(__name__)

@app.route('/receive_text')
def receiveText():
    fromNumber = ???
    msgText = ???
    words = msgText.split()
    
    if len(words) < 2:
        send(fromNumber, 'Your message must include both an action and a twitter handle.')

    action = words[0].upper()
    handle = words[1]

    if action not in ('FOLLOW', 'UNFOLLOW'):
        send(fromNumber, 'Your action must be either "Follow" or "Unfollow". Your action was "%s".' % action)
    elif not handleExists(handle):
        send(fromNumber, 'Could not find the twitter handle "%s"' % handle)

    with open('users.json') as f:
        tmp = f.read()
    handleToPhones = json.loads(tmp)

    phones = handleToPhones.get(handle, [])

    if action == 'FOLLOW' and fromNumber not in phones:
        phones.add(fromNumber)
    elif action == 'UNFOLLOW' and fromNumber in phones:
        phones.remove(fromNumber)

    handleToPhones[handle] = phones

    tmp = json.dumps(handleToPhones)
    with open('users.json', 'w') as f:
        f.write(tmp)

    send(fromNumber, "You have %s %s" % (action, handle))

def handleExists(handle):
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    auth = tweepy.OAuthHandler(authInfo['twitter_api_key'], authInfo['twitter_api_secret'])
    auth.set_access_token(authInfo['twiter_access_token'], authInfo['twitter_access_secret'])
    api = tweepy.API(auth)

    try:
        api.get_user(handle)
        return True
    except tweepy.error.TweepError:
        return False

def send(phoneNumber, text):
    client.api.account.messages.create(to=phoneNumber, from_="+16178588543", body=text)


if __name__ == '__main__':
    with open('auth.json') as f:
        authInfo = json.loads(f.read())
    
    # twilio info
    client = Client(authInfo['twilio_acct_sid'], authInfo['twilio_auth_token'])
    userIDs = [str(api.get_user(handle).id) for handle in getUsersJson().keys()]

    app.run()
