import random

from elevator import Elevator, Passenger, PassengerStatus


FLOORS_RANGE = (1, 10)
ELEVATOR_CAPACITY = 5
SIMULATION_STEPS = 100
NEW_PASSENGER_PERIOD = 5  # add new passenger every NEW_PASSENGER_PERIOD step


def simulate_passenger_behavior_exit(passenger: Passenger, elevator: Elevator) -> None:
    if passenger.status == PassengerStatus.ON_THE_WAY:
        if passenger.can_exit(elevator):
            passenger.exit(elevator)


def simulate_passenger_behavior_enter(passenger: Passenger, elevator: Elevator) -> None:
    if passenger.status == PassengerStatus.INIT:
        passenger.call(elevator)
    elif passenger.status == PassengerStatus.WAITING_FOR_ELEVATOR:
        if passenger.can_enter(elevator):
            passenger.enter(elevator)
            passenger.select(elevator)


if __name__ == "__main__":
    passengers = []
    elevator = Elevator(FLOORS_RANGE, ELEVATOR_CAPACITY)

    for step in range(SIMULATION_STEPS):
        if step % NEW_PASSENGER_PERIOD == 0:
            current_floor = random.randint(FLOORS_RANGE[0], FLOORS_RANGE[1])
            destination_floor = random.randint(FLOORS_RANGE[0], FLOORS_RANGE[1])
            if current_floor != destination_floor:
                passengers.append(Passenger(current_floor, destination_floor))

        elevator.move()

        # Firstly process passengers who can get out to make space for other passengers
        for passenger in passengers:
            simulate_passenger_behavior_exit(passenger, elevator)

        # Filter passengers who already at the destination point
        passengers = [
            passenger
            for passenger in passengers
            if passenger.status != PassengerStatus.AT_THE_DESTINATION
        ]

        for passenger in passengers:
            simulate_passenger_behavior_enter(passenger, elevator)
