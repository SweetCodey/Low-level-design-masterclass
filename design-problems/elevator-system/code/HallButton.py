from Button import Button

class HallButton(Button):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    def get_direction(self):
        return self.direction

    def is_pressed(self):
        return self.pressed
