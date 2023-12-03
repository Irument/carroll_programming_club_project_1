# Adding a room
To add a room to the GUI, It needs to be mentioned in a few places.
- /static/pyscript/rooms/someRoomName.py: A Python file with a `Room` class needs to be created. The filename should be the room name. Look off the previous rooms for how to make this python file. The rooms inherit `rooms.BaseRoom`. This has every function that is used by the gui object, as well as notes on what every function does. The notes also explain what the gui/canvas objects are.
- [home.html](/templates/home.html): The py-env element needs to be modified. In the same way the other paths are mentioned, you need to add the Python file that was created before.
- [gui.py](/static/pyscript/gui.py): In the `__init__` function of the GUI class, there is a rooms array that needs to be modified to add a room.

# Adding an image
To add an image to use, it needs to be added to the [/static/img](/static/img) directory. Then, it can be called by this link: /static/img/yourFilename.png

# Using an image
To use an image in a room, you have to run the function self.canvas.prepare_image for each image you are going to use that image. The function has 2 parameters, id and link. The id would be a name for the image, that you would use in a function like add_image or add_button to specify the image, and the link would just be the link. Then on the end of the render function, run self.canvas.loadImages().

# Switching rooms in render function
To switch the room in the render function, you need to use the `gui` object. You can learn more about the different parameters in the [Adding a room](#adding-a-room) section. You would probably want to put this in some kind of callback. Just running this code in the render function will make the room switch as soon as it is loaded.

```py
self.gui.room = 'yourRoom'
self.gui.render_current_room()
```

# Handling key presses in a room
The keyDown function is called when a key is pressed, and the keyUp function is called when a key is released. The function has one parameter called `key`, that is the printable form of the key that was pressed. You can test around with keys that are not printable like enter or shift, but keys like letters will just show that letter.

# print function
Instead of using `print`, import console from js, and use Javascript's logging tools. print works, however it is mixed with pyodide's stuff and is not really good.

# Sharing data between rooms
The room object has access to a blank object that is shared between all rooms. Use this for storing any variables that other rooms need access to.
```py
self.gui.shared
```

# Creating a quiz
Run the create_quiz.py file, and it will guide you through making a quiz, and add it to the DB. The server does not have to be restarted and the client does not have to be reloaded to use a new quiz.

# Deleting a quiz
Run the delete_quiz.py file with the first argument being the quiz id.
