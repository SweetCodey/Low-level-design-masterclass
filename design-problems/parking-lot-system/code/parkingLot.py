from enum import Enum
from abc import ABC, abstractmethod
import time


# ---------- ENUM ----------

class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"


# ---------- BASIC ENTITIES ----------

class Vehicle:
    def __init__(self, number: str, vehicle_type: VehicleType):
        self.number = number
        self.type = vehicle_type

    def get_number(self) -> str:
        return self.number

    def get_type(self) -> VehicleType:
        return self.type


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


# ---------- STRATEGIES ----------

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, entry_time: float, exit_time: float, vehicle_type: VehicleType) -> int:
        pass


class HourlyPricing(PricingStrategy):
    def __init__(self, rates: dict):
        self.rates = rates  # {VehicleType.BIKE: 20, VehicleType.CAR: 50, ...}

    def calculate_fee(self, entry_time: float, exit_time: float, vehicle_type: VehicleType) -> int:
        hours = int((exit_time - entry_time) / 3600)
        if hours < 1:
            hours = 1
        return hours * self.rates[vehicle_type]


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: int) -> bool:
        pass


class CashPayment(PaymentStrategy):
    def process_payment(self, amount: int) -> bool:
        print(f"  Payment of Rs.{amount} processed via cash.")
        return True


# ---------- FACTORY ----------

class ParkingSpotFactory:
    @staticmethod
    def get_spot_type(vehicle_type: VehicleType) -> VehicleType:
        # Since we use a single enum, the mapping is direct.
        # Bike -> BIKE spot (Compact), Car -> CAR spot (Regular), Truck -> TRUCK spot (Large)
        return vehicle_type


# ---------- PARKING LOT SYSTEM (SINGLETON) ----------

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


# ---------- GATES ----------

class EntranceGate:
    def __init__(self, system: ParkingLotSystem):
        self.system = system

    def enter(self, vehicle: Vehicle):
        return self.system.handle_entry(vehicle)


class ExitGate:
    def __init__(self, system: ParkingLotSystem):
        self.system = system

    def exit(self, ticket: ParkingTicket):
        self.system.handle_exit(ticket)


# ---------- MAIN ----------

if __name__ == "__main__":
    # Dependency Injection: we create the dependencies outside
    # and inject them into ParkingLotSystem. Tomorrow if we want
    # PeakHourPricing or CardPayment, we just change what we pass in.
    rates = {VehicleType.BIKE: 20, VehicleType.CAR: 50, VehicleType.TRUCK: 100}
    pricing_service = HourlyPricing(rates)
    payment_service = CashPayment()

    system = ParkingLotSystem.get_instance(pricing_service, payment_service)

    # Add spots of different types
    system.add_spot(ParkingSpot(1, VehicleType.BIKE))
    system.add_spot(ParkingSpot(2, VehicleType.CAR))
    system.add_spot(ParkingSpot(3, VehicleType.CAR))
    system.add_spot(ParkingSpot(4, VehicleType.TRUCK))

    entrance = EntranceGate(system)
    exit_gate = ExitGate(system)

    car = Vehicle("KA-01-1234", VehicleType.CAR)
    bike = Vehicle("KA-05-9876", VehicleType.BIKE)

    print("--- Car entering ---")
    ticket1 = entrance.enter(car)
    if ticket1:
        print(f"  Car parked at spot {ticket1.get_spot().get_id()}")

    print("--- Bike entering ---")
    ticket2 = entrance.enter(bike)
    if ticket2:
        print(f"  Bike parked at spot {ticket2.get_spot().get_id()}")

    print("--- Car exiting ---")
    if ticket1:
        exit_gate.exit(ticket1)
        print(f"  Spot {ticket1.get_spot().get_id()} is now free: {ticket1.get_spot().available()}")

    print("--- Bike exiting ---")
    if ticket2:
        exit_gate.exit(ticket2)
        print(f"  Spot {ticket2.get_spot().get_id()} is now free: {ticket2.get_spot().available()}")
