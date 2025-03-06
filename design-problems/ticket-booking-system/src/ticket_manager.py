from typing import List
from datetime import datetime
from collections import defaultdict

from train_manager import TrainSeat, TrainManager



class TicketManager:
    def __init__(self, train_manager: TrainManager):
        # {user_id: [Ticket1, Ticket2, ...]}
        self.tickets = defaultdict(list)
        self.ticket_counter = 1
        self.train_manager = train_manager

    def book_ticket(
        self,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: datetime.date,
        seats: List[TrainSeat],
    ):
        booking_success = self.train_manager.book_seats(seats)
        
        if not booking_success:
            print("Failed to book seats - invalid train or seats already booked\n")
            return None

        ticket = Ticket(
            self.ticket_counter,
            user_id,
            train_id,
            origin,
            destination,
            date_of_journey,
            seats,
        )
        self.tickets[user_id].append(ticket)
        self.ticket_counter += 1
        return ticket

    def get_tickets(self, user_id):
        return self.tickets.get(user_id)

    def cancel_ticket(self, user_id: int, ticket_id: int):
        tickets = self.tickets[user_id]
        ticket = next(
            (ticket for ticket in tickets if ticket.ticket_id == ticket_id), None
        )
        if ticket:
            if (ticket.date_of_journey - datetime.now().date()).days < 3:
                print("Cannot cancel the ticket. Not within 3 days of journey.\n")
                return False

            unbooking_success = self.train_manager.unbook_seats(ticket.seats)
            if unbooking_success:
                ticket.set_cancelled_status()
                print(f"Ticket ID: {ticket_id} has been canceled.\n")
                return True
            else:
                print(f"Failed to cancel ticket ID: {ticket_id}\n")
                return False
        return False


class Ticket:
    def __init__(
        self,
        ticket_id: int,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: datetime.date,
        seats: List[TrainSeat],
    ):
        self.ticket_id: int = ticket_id
        self.user_id: int = user_id
        self.train_id: int = train_id
        self.origin: str = origin
        self.destination: str = destination
        self.date_of_journey: datetime.date = date_of_journey
        self.seats: List[TrainSeat] = seats
        self.ticket_status: str = "CONFIRMED"

    def set_cancelled_status(self):
        """Set ticket status to cancelled without modifying seat state"""
        self.ticket_status = "CANCELLED"
