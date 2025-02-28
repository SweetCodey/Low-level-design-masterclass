from abc import ABC, abstractmethod
from collections import defaultdict
from train_manager import Train
from train_seat_type import TrainSeatType

class SeatAssignmentStrategy(ABC):
    @abstractmethod
    def find_available_seats(self, train: Train, required_seat_types: dict[TrainSeatType: int]):
        pass

class FirstAvailableSeatsStrategy(SeatAssignmentStrategy):
    def find_available_seats(self, train: Train, required_seat_types: dict[TrainSeatType: int]):
        final_seats = defaultdict(list)
        for seat in train.seats:
            seat_type = seat.seat_type
            if seat_type in required_seat_types and not seat.is_booked() \
              and len(final_seats[seat_type]) < required_seat_types[seat_type]:
                final_seats[seat_type].append(seat)
        
        for seat_type, count in required_seat_types.items():
            if len(final_seats.get(seat_type, [])) != count:
                return []
        return [seat for seats in final_seats.values() for seat in seats]
