from ParkingLotSystem import ParkingLotSystem
from Vehicle import Vehicle


class EntranceGate:
    def __init__(self, system: ParkingLotSystem):
        self.system = system

    def enter(self, vehicle: Vehicle):
        return self.system.handle_entry(vehicle)
