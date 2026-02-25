from ParkingLotSystem import ParkingLotSystem
from ParkingTicket import ParkingTicket


class ExitGate:
    def __init__(self, system: ParkingLotSystem):
        self.system = system

    def exit(self, ticket: ParkingTicket):
        self.system.handle_exit(ticket)
