from enums import VehicleType


class Vehicle:
    def __init__(self, number: str, vehicle_type: VehicleType):
        self.number = number
        self.type = vehicle_type

    def get_number(self) -> str:
        return self.number

    def get_type(self) -> VehicleType:
        return self.type
