from Button import Button

class ElevatorButton(Button):
    def __init__(self, floor):
        super().__init__()
        self.destination_floor = floor

    def get_destination_floor(self):
        return self.destination_floor

    def is_pressed(self):
        return self.pressed
