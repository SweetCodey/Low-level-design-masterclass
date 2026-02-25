from enums import Direction, ElevatorState

class Display:
    def __init__(self):
        self.floor = 0
        self.direction = Direction.IDLE
        self.state = ElevatorState.IDLE

    def update(self, floor, direction, state):
        self.floor = floor
        self.direction = direction
        self.state = state

    def show(self, car_id):
        print(f"    Elevator {car_id} | Floor: {self.floor} | Direction: {self.direction.name} | State: {self.state.name}")
