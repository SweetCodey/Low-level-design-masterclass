from Floor import Floor
from ElevatorCar import ElevatorCar

class Building:
    def __init__(self, num_floors, num_cars):
        top_floor = num_floors - 1
        self.floors = [Floor(i, top_floor) for i in range(num_floors)]
        self.cars = [ElevatorCar(i, num_floors) for i in range(num_cars)]

    def get_floors(self):
        return self.floors

    def get_cars(self):
        return self.cars
