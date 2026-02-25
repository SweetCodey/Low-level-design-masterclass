import time

from PricingStrategy import PricingStrategy
from PaymentStrategy import PaymentStrategy
from ParkingSpot import ParkingSpot
from ParkingSpotFactory import ParkingSpotFactory
from ParkingTicket import ParkingTicket
from Vehicle import Vehicle


class ParkingLotSystem:
    _instance = None

    def __init__(self, pricing_service: PricingStrategy, payment_service: PaymentStrategy):
        if ParkingLotSystem._instance is not None:
            raise Exception("ParkingLotSystem is a Singleton. Use get_instance() instead.")
        self.spots = []
        self.pricing_service = pricing_service
        self.payment_service = payment_service
        ParkingLotSystem._instance = self

    @staticmethod
    def get_instance(pricing_service=None, payment_service=None):
        if ParkingLotSystem._instance is None:
            ParkingLotSystem(pricing_service, payment_service)
        return ParkingLotSystem._instance

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def handle_entry(self, vehicle: Vehicle):
        required_type = ParkingSpotFactory.get_spot_type(vehicle.get_type())

        for spot in self.spots:
            if spot.available() and spot.get_type() == required_type:
                spot.mark_occupied()
                return ParkingTicket(vehicle, spot)

        return None  # no matching spot available

    def handle_exit(self, ticket: ParkingTicket):
        fee = self.pricing_service.calculate_fee(
            ticket.get_entry_time(),
            time.time(),
            ticket.get_spot().get_type()
        )

        if self.payment_service.process_payment(fee):
            ticket.get_spot().release()
