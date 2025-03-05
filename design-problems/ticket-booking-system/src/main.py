from datetime import datetime
from train_seat_type import StandardSeat, DeluxeSeat
from ticket_booking_system import TicketBookingSystem

# Initialize Ticket Booking System
ticket_booking_system = TicketBookingSystem()

# Create Users
ticket_booking_system.add_user("Aman", "aman@example.com", "1234567890")

# Create Trains
ticket_booking_system.add_train(
    1,
    "Rajdhani Express",
    {
        "Delhi": (0, datetime.strptime("08:00", "%H:%M").time()),
        "Mumbai": (1440, datetime.strptime("20:00", "%H:%M").time()),
    },
    {StandardSeat(): 5, DeluxeSeat(): 3},
)

ticket_booking_system.add_train(
    2,
    "Maharaja Express",
    {
        "Delhi": (0, datetime.strptime("12:00", "%H:%M").time()),
        "Jaipur": (300, datetime.strptime("16:00", "%H:%M").time()),
    },
    {StandardSeat(): 5, DeluxeSeat(): 3},
)

# Search for Trains
print("Searching for trains from Delhi to Mumbai:")
available_trains = ticket_booking_system.search_trains("Delhi", "Mumbai")
for train in available_trains:
    print(f"Train ID: {train.train_id}, Train Name: {train.train_name}\n")

print("---------")

# Book a Ticket
if available_trains:
    selected_train = available_trains[0]  # Select the first available train
    seats_to_book = {StandardSeat(): 1, DeluxeSeat(): 1}
    print(f"Trying to book ticket for Train ID: {selected_train.train_id}")
    ticket1 = ticket_booking_system.book_ticket(
        1,
        selected_train.train_id,
        "Delhi",
        "Mumbai",
        datetime.strptime("2025-03-05", "%Y-%m-%d").date(),
        seats_to_book,
    )
    if ticket1:
        print(
            f"Ticket ID: {ticket1.ticket_id}, Train ID: {ticket1.train_id}\n"
            + f"Origin: {ticket1.origin}, Destination: {ticket1.destination}\n"
            + f"Date of Journey: {ticket1.date_of_journey}\n"
            + f"Status: {ticket1.ticket_status}, Seats:\n"
        )
        for seat in ticket1.seats:
            print(f"Seat ID: {seat.seat_id}, Seat Type: {seat.seat_type.class_name}")

print("---------")

# Get Tickets for a User
tickets = ticket_booking_system.get_tickets(1)
if tickets:
    print("\nTickets for User ID: 1")
    for ticket in tickets:
        print(
            f"Ticket ID: {ticket.ticket_id}, Train ID: {ticket.train_id}\n"
            + f"Origin: {ticket.origin}, Destination: {ticket.destination}\n"
            + f"Date of Journey: {ticket.date_of_journey}\n"
            + f"Status: {ticket.ticket_status}, Seats:\n"
        )
        for seat in ticket.seats:
            print(f"Seat ID: {seat.seat_id}, Seat Type: {seat.seat_type.class_name}")
        print("\n")

print("---------")
# Cancel a Ticket
ticket_cancel_status = ticket_booking_system.cancel_ticket(1, 1)
print("---------")

# Verify tickets for a user after canceling a ticket
tickets = ticket_booking_system.get_tickets(1)
if tickets:
    print("\nTickets for User ID: 1")
    for ticket in tickets:
        print(
            f"Ticket ID: {ticket.ticket_id}, Train ID: {ticket.train_id}\n"
            + f"Origin: {ticket.origin}, Destination: {ticket.destination}\n"
            + f"Date of Journey: {ticket.date_of_journey}\n"
            + f"Status: {ticket.ticket_status}\n"
        )
