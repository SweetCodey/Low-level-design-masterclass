from typing import Dict, List, Optional, Tuple
from datetime import datetime, time, date, timedelta
from collections import defaultdict

class User:
    def __init__(self, user_id: int, name: str, email: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone

class UserManager:
    def __init__(self):
        # {user_id: User}
        self.users = {}
        self.user_counter = 1

    def add_user(self, name: str, email: str, phone: str) -> None:
        user = User(self.user_counter, name, email, phone)
        self.users[self.user_counter] = user
        self.user_counter += 1
        print(f"User {name} has been added successfully. User ID: {user.user_id}\n")
        
class TrainSeat:
    def __init__(self, seat_id: int, train_id: int):
        self.seat_id = seat_id
        self.train_id = train_id
        self.__is_booked = False

    def book(self):
        self.__is_booked = True

    def unbook(self):
        self.__is_booked = False

    def is_booked(self):
        return self.__is_booked


class Train:
    def __init__(
        self,
        train_id: int,
        train_name: str,
        schedule: dict[str: (int, time)],
        seats: List[TrainSeat],
    ):
        self.train_id: int = train_id
        self.train_name: str = train_name
        self.schedule: Dict[str, (int, time)] = schedule
        self.origin: str = list(schedule.keys())[0]
        self.destination: str = list(schedule.keys())[-1]
        self.seats: List[TrainSeat] = seats

    def find_available_seats(self, seats_required: int) -> List[TrainSeat]:
        available_seats = []
        for seat in self.seats:
            if not seat.is_booked():
                available_seats.append(seat)
            if len(available_seats) == seats_required:
                return available_seats
        return None

    def get_distance(self, origin: str, destination: str):
        return self.schedule[destination][0] - self.schedule[origin][0]


class TrainManager:
    def __init__(self):
        self.trains: dict[int, Train] = {}

    def add_train(
        self,
        train_id: int,
        train_name: str,
        schedule: dict[str, (int, time)],
        total_seats: int,
    ):
        seats = [TrainSeat(i, train_id) for i in range(1, total_seats + 1)]
        train = Train(train_id, train_name, schedule, seats)
        self.trains[train_id] = train
        print(f"Train {train_name} with ID {train_id} has been added successfully.\n")

    def search_trains(self, origin: str, destination: str) -> List[Train]:
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
        for seat in seats:
            if seat.is_booked():
                return False
        for seat in seats:
            seat.book()
        return True

    def unbook_seats(self, seats: List[TrainSeat]) -> bool:
        for seat in seats:
            seat.unbook()
        return True

    def find_available_seats(self, train_id: int, seats_required: int) -> List[TrainSeat]:
        return self.trains[train_id].find_available_seats(seats_required)

    def get_train(self, train_id: int) -> Train:
        return self.trains.get(train_id)
    
class Ticket:
    def __init__(
        self,
        ticket_id: int,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: date,
        seats: List[TrainSeat],
    ):
        self.ticket_id: int = ticket_id
        self.user_id: int = user_id
        self.train_id: int = train_id
        self.origin: str = origin
        self.destination: str = destination
        self.date_of_journey: date = date_of_journey
        self.seats: List[TrainSeat] = seats
        self.ticket_status: str = "CONFIRMED"

    def set_cancelled_status(self):
        self.ticket_status = "CANCELLED"


class TicketManager:
    def __init__(self, train_manager: TrainManager):
        self.tickets = defaultdict(list)
        self.ticket_counter = 1
        self.train_manager = train_manager

    def book_ticket(
        self,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: date,
        seats: List[TrainSeat],
    ):
        booking_success = self.train_manager.book_seats(seats)
        if not booking_success:
            print("Failed to book seats - Seats already booked\n")
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

    def get_tickets(self, user_id: int):
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
        
class PaymentManager:
    def process_payment(self, user_id: int, amount: float) -> bool:
        print(f"Payment of {amount} processed for user {user_id}")
        return True

class PricingManager:
    def __init__(self, train_manager: TrainManager):
        self.train_manager = train_manager
        self.fixed_price = 100
        self.dynamic_price_per_km = 1

    def calculate_price(
        self,
        train_id: int,
        origin: str,
        destination: str,
        required_seats: int,
    ) -> int:
        distance = self.train_manager.get_train(train_id).get_distance(
            origin, destination
        )
        total_price_per_seat = self.fixed_price + (self.dynamic_price_per_km * distance)
        return total_price_per_seat * required_seats
        
class TicketBookingSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.train_manager = TrainManager()
        self.payment_manager = PaymentManager()
        self.pricing_manager = PricingManager(self.train_manager)
        self.ticket_manager = TicketManager(self.train_manager)

    def add_user(self, name: str, email: str, phone: str) -> None:
        self.user_manager.add_user(name, email, phone)

    def add_train(
        self,
        train_id: int,
        train_name: str,
        schedule: dict[str, Tuple[int, datetime.time]],
        total_seats: int,
    ) -> None:
        self.train_manager.add_train(train_id, train_name, schedule, total_seats)

    def search_trains(self, origin: str, destination: str) -> List[Train]:
        return self.train_manager.search_trains(origin, destination)

    def book_ticket(
        self,
        user_id: int,
        train_id: int,
        origin: str,
        destination: str,
        date_of_journey: date,
        seats_required: int,
    ) -> Optional[Ticket]:
        final_seats = self.train_manager.find_available_seats(train_id, seats_required)
        if not final_seats:
            print("Seats are not available. Ticket booking failed.\n")
            return None

        price = self.pricing_manager.calculate_price(
            train_id, origin, destination, seats_required
        )

        if self.payment_manager.process_payment(user_id, price):
            ticket = self.ticket_manager.book_ticket(
                user_id, train_id, origin, destination, date_of_journey, final_seats
            )
            print(f"Ticket booked successfully. Ticket ID: {ticket.ticket_id}\n")
            return ticket

        print("Payment failed. Ticket booking failed.\n")
        return None

    def get_tickets(self, user_id: int) -> Optional[List[Ticket]]:
        return self.ticket_manager.get_tickets(user_id)

    def cancel_ticket(self, user_id: int, ticket_id: int) -> bool:
        return self.ticket_manager.cancel_ticket(user_id, ticket_id)
    
def main():
    # Create the ticket booking system
    booking_system = TicketBookingSystem()
    
    # Add users
    booking_system.add_user("Alice", "alice@example.com", "1234567890")
    booking_system.add_user("Bob", "bob@example.com", "0987654321")
    
    # Add trains with schedules
    # Schedule format: {location: (distance_from_origin, arrival_time)}
    train1_schedule = {
        "New York": (0, time(hour=6, minute=0)),
        "Philadelphia": (150, time(hour=7, minute=30)),
        "Washington DC": (350, time(hour=9, minute=0))
    }
    
    train2_schedule = {
        "Boston": (0, time(hour=8, minute=0)),
        "New York": (220, time(hour=10, minute=30)),
        "Philadelphia": (370, time(hour=12, minute=0)),
        "Washington DC": (570, time(hour=14, minute=0))
    }
    
    booking_system.add_train(101, "Express Northeast", train1_schedule, 50)
    booking_system.add_train(102, "Regional Express", train2_schedule, 100)
    
    # Search for trains
    print("Searching for trains from New York to Washington DC:")
    trains = booking_system.search_trains("New York", "Washington DC")
    for train in trains:
        print(f"Found train: {train.train_name} (ID: {train.train_id})")
    
    # Book tickets
    journey_date = date.today() + timedelta(days=10)
    ticket1 = booking_system.book_ticket(
        user_id=1, 
        train_id=101, 
        origin="New York", 
        destination="Washington DC", 
        date_of_journey=journey_date, 
        seats_required=2
    )
    
    # View bookings
    print("\nViewing tickets for user 1:")
    user_tickets = booking_system.get_tickets(1)
    if user_tickets:
        for ticket in user_tickets:
            print(f"Ticket ID: {ticket.ticket_id}, Train: {ticket.train_id}, " 
                  f"From: {ticket.origin}, To: {ticket.destination}, "
                  f"Date: {ticket.date_of_journey}, Status: {ticket.ticket_status}")
    
    # Cancel a ticket
    print("\nCancelling ticket:")
    if ticket1:
        booking_system.cancel_ticket(1, ticket1.ticket_id)
        
        # View bookings again
        print("\nViewing tickets for user 1 after cancellation:")
        user_tickets = booking_system.get_tickets(1)
        if user_tickets:
            for ticket in user_tickets:
                print(f"Ticket ID: {ticket.ticket_id}, Train: {ticket.train_id}, "
                      f"From: {ticket.origin}, To: {ticket.destination}, "
                      f"Date: {ticket.date_of_journey}, Status: {ticket.ticket_status}")

if __name__ == "__main__":
    main()