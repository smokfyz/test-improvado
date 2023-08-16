import logging
from enum import auto, Enum

from .elevator import Elevator
from .exceptions import UnexpectedFloor, ElevatorIsFull

log = logging.getLogger(__name__)


class PassengerStatus(Enum):
    INIT = auto()
    WAITING_FOR_ELEVATOR = auto()
    ON_THE_WAY = auto()
    AT_THE_DESTINATION = auto()


class Passenger:
    def __init__(self, current_floor: int, destination_floor: int) -> None:
        log.info(f"New passenger on {current_floor} -> {destination_floor} floor.")

        self._current_floor = current_floor
        self._destination_floor = destination_floor

        self.status = PassengerStatus.INIT

    def call(self, elevator: Elevator) -> None:
        log.info(f"Passenger call the elevator on {self._current_floor} floor.")

        elevator.call(self._current_floor)
        self.status = PassengerStatus.WAITING_FOR_ELEVATOR

    def select(self, elevator: Elevator) -> None:
        log.info(f"Passenger select {self._destination_floor} floor in the elevator.")

        elevator.select(self._destination_floor)

    def can_enter(self, elevator) -> None:
        return elevator.is_boarding(self._current_floor) and not elevator.is_full

    def can_exit(self, elevator) -> None:
        return elevator.is_boarding(self._destination_floor)

    def enter(self, elevator: Elevator) -> None:
        if not self.can_enter(elevator):
            UnexpectedFloor()

        log.info("Passenger enter the elevator.")

        try:
            elevator.enter()
            self.status = PassengerStatus.ON_THE_WAY
        except ElevatorIsFull:
            self.call(elevator)

    def exit(self, elevator: Elevator) -> None:
        if not self.can_exit(elevator):
            UnexpectedFloor()

        log.info("Passenger exit the elevator.")

        elevator.exit()
        self.status = PassengerStatus.AT_THE_DESTINATION
