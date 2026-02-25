import time

from Vehicle import Vehicle
from ParkingSpot import ParkingSpot


class ParkingTicket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()

    def get_vehicle(self) -> Vehicle:
        return self.vehicle

    def get_spot(self) -> ParkingSpot:
        return self.spot

    def get_entry_time(self) -> float:
        return self.entry_time
