from ElevatorButton import ElevatorButton
from DoorButton import DoorButton
from EmergencyButton import EmergencyButton

class ElevatorPanel:
    def __init__(self, num_floors):
        self.floor_buttons = [ElevatorButton(i) for i in range(num_floors)]
        self.open_button = DoorButton()
        self.close_button = DoorButton()
        self.emergency_button = EmergencyButton()
