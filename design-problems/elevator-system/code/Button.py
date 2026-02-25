class Button:
    def __init__(self):
        self.pressed = False

    def press_down(self):
        self.pressed = True

    def reset(self):
        self.pressed = False

    def is_pressed(self):
        raise NotImplementedError("Must be implemented by subclasses")
