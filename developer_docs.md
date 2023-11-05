# Adding a room
To add a room to the GUI, It needs to be mentioned in a few places.
- /static/pyscript/rooms/someRoomName.py: A Python file with a `Room` class needs to be created. The filename should be the room name. Look off the previous rooms for how to make this python file. The rooms inherit `rooms.BaseRoom`. This has every function that is used by the gui object, as well as notes on what every function does. The notes also explain what the gui/canvas objects are.
- [home.html](/templates/home.html): The py-env element needs to be modified. In the same way the other paths are mentioned, you need to add the Python file that was created before.
- [gui.py](/static/pyscript/gui.py): In the `__init__` function of the GUI class, there is a rooms array that needs to be modified to add a room.

# Adding an image
To add an image to use, it needs to be added to the [/static/img](/static/img) directory. Then, it can be called by this link: /static/img/yourFilename.png

# Switching rooms in render function
To switch the room in the render function, you need to use the `gui` object. You can learn more about the different parameters in the [Adding a room](#adding-a-room) section. You would probably want to put this in some kind of callback. Just running this code in the render function will make the room switch as soon as it is loaded.

```py
self.gui.room = 'yourRoom'
self.gui.render_current_room()
```

# Handling key presses in a room
The keyDown function is called when a key is pressed, and the keyUp function is called when a key is released. The keyCode parameter for both functions is the ASCII code for the key pressed. There is a function to convert these key codes to characters. The function `keyCodeToChar` is defined in the [gui class](/static/pyscript/gui.py). If the character is non-printable, you can still catch for it by using an if statement. You can find the key code for a non-printable character [here](https://www.ascii-code.com/). The first column would be the key code. Characters always show up in uppercase even if caps lock is on or shift is pressed/not pressed. Detecting this is not really a big deal however. This will probably be fixed later. This is also the case when using shift to use special characters.

# print function
Instead of using `print`, import console from js, and use Javascript's logging tools. print works, however it is mixed with pyodide's stuff and is not really good.