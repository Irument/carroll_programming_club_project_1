import rooms

class Room(rooms.BaseRoom):
    def render(self):
        def test_button_callback():
            """
            Switches rooms to home
            """

            self.gui.room = 'home'
            self.gui.render_current_room()
        
        self.canvas.text('Some room', 250, 450, 'Arial', 25)
        self.canvas.add_button(10, 10, 200, 100, '/static/img/test_button.png', test_button_callback)
