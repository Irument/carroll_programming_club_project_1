from canvas import Canvas
import gui as gui_mod
import socketio as socketio_mod

canvas = Canvas('canvas')
socketio = socketio_mod.SocketIO()
gui = gui_mod.GUI(canvas, socketio)
gui.render_current_room()