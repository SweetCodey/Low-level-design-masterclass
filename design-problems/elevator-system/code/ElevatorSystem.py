from collections import deque
from Building import Building
from enums import Direction

class FloorRequest:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction

class ElevatorSystem:
    _instance = None

    def __init__(self, num_floors, num_cars, dispatch_strategy):
        if ElevatorSystem._instance is not None:
            raise Exception("ElevatorSystem is a Singleton. Use get_instance() instead.")
        self.building = Building(num_floors, num_cars)
        self.dispatch_strategy = dispatch_strategy
        self.hall_requests = deque()
        ElevatorSystem._instance = self

    @staticmethod
    def get_instance(num_floors=None, num_cars=None, dispatch_strategy=None):
        if ElevatorSystem._instance is None:
            ElevatorSystem(num_floors, num_cars, dispatch_strategy)
        return ElevatorSystem._instance

    def get_cars(self):
        return self.building.get_cars()

    def call_elevator(self, floor, direction):
        self.hall_requests.append(FloorRequest(floor, direction))
        print(f"  Hall button pressed on floor {floor} ({direction.name}). Request queued.")

    def dispatcher(self):
        print("  Dispatcher running...")
        while self.hall_requests:
            req = self.hall_requests.popleft()
            car = self.dispatch_strategy.select_car(
                self.building.get_cars(), req.floor
            )
            if car is None:
                print(f"  No available car for floor {req.floor}. Re-queuing request.")
                self.hall_requests.append(req)
                break
            print(f"  Dispatching Elevator {car.get_id()} to floor {req.floor}.")
            car.move(req.floor)
            # Car has arrived. Reset the hall button and open the door
            hall_panel = self.building.get_floors()[req.floor].get_panel()
            if req.direction == Direction.UP and hall_panel.get_up_button():
                hall_panel.get_up_button().reset()
                print(f"  Hall button (UP) on floor {req.floor} reset.")
            elif req.direction == Direction.DOWN and hall_panel.get_down_button():
                hall_panel.get_down_button().reset()
                print(f"  Hall button (DOWN) on floor {req.floor} reset.")
            car.get_door().open(car.get_id())

    def select_floor(self, car, floor):
        """Called when a passenger presses an ElevatorButton inside the car."""
        print(f"  Passenger in Elevator {car.get_id()} selected floor {floor}.")
        car.get_door().close(car.get_id())
        car.move(floor)
        car.get_door().open(car.get_id())
