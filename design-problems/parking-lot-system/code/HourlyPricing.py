from PricingStrategy import PricingStrategy
from enums import VehicleType


class HourlyPricing(PricingStrategy):
    def __init__(self, rates: dict):
        self.rates = rates  # {VehicleType.BIKE: 20, VehicleType.CAR: 50, ...}

    def calculate_fee(self, entry_time: float, exit_time: float, vehicle_type: VehicleType) -> int:
        hours = int((exit_time - entry_time) / 3600)
        if hours < 1:
            hours = 1
        return hours * self.rates[vehicle_type]
