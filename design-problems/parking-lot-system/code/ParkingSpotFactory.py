from enums import VehicleType


class ParkingSpotFactory:
    @staticmethod
    def get_spot_type(vehicle_type: VehicleType) -> VehicleType:
        # Since we use a single enum, the mapping is direct.
        # Bike -> BIKE spot (Compact), Car -> CAR spot (Regular), Truck -> TRUCK spot (Large)
        return vehicle_type
