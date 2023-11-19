from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import study as study_mod
import json

app = Flask(__name__)
socketio = SocketIO(app)
study = study_mod.Study()

@app.route('/')
def home():
    return render_template('home.html')

@socketio.on('get_quiz')
def get_quiz(client_id):
    socketio.emit('get_quiz_{}'.format(client_id), study.get_quiz())

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3432)
