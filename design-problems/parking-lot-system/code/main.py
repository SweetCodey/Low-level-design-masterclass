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

    ticket1 = entrance.enter(car)
    ticket2 = entrance.enter(bike)

    if ticket1:
        exit_gate.exit(ticket1)

    if ticket2:
        exit_gate.exit(ticket2)
