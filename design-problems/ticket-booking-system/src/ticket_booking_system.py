from datetime import datetime

from payment_manager import PaymentManager
from ticket_manager import TicketManager
from train_seat_type import TrainSeatType
from train_manager import TrainManager
from user_manager import UserManager
from seat_assignment_strategy import FirstAvailableSeatsStrategy

class TicketBookingSystem:
    def __init__(self):
        self.payment_manager = PaymentManager()
        self.train_manager = TrainManager()
        self.user_manager = UserManager()
        self.ticket_manager = TicketManager()
        self.seat_assignment_strategy = FirstAvailableSeatsStrategy()

    def add_user(self, name: str, email: str, phone: str):
        self.user_manager.add_user(name, email, phone)

    def add_train(self, train_id: int, train_name: str, schedule: dict[str: (int, datetime.time)], 
                  seats: dict[TrainSeatType: int]):
        self.train_manager.add_train(train_id, train_name, schedule, seats)

    # We are assuming all the trains run on all weekdays
    def search_trains(self, origin: str, destination: str):
        return self.train_manager.search_trains(origin, destination)

    def book_ticket(self, user_id: int, train_id: int, origin: str, destination: str, 
                    date_of_journey: datetime.date, required_seat_types: dict[TrainSeatType: int]):
        train = self.train_manager.get_train(train_id)
        available_seats = self.seat_assignment_strategy.find_available_seats(train, required_seat_types)
        if not available_seats:
            print("Seats are not available. Ticket booking failed.\n")
            return None
        price = self.calculate_price(train_id, origin, destination, required_seat_types)
        if self.payment_manager.process_payment(user_id, price):
            ticket = self.ticket_manager.book_ticket(user_id, train_id, origin, destination, 
                                                     date_of_journey, available_seats)
            print(f"Ticket booked successfully. Ticket ID: {ticket.ticket_id}\n")
            return ticket
        print("Payment failed. Ticket booking failed.\n")
        return None

    def calculate_price(self, train_id: int, origin: str, destination: str, required_seat_types: dict[TrainSeatType: int]):
        distance = self.train_manager.get_train(train_id).get_distance(origin, destination)
        total_price = 0

        for seat_type, quantity in required_seat_types.items():
            seat_price = seat_type.fixed_price + (seat_type.dynamic_price_per_km * distance)
            total_price += seat_price * quantity
        return total_price

    def get_tickets(self, user_id: str):
        return self.ticket_manager.get_tickets(user_id)

    def cancel_ticket(self, user_id: int, ticket_id: int):
        return self.ticket_manager.cancel_ticket(user_id, ticket_id)
