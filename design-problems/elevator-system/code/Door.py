from enums import DoorState

class Door:
    def __init__(self):
        self.state = DoorState.CLOSED

    def open(self, car_id=None):
        self.state = DoorState.OPEN
        label = f"Elevator {car_id}" if car_id is not None else "Door"
        print(f"  {label}: Door opened.")

    def close(self, car_id=None):
        self.state = DoorState.CLOSED
        label = f"Elevator {car_id}" if car_id is not None else "Door"
        print(f"  {label}: Door closed.")

    def is_open(self):
        return self.state == DoorState.OPEN
