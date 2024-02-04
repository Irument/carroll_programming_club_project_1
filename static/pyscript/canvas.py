from js import document, console
from pyodide import create_proxy
import math
import json

class Canvas:
    def __init__(self, canvas):
        self.canvas = document.getElementById(canvas)
        self.canvas.onmousedown = self.on_mouse_down
        document.body.addEventListener('keydown', create_proxy(self.on_key_down), False)
        document.body.addEventListener('keyup', create_proxy(self.on_key_up), False)
        self.buttons = []
        self.keys_pressed = []
        # Set by gui object
        self.room = None
        self.room_name = None

    def ctx(self):
        """
        Gets context
        """

        return self.canvas.getContext('2d')

    def clear(self):
        """
        Clears the canvas
        """

        self.buttons = []
        ctx = self.ctx()
        ctx.fillStyle = '#eaeaea'
        ctx.fillRect(0, 0, self.canvas.width, self.canvas.height)

    def circle(self, x, y, r):
        """
        Makes a circle with the specified XY coordinates and radius.
        """

        ctx = self.ctx()
        ctx.beginPath()
        ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.stroke()

    def text(self, text, x, y, font, fontsize, center=True, fillStyle='black'):
        """
        Draws text. Newlines work.
        """

        ctx = self.ctx()
        ctx.font = '{}px {}'.format(fontsize, font)
        ctx.fillStyle = fillStyle
        if center:
            ctx.textAlign = 'center'
        lines = text.split('\n')
        z = 0
        for line in lines:
            ctx.fillText(str(line), x, y+(z*fontsize))
            z += 1

    def rect(self, x, y, width, height):
        """
        Makes a rectangle
        """

        ctx = self.ctx()
        ctx.rect(x, y, width, height)
        ctx.stroke()

    def add_image(self, x, y, link, w=None, h=None):
        """
        Adds an image to the canvas by link
        """

        ctx = self.ctx()
        
        if not w == None and not h == None:
            ctx.drawImage(document.getElementById(link), x, y, w, h)
        else:
            ctx.drawImage(document.getElementById(link), x, y)

    def add_button(self, x, y, w, h, link, callback):
        """
        Adds an image to the canvas that acts as a button
        """

        self.buttons.append({
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'callback': callback
        })

        ctx = self.ctx()
        ctx.drawImage(document.getElementById(link), x, y, w, h)

    def on_mouse_down(self, e):
        """
        Runs callback for pressed buttons
        """

        canvas_rect = self.canvas.getBoundingClientRect()
    
        x = e.x - canvas_rect.left
        y = e.y - canvas_rect.top

        for button in self.buttons:
            if x >= button['x'] and x <= button['x'] + button['w'] and y >= button['y'] and y <= button['y'] + button['h']:
                button['callback']()
    
    def on_key_down(self, e):
        """
        Handles for key presses
        """

        if e.key in self.keys_pressed:
            return

        if 65 <= e.keyCode <= 90 and len(e.key) == 1:
            upper = e.shiftKey
            if e.getModifierState('CapsLock'):
                upper = not upper
            if upper:
                key = e.key.upper()
            else:
                key = e.key.lower()
        else:
            key = e.key
        self.keys_pressed.append(e.key)
        self.room.keyDown(key)

    def on_key_up(self, e):
        """
        Handles for key releases
        """

        if len(e.key) == 1:
            upper = e.shiftKey
            if e.getModifierState('CapsLock'):
                upper = not upper
            if upper:
                key = e.key.upper()
            else:
                key = e.key.lower()
        else:
            key = e.key
        
        try:
            self.keys_pressed.remove(e.key)
        except ValueError:
            pass

        self.room.keyUp(key)
