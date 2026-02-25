from enums import ElevatorState, Direction
from Door import Door
from Display import Display
from ElevatorPanel import ElevatorPanel

class ElevatorCar:
    MAX_LOAD = 680  # kg

    def __init__(self, car_id, num_floors):
        self.id = car_id
        self.current_floor = 0
        self.state = ElevatorState.IDLE
        self.door = Door()
        self.display = Display()
        self.panel = ElevatorPanel(num_floors)
        self.load = 0
        self.overloaded = False
        self.maintenance = False
        self.update_display()

    def get_id(self):
        return self.id

    def get_current_floor(self):
        return self.current_floor

    def get_state(self):
        return self.state

    def get_door(self):
        return self.door

    def get_display(self):
        return self.display

    def is_in_maintenance(self):
        return self.maintenance

    def is_overloaded(self):
        return self.overloaded

    def move(self, target):
        if self.maintenance:
            print(f"  Elevator {self.id}: In MAINTENANCE. Ignoring move request to floor {target}.")
            return
        if self.overloaded:
            print(f"  Elevator {self.id}: OVERLOADED. Refusing to move to floor {target}.")
            return

        if target == self.current_floor:
            print(f"  Elevator {self.id}: Already at floor {target}.")
            self.state = ElevatorState.IDLE
            self.update_display()
            return

        direction_str = "UP" if target > self.current_floor else "DOWN"
        print(f"  Elevator {self.id}: Moving {direction_str} from floor {self.current_floor} to floor {target}.")
        self.state = ElevatorState.UP if target > self.current_floor else ElevatorState.DOWN

        while self.current_floor != target:
            self.current_floor += 1 if self.state == ElevatorState.UP else -1
            self.update_display()
            self.display.show(self.id)

        print(f"  Elevator {self.id}: Arrived at floor {target}.")
        self.state = ElevatorState.IDLE
        self.update_display()

    def update_display(self):
        if self.state == ElevatorState.UP:
            direction = Direction.UP
        elif self.state == ElevatorState.DOWN:
            direction = Direction.DOWN
        else:
            direction = Direction.IDLE
        self.display.update(self.current_floor, direction, self.state)

    def enter_maintenance(self):
        self.maintenance = True
        self.state = ElevatorState.MAINTENANCE
        self.door.close(self.id)
        self.update_display()
        print(f"  Elevator {self.id}: Entered MAINTENANCE mode.")

    def exit_maintenance(self):
        self.maintenance = False
        self.state = ElevatorState.IDLE
        self.update_display()
        print(f"  Elevator {self.id}: Exited MAINTENANCE mode. Now IDLE.")

    def add_load(self, kg):
        self.load += kg
        if self.load > ElevatorCar.MAX_LOAD:
            self.overloaded = True
            print(f"  ALARM: Elevator {self.id} is overloaded! Current load: {self.load} kg (max: {ElevatorCar.MAX_LOAD} kg). Elevator will not move.")

    def remove_load(self, kg):
        self.load -= kg
        if self.load <= ElevatorCar.MAX_LOAD:
            self.overloaded = False
            print(f"  Elevator {self.id}: Overload cleared. Current load: {self.load} kg.")

    def emergency_stop(self):
        self.state = ElevatorState.IDLE
        self.door.close(self.id)
        self.update_display()
        print(f"  EMERGENCY: Elevator {self.id} stopped. Doors closed. Alert sent.")
