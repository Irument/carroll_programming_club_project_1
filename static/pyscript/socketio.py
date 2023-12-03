from js import io
from functools import wraps
from pyodide import create_proxy
import string
import random
import json

def get_random_string(length):
    choice = string.ascii_uppercase + string.ascii_lowercase + string.digits
    final = ''
    for x in range(length):
        final += random.choice(choice)
    return final

class SocketIO:
    """
    Communication with the server
    """

    def __init__(self):
        """
        Connects to server
        """

        self.client_id = get_random_string(10)
        self.socket = io()
    
    def on(self, event, **kwargs):
        """
        Decorator for handling events
        """

        def decorator(f):
            self.socket.on(event, create_proxy(f))
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped
        return decorator

    def emit(self, event, data):
        """
        Send data to server
        """

        data = json.dumps(data)
        create_proxy(self.socket.emit(event, data))
