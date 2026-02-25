from enums import VehicleType


class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: VehicleType):
        self.id = spot_id
        self.type = spot_type
        self.is_free = True

    def available(self) -> bool:
        return self.is_free

    def get_type(self) -> VehicleType:
        return self.type

    def mark_occupied(self):
        self.is_free = False

    def release(self):
        self.is_free = True

    def get_id(self) -> int:
        return self.id
