def render(gui, canvas):
    def test_button_callback():
        """
        Switches rooms to home
        """

        gui.room = 'home'
        gui.render_current_room()
    
    canvas.text('Some room', 250, 450, 'Arial', 25)
    canvas.add_button(10, 10, 200, 100, '/static/img/test_button.png', test_button_callback)
