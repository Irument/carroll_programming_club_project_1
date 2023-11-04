# Adding a room
To add a room to the GUI, It needs to be mentioned in a few places.
- /static/pyscript/rooms/someRoomName.py: A Python file with a `render` function needs to be created. The filename should be the room name. This render function should contain the code ran when the room needs to be rendered. This render function should have 3 parameters: `gui`, `canvas`, `persistant`. The `gui` parameter is an object that manages the rooms. Look at [gui.py](/static/pyscript/gui.py) for more info. The `canvas` parameter is an object used for modifying the canvas. You can modify the canvas yourself by using the `canvas.ctx` function to get the context, or just getting the DOM element for the canvas by `canvas.canvas`. I have created some functions for modifying the canvas without using the normal canvas API. You can find the functions [here](/static/pyscript/canvas.py). The `persistant` parameter is a blank object that is used for putting variables that need to persist after being rendered again. This data does not persist beyond a reload.
- [home.html](/templates/home.html): The py-env element needs to be modified. In the same way the other paths are mentioned, you need to add the Python file that was created before.
- [gui.py](/static/pyscript/gui.py): In the `__init__` function of the GUI class, there is a rooms array that needs to be modified to add a room.

# Adding an image
To add an image to use, it needs to be added to the [/static/img](/static/img) directory. Then, it can be called by this link: /static/img/yourFilename.png

# Switching rooms in render function
To switch the room in the render function, you need to use the `gui` object. You can learn more about the different parameters in the [Adding a room](#adding-a-room) section. You would probably want to put this in some kind of callback. Just running this code in the render function will make the room to switch as soon as it is loaded.

```py
gui.room = 'yourRoom'
gui.render_current_room()
```
