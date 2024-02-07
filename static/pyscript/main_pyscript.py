from canvas import Canvas
import gui as gui_mod
import socketio as socketio_mod

from js import set_exec
from pyodide import create_proxy

def execute_python_code(code):
    # Since it is a built-in function, I can't pass that directly to javscript or else it would raise SystemError
    exec(code)

set_exec(create_proxy(execute_python_code))

canvas = Canvas('canvas')
socketio = socketio_mod.SocketIO()
gui = gui_mod.GUI(canvas, socketio)
gui.render_current_room()
