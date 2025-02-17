from typing import List
from ticket_status import TicketStatus
from train_seat import TrainSeat

class Ticket:
    def __init__(self, ticket_id: int, user_id: int, train_id: int, seats: List[TrainSeat]):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.train_id = train_id
        self.seats = seats
        self.status: List[TicketStatus] = []  # List of TicketStatus for each seat
