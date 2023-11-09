import rooms

class Room(rooms.BaseRoom):
    def render(self):
        self.canvas.canvas.style.background = '#f9f9f9'
        self.canvas.circle(250, 250, 100)
        self.canvas.text('Hello, World!', 250, 450, 'Arial', 25)
        self.canvas.rect(200, 200, 100, 100)
        def test_button_callback():
            """
            Switches rooms to testRoom
            """

            self.gui.room = 'testRoom'
            self.gui.render_current_room()

        self.canvas.add_button(10, 10, 200, 100, '/static/img/test_button.png', test_button_callback)
    
    def keyDown(self, key):
        
        self.reRender()
        self.canvas.text('{}'.format(key), 250, 250, 'Arial', 10)
