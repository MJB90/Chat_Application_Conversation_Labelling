from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import saveConvo

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

# Global Variables
isTrain = True
conversation = []

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdkfngk'
socketio = SocketIO(app)


def check_bye(json):
    for key, value in json.items():
        if str(value) == 'Bye' or str(value) == 'bye':
            return True

    return False


def check_connected(json):
    for key, value in json.items():
        if str(key) == 'data':
            return True

    return False


@app.route('/')
def hello():
    return render_template('./ChatApp.html')


def messageRecived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json):
    global conversation
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageRecived)
    is_connected = check_connected(json)

    if not is_connected:
        conversation.append(json)

    is_bye = check_bye(json)
    if is_bye:
        # saveConvo.save_conversation(conversation)
        # conversation = []
         return redirect(url_for('/'))



if __name__ == '__main__':
    socketio.run(app, debug=True)
