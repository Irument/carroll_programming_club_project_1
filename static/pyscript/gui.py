import importlib
from js import console

class SharedData:
    """
    Blank object that all rooms would have access to. This makes it more organized to
    share data between rooms
    """

    def __init__(self):
        pass

class GUI:
    def __init__(self, canvas, socketio):
        """
        The GUI is in rooms. It will know what to render based on
        what room it is in. Rooms are only rendered again if something needs to be changed.
        To add a room, it needs to be mentioned in a few places. A python file with a render
        function needs to be added to /static/pyscript/rooms, with the filename being the name
        of the room. The path needs to be mentioned in the /templates/home.html file, under the
        py-env element in the same format as the other ones. The room also needs to be mentioned
        here under the rooms array below. There also cannot be another module with the same
        name as a room. They will conflict.
        """
        self.room = 'waiting_for_quiz'
        self.canvas = canvas
        self.socketio = socketio
        self.shared = SharedData()
        rooms = [
            'home',
            'scores',
            'waiting_for_quiz'
        ]
        self.rooms = {}
        for room in rooms:
            self.rooms[room] = importlib.import_module(room).Room(self, self.canvas, self.socketio)

    def render_current_room(self):
        """
        Rooms are stored in the rooms folder. They need to have a render function, that this
        function calls.
        """

        self.canvas.clear()
        self.rooms[self.room].render()
        self.canvas.room = self.rooms[self.room]
        self.canvas.room_name = self.room
        console.log('Room {} rendered.'.format(self.room))
