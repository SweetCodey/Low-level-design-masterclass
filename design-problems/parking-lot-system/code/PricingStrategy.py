from abc import ABC, abstractmethod

from enums import VehicleType


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, entry_time: float, exit_time: float, vehicle_type: VehicleType) -> int:
        pass
