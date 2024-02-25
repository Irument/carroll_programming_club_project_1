from js import document, console
from pyodide import create_proxy
import rooms
import json

class Room(rooms.BaseRoom):
    def room_specific_init(self):
        self.register_socketio_events()
        document.getElementById('quiz_id_start').addEventListener('click', create_proxy(self.start))

    def start(self, e):
        """
        Start button callback outside of
        canvas. Emits a socketio event
        for checking if the quiz mentioned
        exists
        """

        quiz_id = document.getElementById('quiz_id').value
        self.socketio.emit('check_quiz', {'client_id': self.socketio.client_id, 'quiz_id': quiz_id})

    def render(self):
        self.canvas.canvas.style.background = '#f9f9f9'
        self.canvas.text('Enter a quiz ID below', self.canvas.canvas.width/2, self.canvas.canvas.height/2, 'Arial', 30)
    
    def register_socketio_events(self):
        @self.socketio.on('check_quiz_{}'.format(self.socketio.client_id))
        def check_quiz_response(data):
            """
            Response from the server for the
            start button's callback emitting an
            event for checking if the quiz exists.
            If it exists, switch rooms to home. 
            If it does not exist, show invalid
            quiz id text on the canvas.
            """

            data = json.loads(data)
            if data['exists']:
                document.getElementById('quiz_id_container').setAttribute('style', 'display: none;')
                self.gui.shared.quiz_id = data['quiz_id']
                self.gui.rooms['quiz'].questions = []
                self.gui.rooms['quiz'].current_question = 0
                self.gui.shared.correct_questions = 0
                self.gui.room = 'home'
            else:
                if self.gui.room == 'waiting_for_quiz':
                    self.canvas.text('Invalid quiz ID', self.canvas.canvas.width/2, self.canvas.canvas.height/3*2, 'Arial', 20, fillStyle='red')
