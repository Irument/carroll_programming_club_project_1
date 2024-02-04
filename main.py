from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import study as study_mod
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
study = study_mod.Study('main.db')

@app.route('/')
def home():
    return render_template('home.html', imgs=os.listdir('static/img'))

@socketio.on('get_quiz')
def get_quiz(data):
    data = json.loads(data)
    client_id = data['client_id']
    quiz_id = data['quiz_id']

    if study.quiz_exists(quiz_id):
        socketio.emit('get_quiz_{}'.format(client_id), json.dumps(study.get_quiz(quiz_id)))
    else:
        socketio.emit('get_quiz_{}'.format(client_id), False)

@socketio.on('check_quiz')
def check_quiz(data):
    data = json.loads(data)
    client_id = data['client_id']
    quiz_id = data['quiz_id']

    socketio.emit('check_quiz_{}'.format(client_id), json.dumps({'exists': study.quiz_exists(quiz_id), 'quiz_id': quiz_id}))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3432)
