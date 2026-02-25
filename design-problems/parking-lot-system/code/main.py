from enums import VehicleType
from Vehicle import Vehicle
from ParkingSpot import ParkingSpot
from ParkingLotSystem import ParkingLotSystem
from HourlyPricing import HourlyPricing
from CashPayment import CashPayment
from EntranceGate import EntranceGate
from ExitGate import ExitGate


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
