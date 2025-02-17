from user import User
from train import Train
from train_seat import TrainSeat
from ticket import Ticket
from payment import Payment
from train_seat_type import StandardSeat, DeluxeSeat, ExecutiveSeat
from ticket_status import BookedStatus, CanceledStatus, WaitlistedStatus
from payment_status import SuccessPayment, FailedPayment, InProgressPayment

# Create Users
user1 = User(1, "Aman", "aman@example.com", "1234567890")

# Create a Train
train1 = Train(101, "Express 101", "Delhi", "Mumbai", "08:00 AM", "10:00 PM")

# Create Train Seats
seat1 = TrainSeat(1, train1.train_id, StandardSeat())
seat2 = TrainSeat(2, train1.train_id, DeluxeSeat())
train1.seats.append(seat1)
train1.seats.append(seat2)

# Book a Ticket
ticket1 = Ticket(1001, user1.user_id, train1.train_id, [seat1, seat2])
ticket1.status.append(BookedStatus())  # Mark seats as booked
user1.tickets.append(ticket1)

# Process Payment
payment1 = Payment(5001, ticket1.ticket_id, 250.0, "Credit Card", SuccessPayment())

# Output
print(f"User: {user1.name} booked Ticket ID: {ticket1.ticket_id} on Train {train1.train_name}")
print(f"Seats: {[seat.seat_type.get_class_name() for seat in ticket1.seats]}")
print(f"Ticket Status: {[status.get_status() for status in ticket1.status]}")
print(f"Payment Status: {payment1.payment_status.get_status()}")
