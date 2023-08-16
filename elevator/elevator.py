import logging
from enum import auto, Enum
from typing import Tuple
from sortedcontainers import SortedSet

from .exceptions import (
    UnexpectedFloor,
    ElevatorIsFull,
    ElevatorIsEmpty,
    NotBoardingStatus,
)


log = logging.getLogger(__name__)


class ElevatorStatus(Enum):
    IDLE = auto()
    BOARDING = auto()
    MOVING = auto()


class Direction(Enum):
    UP = auto()
    DOWN = auto()


class Elevator:
    def __init__(self, floors_range: Tuple[int, int] = (1, 10), capacity: int = 5) -> None:
        self._floors_range = floors_range
        self._capacity = capacity

        self._current_floor = floors_range[0]

        # Split floor requests to two types to handle cases when
        # elevator is full and must skip all floors which were
        # requested from outside.
        self._requested_floors_outside = SortedSet()
        self._requested_floors_inside = SortedSet()

        self._status = ElevatorStatus.IDLE
        self._direction = Direction.DOWN
        self._number_of_passengers = 0

    def move(self) -> None:
        if not self._is_any_requested_floors:
            self._status = ElevatorStatus.IDLE
            self._log_status()
            return

        if self._should_boarding_be_on_current_floor:
            self._status = ElevatorStatus.BOARDING
            self._visit_current_floor()
            self._log_status()
            return

        if self._status != ElevatorStatus.MOVING:
            self._status = ElevatorStatus.MOVING
            self._log_status()
            return

        if self._should_direction_be_changed:
            self._change_direction()

        self._current_floor += 1 if self._direction == Direction.UP else -1
        self._log_status()

    def call(self, floor: int) -> None:
        self._is_floor_in_range(floor)
        self._requested_floors_outside.add(floor)

    def select(self, floor: int) -> None:
        self._is_floor_in_range(floor)
        self._requested_floors_inside.add(floor)

    def enter(self) -> None:
        if self.is_full:
            raise ElevatorIsFull()
        if self._status != ElevatorStatus.BOARDING:
            raise NotBoardingStatus()
        self._number_of_passengers += 1

    def exit(self) -> None:
        if self.is_empty:
            raise ElevatorIsEmpty()
        if self._status != ElevatorStatus.BOARDING:
            raise NotBoardingStatus()
        self._number_of_passengers -= 1

    def is_boarding(self, floor: int) -> bool:
        return (
            self._status == ElevatorStatus.BOARDING and
            self._current_floor == floor
        )

    @property
    def is_full(self) -> bool:
        return self._number_of_passengers == self._capacity

    @property
    def is_empty(self) -> bool:
        return self._number_of_passengers == 0

    def _is_floor_in_range(self, floor: int) -> None:
        if self._floors_range[0] > floor or floor > self._floors_range[1]:
            raise UnexpectedFloor(f"Unexpected floor: {floor}. Floors range: {self._floors_range}.")

    @property
    def _is_any_requested_floors(self) -> bool:
        return (
            len(self._requested_floors_outside) != 0 or
            len(self._requested_floors_inside) != 0
        )

    @property
    def _should_boarding_be_on_current_floor(self) -> bool:
        return (
            self._current_floor in self._requested_floors_inside or
            not self.is_full and self._current_floor in self._requested_floors_outside
        )

    @property
    def _any_boarding_on_higher_floors(self) -> bool:
        return (
            self._requested_floors_inside.bisect_left(
                self._current_floor
            ) != len(
                self._requested_floors_inside
            ) or
            not self.is_full and self._requested_floors_outside.bisect_left(
                self._current_floor
            ) != len(
                self._requested_floors_outside
            )
        )

    @property
    def _any_boarding_on_lower_floors(self) -> bool:
        return (
            self._requested_floors_inside.bisect_right(self._current_floor) != 0 or
            not self.is_full and self._requested_floors_outside.bisect_right(self._current_floor) != 0
        )

    @property
    def _should_direction_be_changed(self) -> bool:
        if self._direction == Direction.UP and self._any_boarding_on_higher_floors:
            return False
        if self._direction == Direction.DOWN and self._any_boarding_on_lower_floors:
            return False
        return True

    def _change_direction(self) -> None:
        self._direction = Direction.UP if self._direction == Direction.DOWN else Direction.DOWN

    def _visit_current_floor(self) -> None:
        try:
            self._requested_floors_outside.remove(self._current_floor)
        except KeyError:
            pass

        try:
            self._requested_floors_inside.remove(self._current_floor)
        except KeyError:
            pass

    def _log_status(self) -> None:
        log.info(
            f"Elevator status is {self._status.name}. Current floor: {self._current_floor}. "
            f"Current direction: {self._direction.name}. Number of passenger: {self._number_of_passengers}."
        )
