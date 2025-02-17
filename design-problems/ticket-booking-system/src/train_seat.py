from train_seat_type import TrainSeatType

class TrainSeat:
    def __init__(self, seat_id: int, train_id: int, seat_type: TrainSeatType):
        self.seat_id = seat_id
        self.train_id = train_id
        self.seat_type = seat_type
        self.is_booked = False
