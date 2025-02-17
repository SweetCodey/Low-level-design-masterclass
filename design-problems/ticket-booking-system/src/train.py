from typing import List
from train_seat import TrainSeat

class Train:
    def __init__(self, train_id: int, train_name: str, origin: str, destination: str, departure_time: str, arrival_time: str):
        self.train_id = train_id
        self.train_name = train_name
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats: List[TrainSeat] = []
