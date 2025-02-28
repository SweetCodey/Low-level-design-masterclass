from abc import ABC

class TrainSeatType(ABC):
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.fixed_price = 0
        self.dynamic_price_per_km = 0

    def get_class_name(self) -> str:
        return self.class_name
    
    def __eq__(self, other):
        if isinstance(other, TrainSeatType):
            return self.class_name == other.class_name
        return False
    
    def __hash__(self):
        return hash(self.class_name)

# Concrete Seat Types
class StandardSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Standard")
        self.fixed_price = 100
        self.dynamic_price_per_km = 1

class DeluxeSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Deluxe")
        self.fixed_price = 200
        self.dynamic_price_per_km = 2

class ExecutiveSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Executive")
        self.fixed_price = 500
        self.dynamic_price_per_km = 5
