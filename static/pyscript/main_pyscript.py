from canvas import Canvas
import gui as gui_mod

canvas = Canvas('canvas')
gui = gui_mod.GUI(canvas)
gui.render_current_room()
