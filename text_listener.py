from flask import Flask
import json

app = Flask(__name__)

@app.route('/receive_text')
def receiveText():
    fromNumber = ???
    msgText = ???
    words = msgText.split()
    
    if len(words) < 2:
        return

    action = words[0].upper()
    handle = words[1]

    if action not in ('FOLLOW', 'UNFOLLOW'):
        return

    # TODO: check if valid handle
    # TODO: return error

    with open('users.json') as f:
        handleToPhones = json.loads(f.read())

    if handle in handleToPhones:
        if fromNumber not in handleToPhones[handle]:
            handleToPhones[handle].add(fromNumber)
    else:
        handleToPhones = [fromNumber]

    with open('users.json', 'w') as f:
        f.write(json.dumps(handleToPhones))

if __name__ == '__main__':
    app.run()
