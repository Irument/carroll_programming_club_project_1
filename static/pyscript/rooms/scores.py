import rooms

class Room(rooms.BaseRoom):
    def retry(self):
        self.gui.room = 'quiz'
        self.gui.shared.correct_questions = 0
        self.gui.rooms['quiz'].current_question = -1 # When home is rendered, it adds 1 to the current_question. 0 would skip the first question.
    
    def back(self):
        self.gui.room = 'home'
        self.gui.shared.correct_questions = 0
        self.gui.rooms['quiz'].current_question = -1

    def render(self):
        self.canvas.text('Score', self.canvas.canvas.width/2, 150, 'Arial', 30)
        self.canvas.text('{}/{}'.format(self.gui.shared.correct_questions, self.gui.shared.question_count), self.canvas.canvas.width/2, 200, 'Arial', 25)
        self.canvas.text('{}%'.format(round(self.gui.shared.correct_questions/self.gui.shared.question_count*100)), self.canvas.canvas.width/2, 250, 'Arial', 25)
        self.canvas.add_button(self.canvas.canvas.width/2-50, 275, 100, 50, '/static/img/retry.png', self.retry)
        self.canvas.add_button(self.canvas.canvas.width/2-50, 350, 100, 50, '/static/img/back.png', self.back)
