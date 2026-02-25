from DispatchStrategy import NearestIdleStrategy
from ElevatorSystem import ElevatorSystem
from enums import Direction

# Dependency Injection: we create the strategy outside
# and inject it into ElevatorSystem. Tomorrow if we want
# LeastBusyStrategy, we just change what we pass in.
dispatch_strategy = NearestIdleStrategy()
system = ElevatorSystem.get_instance(10, 3, dispatch_strategy)

print("=" * 60)
print("SCENARIO 1: Maintenance Mode")
print("  Car 2 is in maintenance. Call elevator from floor 5.")
print("  System should skip car 2 and dispatch another car.")
print("=" * 60)

car3 = system.get_cars()[2]
car3.enter_maintenance()

system.call_elevator(5, Direction.UP)
system.dispatcher()

# Take car 3 out of maintenance
car3.exit_maintenance()

print()
print("=" * 60)
print("SCENARIO 2: Overload")
print("  Car 0 is loaded with 700 kg (max: 680 kg).")
print("  Call elevator from floor 3. Car 0 should be skipped.")
print("=" * 60)

car1 = system.get_cars()[0]
car1.add_load(700)  # exceeds 680 kg limit

system.call_elevator(3, Direction.DOWN)
system.dispatcher()  # car1 won't be dispatched since it's overloaded

print()
print("=" * 60)
print("SCENARIO 3: Passenger Ride (Activity 4 & 5)")
print("  Passenger inside car 1 selects floor 7.")
print("=" * 60)

car2 = system.get_cars()[1]
system.select_floor(car2, 7)

print()
print("=" * 60)
print("SCENARIO 4: Emergency Stop")
print("  Car 1 triggers an emergency stop.")
print("=" * 60)

car2.emergency_stop()

print()
print("=" * 60)
print("SCENARIO 5: Overload Recovery")
print("  Remove load from car 0 and dispatch it to floor 8.")
print("=" * 60)

car1.remove_load(700)

system.call_elevator(8, Direction.UP)
system.dispatcher()
