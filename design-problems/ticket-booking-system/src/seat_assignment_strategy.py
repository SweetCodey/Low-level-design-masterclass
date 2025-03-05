from abc import ABC, abstractmethod
from collections import defaultdict
from train_manager import Train
from train_seat_type import TrainSeatType


class SeatAssignmentStrategy(ABC):
    """
    Abstract base class defining the interface for seat assignment strategies.
    Different implementations can provide various algorithms for seat selection.
    """
    @abstractmethod
    def find_available_seats(
        self, train: Train, required_seat_types: dict[TrainSeatType:int]
    ):
        """
        Abstract method to find available seats based on requirements.
        """
        pass


class FirstAvailableSeatsStrategy(SeatAssignmentStrategy):
    """
    Concrete strategy that assigns the first available seats matching the required types.
    This is a greedy approach that selects seats in order of availability.
    """
    def find_available_seats(
        self, train: Train, required_seat_types: dict[TrainSeatType:int]
    ):
        # Use defaultdict to collect seats by type
        final_seats = defaultdict(list)
        
        # Iterate through all seats in the train
        for seat in train.seats:
            seat_type = seat.seat_type
            # Check if this seat type is required, seat is available, and we still need more of this type
            if (
                seat_type in required_seat_types
                and not seat.is_booked()
                and len(final_seats[seat_type]) < required_seat_types[seat_type]
            ):
                final_seats[seat_type].append(seat)

        # Verify that all requirements are met
        for seat_type, count in required_seat_types.items():
            if len(final_seats.get(seat_type, [])) != count:
                # If any seat type requirement is not met, return empty list (booking cannot be fulfilled)
                return []
                
        # Flatten the dictionary of lists into a single list of seats and return
        return [seat for seats in final_seats.values() for seat in seats]
