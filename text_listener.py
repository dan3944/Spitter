from flask import Flask
import json
import tweepy

app = Flask(__name__)

@app.route('/receive_text')
def receiveText():
    # TODO: kill and restart server.py
    # TODO: return error or success
    fromNumber = ???
    msgText = ???
    words = msgText.split()
    
    if len(words) < 2:
        return

    action = words[0].upper()
    handle = words[1]

    if action not in ('FOLLOW', 'UNFOLLOW'):
        return
    elif not isHandle(handle)
        return

    with open('users.json') as f:
        handleToPhones = json.loads(f.read())

    phones = handleToPhones.get(handle, [])

    if action == 'FOLLOW' and fromNumber not in phones:
        phones.add(fromNumber)
    elif action == 'UNFOLLOW' and fromNumber in phones:
        phones.remove(fromNumber)

    handleToPhones[handle] = phones

    with open('users.json', 'w') as f:
        f.write(json.dumps(handleToPhones))

def isHandle(handle):
    with open('auth.json') as f:
        authInfo = json.loads(f.read())

    # twitter info
    auth = tweepy.OAuthHandler(authInfo['twitter_api_key'], authInfo['twitter_api_secret'])
    auth.set_access_token(authInfo['twiter_access_token'], authInfo['twitter_access_secret'])
    api = tweepy.API(auth)

    try:
        api.get_user(handle)
        return True
    except tweepy.error.TweepError:
        return False


if __name__ == '__main__':
    app.run()