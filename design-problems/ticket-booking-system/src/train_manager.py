from typing import List
from datetime import datetime

from train_seat_type import TrainSeatType

class TrainSeat:
    def __init__(self, seat_id: int, train_id: int, seat_type: TrainSeatType):
        self.seat_id = seat_id
        self.train_id = train_id
        self.seat_type = seat_type
        self.__is_booked = False

    def book(self):
        self.__is_booked = True

    def unbook(self):
        self.__is_booked = False

    def is_booked(self):
        return self.__is_booked

class TrainManager:
    def __init__(self):
        self.trains: dict[int:Train] = {}

    def add_train(
        self,
        train_id: int,
        train_name: str,
        schedule: dict[str : (int, datetime.time)],
        seats: dict[TrainSeatType:int],
    ):
        train = Train(train_id, train_name, schedule, seats)
        self.trains[train_id] = train
        print(f"Train {train_name} with ID {train_id} has been added successfully.\n")

    def get_train(self, train_id: int):
        return self.trains.get(train_id)

    def search_trains(self, origin: str, destination: str):
        trains = []
        for train in self.trains.values():
            if (
                origin in train.schedule
                and destination in train.schedule
                and train.schedule[origin][0] < train.schedule[destination][0]
            ):
                trains.append(train)
        return trains

    def book_seats(self, seats: List[TrainSeat]) -> bool:
        """
        Books the provided seats if available
        """ 
        for seat in seats:
            if seat.is_booked():
                return False
            seat.book()
        return True
        
    def unbook_seats(self, seats: List[TrainSeat]) -> bool:
        """
        Unbooks the provided seats
        """
        for seat in seats:
            seat.unbook()
        return True


# For simplicity we assume all the trains run on all weekdays
class Train:
    def __init__(
        self,
        train_id: int,
        train_name: str,
        schedule: dict[str : (int, datetime.time)],
        seats: dict[TrainSeatType:int],
    ):
        self.train_id: int = train_id
        self.train_name: int = train_name
        # schedule: {location: (distance, time)}
        self.schedule: dict[str : (int, datetime.time)] = schedule
        self.origin: str = list(schedule.keys())[0]
        self.destination: str = list(schedule.keys())[-1]
        self.seats: List[TrainSeat] = self.add_seats(seats)

    def add_seats(self, seats: dict[TrainSeatType:int]):
        train_seats = []
        for seat_type, count in seats.items():
            for i in range(count):
                train_seats.append(
                    TrainSeat(len(train_seats) + 1, self.train_id, seat_type)
                )
        return train_seats

    def get_distance(self, origin: str, destination: str):
        return self.schedule[destination][0] - self.schedule[origin][0]
