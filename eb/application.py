from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import json
import tweepy

application = Flask(__name__)

@application.route('/test', methods=['GET', 'POST'])
def test():
    return 'test'


@application.route('/receive_text', methods=['GET', 'POST'])
def receiveText():
    fromNumber = request.values.get('From')
    msgText = request.values.get('Body')

    if fromNumber is None or msgText is None:
        return str(MessagingResponse().message('Error: Malformed message.'))

    words = msgText.split()

    if len(words) < 2:
        return str(MessagingResponse().message(
            'Your message must include both an action and a twitter handle.'))

    action = words[0].upper()
    handle = words[1]

    if action not in ('FOLLOW', 'UNFOLLOW'):
        return str(MessagingResponse().message(
            'Your action must be either "Follow" or "Unfollow". Your action was "%s".' % action))
    elif not handleExists(handle):
        return str(MessagingResponse().message('Could not find the twitter handle "%s"' % handle))

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

    return str(MessagingResponse().message("You have %s %s" % (action, handle)))

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


if __name__ == '__main__':
    # with open('auth.json') as f:
    #     authInfo = json.loads(f.read())
    
    # client = Client(authInfo['twilio_acct_sid'], authInfo['twilio_auth_token'])
    client = Client('AC0941a173f445c6837eda96d803bf31f6', '9708b8d521dff44151d866bbd7b41498')

    application.debug = True
    application.run()
