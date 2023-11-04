def render(gui, canvas, persistant):
    canvas.canvas.style.background = '#f9f9f9'
    canvas.circle(250, 250, 100)
    canvas.text('Hello, World!', 250, 450, 'Arial', 25)
    canvas.rect(200, 200, 100, 100)
    def test_button_callback():
        """
        Switches rooms to testRoom
        """

        gui.room = 'testRoom'
        gui.render_current_room()

    canvas.add_button(10, 10, 200, 100, '/static/img/test_button.png', test_button_callback)