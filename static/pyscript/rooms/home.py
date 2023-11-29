import rooms
import string
import random
from js import console
import json

def get_random_string(length):
    choice = string.ascii_uppercase + string.ascii_lowercase + string.digits
    final = ''
    for x in range(length):
        final += random.choice(choice)
    return final

class AnswerBoxCallbacks:
    """
    Callbacks for every answer box. Knows what the correct answer box is, and
    goes to the next question if it is correct. If not, show text box that says
    "Incorrect!", count it as wrong and don't move to the next question.
    """

    def __init__(self, room):
        self.room = room
        self.correct_answer = None
        self.current_question_wrong = False
    
    def correct(self):
        if not self.current_question_wrong:
            self.room.gui.shared.correct_questions += 1
        self.current_question_wrong = False
        self.room.gui.render_current_room()

    def wrong(self):
        self.current_question_wrong = True
        self.room.canvas.text('Incorrect!', self.room.canvas.canvas.width/2, 60, 'Arial', 20, fillStyle='red')

    def check_wrong(self, box):
        if self.correct_answer == box:
            self.correct()
        else:
            self.wrong()

    def topleft(self):
        self.check_wrong('topleft')
    def topright(self):
        self.check_wrong('topright')
    def bottomleft(self):
        self.check_wrong('bottomleft')
    def bottomright(self):
        self.check_wrong('bottomright')
    
    def add_answers(self):
        """
        Gets a random box and chooses it as the correct one. It puts the correct
        answer for that box, and generates random offsets from the correct answer
        for the other incorrect answers.
        """

        boxes = {'topleft': [125, 312], 'topright': [375, 312], 'bottomleft': [125, 437], 'bottomright': [375, 437]}
        offsets = random.sample([i for i in range(-6, 7) if i != 0], 4)
        x = 0
        for box in boxes:
            xy = boxes[box]
            if box == self.correct_answer:
                self.room.canvas.text('{}'.format(self.room.questions[self.room.current_question][1]), xy[0], xy[1], 'Arial', 20)
            else:
                self.room.canvas.text('{}'.format(int(self.room.questions[self.room.current_question][1])+offsets[x]), xy[0], xy[1], 'Arial', 20)
                x += 1

class Room(rooms.BaseRoom):
    def room_specific_init(self):
        self.client_id = get_random_string(10)
        self.register_socketio_events()
        self.answer_box_callbacks = AnswerBoxCallbacks(self)
        self.questions = [] # Quiz questions/answers are stored here by an array with index 0 being the question and index 1 being the answer
        self.current_question = 0 # Index for self.questions
        self.gui.shared.correct_questions = 0

    def render(self):
        self.canvas.canvas.style.background = '#f9f9f9'
        if self.questions == []:
            self.socketio.emit('get_quiz', self.client_id)
        else:
            self.current_question += 1
            if len(self.questions)-1 < self.current_question: # Check for end of quiz
                self.gui.room = 'scores'
                self.gui.render_current_room()
                return
            
            self.canvas.text(self.questions[self.current_question][0], self.canvas.canvas.width/2, self.canvas.canvas.height/3, 'Arial', 25)
            self.canvas.text('Question {} of {}'.format(self.current_question+1, len(self.questions)), 0, 0, 'Arial', 10)
        self.create_question_boxes()
        if not self.questions == []:
            self.answer_box_callbacks.add_answers()
        self.canvas.load_images()

    
    def create_question_boxes(self):
        """
        Makes the answer buttons. All questions right now are math based, and are just a number.
        For now, I am just converting the answer to an int and randomly changing the number a bit
        for wrong answers
        """

        self.canvas.prepare_image('answer_box', '/static/img/answer_box.png')
        self.answer_box_callbacks.correct_answer = random.choice(['topleft', 'topright', 'bottomleft', 'bottomright'])
        self.canvas.add_button(0, self.canvas.canvas.height/2, 250, 125, 'answer_box', self.answer_box_callbacks.topleft)
        self.canvas.add_button(250, self.canvas.canvas.height/2, 250, 125, 'answer_box', self.answer_box_callbacks.topright)
        self.canvas.add_button(0, self.canvas.canvas.height/2+125, 250, 125, 'answer_box', self.answer_box_callbacks.bottomleft)
        self.canvas.add_button(250, self.canvas.canvas.height/2+125, 250, 125, 'answer_box', self.answer_box_callbacks.bottomright)
    
    def register_socketio_events(self):
        @self.socketio.on('answer_check_{}'.format(self.client_id))
        def answer_check_response(result):
            if result:
                self.gui.room = 'correct'
                self.gui.render_current_room()
            else:
                self.gui.room = 'wrong'
                self.gui.render_current_room()
        
        @self.socketio.on('get_quiz_{}'.format(self.client_id))
        def get_quiz_response(quiz):
            new_quiz = {}
            x = 0
            keys = quiz.object_keys()
            values = quiz.object_values()
            for key in keys:
                new_quiz[key] = values[x]
                x += 1
            quiz = new_quiz
            
            for question in quiz:
                self.questions.append([question, quiz[question]])
            self.canvas.text(self.questions[self.current_question][0], self.canvas.canvas.width/2, self.canvas.canvas.height/3, 'Arial', 25)
            self.gui.shared.question_count = len(self.questions)
            self.answer_box_callbacks.add_answers()
