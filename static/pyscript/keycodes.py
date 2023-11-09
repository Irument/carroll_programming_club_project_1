def translate_keycode(keycode):
    """
    Translates a keycode to printable.
    If it is non-printable, return None
    """

    if 65 <= keycode <= 90: # Uppercase range. All keycodes that are letters will be uppercase
        if check_caps():
            return keycode
        else:
            return keycode+32 # Adding 32 makes it lowercase range
