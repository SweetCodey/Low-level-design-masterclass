from abc import ABC, abstractmethod
from enums import ElevatorState

class DispatchStrategy(ABC):
    @abstractmethod
    def select_car(self, cars, floor):
        pass

class NearestIdleStrategy(DispatchStrategy):
    def select_car(self, cars, floor):
        best = None
        min_dist = float('inf')
        for car in cars:
            if (car.get_state() == ElevatorState.IDLE
                and not car.is_in_maintenance()
                and not car.is_overloaded()):
                dist = abs(car.get_current_floor() - floor)
                if dist < min_dist:
                    min_dist = dist
                    best = car
        return best
