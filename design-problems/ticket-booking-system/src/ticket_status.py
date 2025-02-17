class TicketStatus:
    def __init__(self, status_name: str):
        self.status_name = status_name

    def get_status(self) -> str:
        return self.status_name

# Concrete Ticket Statuses
class BookedStatus(TicketStatus):
    def __init__(self):
        super().__init__("Booked")

class CanceledStatus(TicketStatus):
    def __init__(self):
        super().__init__("Canceled")

class WaitlistedStatus(TicketStatus):
    def __init__(self):
        super().__init__("Waitlisted")
