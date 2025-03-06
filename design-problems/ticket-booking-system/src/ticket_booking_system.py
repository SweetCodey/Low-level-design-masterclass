from datetime import datetime
from typing import Dict, List, Tuple, Optional

from payment_manager import PaymentManager
from ticket_manager import TicketManager, Ticket
from train_seat_type import TrainSeatType
from train_manager import TrainManager, Train
from user_manager import UserManager
from seat_assignment_strategy import FirstAvailableSeatsStrategy
from pricing_manager import PricingManager


class TicketBookingSystem:
    def __init__(self):
        self.payment_manager = PaymentManager()
        self.train_manager = TrainManager()
        self.user_manager = UserManager()
        self.ticket_manager = TicketManager(self.train_manager)
        self.seat_assignment_strategy = FirstAvailableSeatsStrategy()
        self.pricing_manager = PricingManager(self.train_manager)

    def add_user(self, name: str, email: str, phone: str) -> None:
        """
        Add a new user to the system.
        """
        self.user_manager.add_user(name, email, phone)

    def add_train(
        self,
        train_id: int,
        train_name: str,
        schedule: Dict[str, Tuple[int, datetime.time]],
        seats: Dict[TrainSeatType, int],
    ) -> None:
        """
        Add a new train to the system.
        """
        self.train_manager.add_train(train_id, train_name, schedule, seats)

    def search_trains(self, origin: str, destination: str) -> List[Train]:
        """
        Search for trains between origin and destination.
        """
        return self.train_manager.search_trains(origin, destination)

    def book_ticket(
        self,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: datetime.date,
        required_seat_types: Dict[TrainSeatType, int],
    ) -> Optional[Ticket]:
        """
        Book a ticket for a user.
        """
        train = self.train_manager.get_train(train_id)
        available_seats = self.seat_assignment_strategy.find_available_seats(
            train, required_seat_types
        )
        if not available_seats:
            print("Seats are not available. Ticket booking failed.\n")
            return None
        price = self.pricing_manager.calculate_price(
            train_id, origin, destination, required_seat_types
        )
        if self.payment_manager.process_payment(user_id, price):
            ticket = self.ticket_manager.book_ticket(
                user_id, train_id, origin, destination, date_of_journey, available_seats
            )
            print(f"Ticket booked successfully. Ticket ID: {ticket.ticket_id}\n")
            return ticket
        print("Payment failed. Ticket booking failed.\n")
        return None

    def get_tickets(self, user_id: int) -> Optional[List[Ticket]]:
        """
        Get all tickets for a user.
        """
        return self.ticket_manager.get_tickets(user_id)

    def cancel_ticket(self, user_id: int, ticket_id: int) -> bool:
        """
        Cancel a ticket for a user.
        """
        return self.ticket_manager.cancel_ticket(user_id, ticket_id)
