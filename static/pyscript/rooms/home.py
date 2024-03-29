import rooms

class Room(rooms.BaseRoom):
    def room_specific_init(self):
        self.gui.shared.clicks = 0
    
    def click(self):
        self.gui.shared.clicks += 1
    
    def answer_questions(self):
        self.gui.room = 'quiz'

    def render(self):
        self.canvas.text(str(self.gui.shared.clicks), self.canvas.canvas.width/2, self.canvas.canvas.height/3, 'Arial', 30)
        self.canvas.add_button((self.canvas.canvas.width/2)-65, (self.canvas.canvas.height/2)-65, 130, 130, '/static/img/coffee.png', self.click)
        self.canvas.add_button((self.canvas.canvas.width/2)-75, ((self.canvas.canvas.height/4)*3)-25, 150, 50, '/static/img/answer_questions.png', self.answer_questions)
