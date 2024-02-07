class BaseRoom:
    def __init__(self, gui, canvas, socketio):
        """
        gui is an object that is defined in /static/pyscript/gui.py. It handles rooms.
        canvas is an object that is defined in /static/pyscript/canvas.py and it has functions for interacting with the canvas.
        socketio is an object that is defined in /static/pyscript/socketio.py. It handles communication with the server.
        """

        self.gui = gui
        self.canvas = canvas
        self.socketio = socketio
        self.room_specific_init()

    def room_specific_init(self):
        """
        This is called in __init__. This is here for
        if some other room-specific variables need to
        be defined on init.
        """

        pass

    def render_start(self):
        """
        Ran when the room is switched
        """

        pass

    def render(self):
        """
        Do canvas stuff here. Ran 60 times a second
        """

        pass

    def reRender(self):
        """
        Clears canvas and renders again.
        """

        self.canvas.clear()
        self.render()

    def keyDown(self, keyCode):
        """
        Do something when a key is pressed
        """

        pass

    def keyUp(self, keyCode):
        """
        Do something when a key is released
        """

        pass
