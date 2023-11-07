class BaseRoom:
    def __init__(self, gui, canvas):
        """
        gui is an object that is defined in /static/pyscript/gui.py. It handles rooms.
        canvas is an object that is defined in /static/pyscript/canvas.py and it has functions for interacting with the canvas.
        """

        self.gui = gui
        self.canvas = canvas
        self.room_specific_init()

    def room_specific_init(self):
        """
        This is called in __init__. This is here for
        if some other room-specific variables need to
        be defined on init.
        """

        pass

    def render(self):
        """
        Do canvas stuff here
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
