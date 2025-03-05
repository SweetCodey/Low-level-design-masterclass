from typing import Dict
from train_seat_type import TrainSeatType, StandardSeat, DeluxeSeat, ExecutiveSeat
from train_manager import TrainManager


class PricingManager:
    def __init__(self, train_manager: TrainManager = None):
        self.pricing_config: Dict[str, Dict[str, int]] = {}
        self.train_manager = train_manager

        # Set default prices
        self.set_pricing(StandardSeat(), 50, 0)
        self.set_pricing(DeluxeSeat(), 200, 2)
        self.set_pricing(ExecutiveSeat(), 500, 5)

    def set_pricing(
        self, seat_type: TrainSeatType, fixed_price: int, dynamic_price_per_km: int
    ) -> None:
        self.pricing_config[seat_type.get_class_name()] = {
            "fixed_price": fixed_price,
            "dynamic_price_per_km": dynamic_price_per_km,
        }

    def calculate_price(
        self,
        train_id: int,
        origin: str,
        destination: str,
        required_seat_types: Dict[TrainSeatType, int],
    ) -> int:
        """
        Calculate the total price for a journey based on train, route and seats.
        """
        distance = self.train_manager.get_train(train_id).get_distance(
            origin, destination
        )

        total_price = 0
        for seat_type, quantity in required_seat_types.items():
            class_name = seat_type.get_class_name()   
            pricing = self.pricing_config[class_name]

            seat_price = pricing["fixed_price"] + (
                pricing["dynamic_price_per_km"] * distance
            )
            total_price += seat_price * quantity

        return total_price
