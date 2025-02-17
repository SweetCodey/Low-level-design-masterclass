class TrainSeatType:
    def __init__(self, class_name: str):
        self.class_name = class_name

    def get_class_name(self) -> str:
        return self.class_name

# Concrete Seat Types
class StandardSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Standard")

class DeluxeSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Deluxe")

class ExecutiveSeat(TrainSeatType):
    def __init__(self):
        super().__init__("Executive")
