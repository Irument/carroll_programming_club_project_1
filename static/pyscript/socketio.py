from js import io
from functools import wraps
from pyodide import create_proxy

class SocketIO:
    """
    Communication with the server
    """

    def __init__(self):
        """
        Connects to server
        """

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

        create_proxy(self.socket.emit(event, data))
