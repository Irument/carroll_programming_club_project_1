import rooms
import string
import random
from js import console
import json

class AnswerBoxCallbacks:
    """
    Callbacks for every answer box. Knows what the correct answer box is, and
    goes to the next question if it is correct. If not, show text box that says
    "Incorrect!", count it as wrong and don't move to the next question.
    """

    def __init__(self, room):
        self.room = room
        self.current_question_wrong = False
        self.correct_answer = None
    
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

        left = int(self.room.canvas.canvas.width/4)
        right = int(self.room.canvas.canvas.width/4*3)
        top = int(self.room.canvas.canvas.height/8*5)
        bottom = int(self.room.canvas.canvas.height/8*7)

        boxes = {
            'topleft': [left, top],
            'topright': [right, top],
            'bottomleft': [left, bottom],
            'bottomright': [right, bottom]
        }

        box_order = ['topleft', 'topright', 'bottomleft', 'bottomright']
        random.shuffle(box_order)
        self.correct_answer = box_order[0]
        if self.room.questions[self.room.current_question]['choices'] == []:
            offsets = random.sample([i for i in range(-6, 7) if i != 0], 4)
            x = 0
            for box in box_order:
                xy = boxes[box]
                if x == 0:
                    self.room.canvas.text('{}'.format(self.room.questions[self.room.current_question]['answer']), xy[0], xy[1], 'Arial', 20)
                else:
                    self.room.canvas.text('{}'.format(int(self.room.questions[self.room.current_question]['answer'])+offsets[x-1]), xy[0], xy[1], 'Arial', 20)
                x += 1
        else:
            x = 0
            for box in box_order:
                xy = boxes[box]
                if x == 0:
                    self.room.canvas.text('{}'.format(self.room.questions[self.room.current_question]['answer']), xy[0], xy[1], 'Arial', 20)
                else:
                    self.room.canvas.text('{}'.format(self.room.questions[self.room.current_question]['choices'][x-1]), xy[0], xy[1], 'Arial', 20)
                x += 1

class Room(rooms.BaseRoom):
    def room_specific_init(self):
        self.register_socketio_events()
        self.answer_box_callbacks = AnswerBoxCallbacks(self)
        self.questions = [] # Quiz questions/answers are stored here by an array with index 0 being the question and index 1 being the answer
        self.current_question = 0 # Index for self.questions
        self.gui.shared.correct_questions = 0
        self.gui.shared.quiz_name = None

    def render(self):
        self.canvas.canvas.style.background = '#f9f9f9'
        if self.questions == []:
            self.socketio.emit('get_quiz', {'client_id': self.socketio.client_id, 'quiz_id': self.gui.shared.quiz_id})
        else:
            self.current_question += 1
            if len(self.questions)-1 < self.current_question: # Check for end of quiz
                self.gui.room = 'scores'
                self.gui.render_current_room()
                return
            
            self.canvas.text(self.questions[self.current_question]['question'], self.canvas.canvas.width/2, self.canvas.canvas.height/3, 'Arial', 25)
            self.canvas.text('Question {} of {}'.format(self.current_question+1, len(self.questions)), 0, 0, 'Arial', 10)
        self.create_question_boxes()
        if not self.questions == []:
            self.answer_box_callbacks.add_answers()
        self.canvas.load_images()

    
    def create_question_boxes(self):
        """
        Makes the answer buttons. For math questions that only have a number answer, there is
        just an offset from the correct answer instead of filling out each choice box.
        """

        self.canvas.prepare_image('answer_box', '/static/img/answer_box.png')
        self.canvas.add_button(0, self.canvas.canvas.height/2, 250, 125, 'answer_box', self.answer_box_callbacks.topleft)
        self.canvas.add_button(250, self.canvas.canvas.height/2, 250, 125, 'answer_box', self.answer_box_callbacks.topright)
        self.canvas.add_button(0, self.canvas.canvas.height/2+125, 250, 125, 'answer_box', self.answer_box_callbacks.bottomleft)
        self.canvas.add_button(250, self.canvas.canvas.height/2+125, 250, 125, 'answer_box', self.answer_box_callbacks.bottomright)
    
    def register_socketio_events(self):
        @self.socketio.on('answer_check_{}'.format(self.socketio.client_id))
        def answer_check_response(result):
            if result:
                self.gui.room = 'correct'
                self.gui.render_current_room()
            else:
                self.gui.room = 'wrong'
                self.gui.render_current_room()
        
        @self.socketio.on('get_quiz_{}'.format(self.socketio.client_id))
        def get_quiz_response(quiz):
            quiz = json.loads(quiz)
            self.questions = quiz[0]
            self.quiz_name = quiz[1]
            self.canvas.text(self.questions[self.current_question]['question'], self.canvas.canvas.width/2, self.canvas.canvas.height/3, 'Arial', 25)
            self.gui.shared.question_count = len(self.questions)
            self.answer_box_callbacks.add_answers()
