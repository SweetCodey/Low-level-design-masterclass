from HallButton import HallButton
from enums import Direction

class HallPanel:
    def __init__(self, floor_number, top_floor):
        self.up = None if floor_number == top_floor else HallButton(Direction.UP)
        self.down = None if floor_number == 0 else HallButton(Direction.DOWN)

    def get_up_button(self):
        return self.up

    def get_down_button(self):
        return self.down
