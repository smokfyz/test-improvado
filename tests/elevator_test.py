import pytest

from elevator import Elevator
from elevator.elevator import ElevatorStatus, Direction
from elevator.exceptions import ElevatorIsEmpty, ElevatorIsFull, UnexpectedFloor


def test_elevator_initial_state():
    elevator = Elevator((1, 10), 5)

    assert elevator._number_of_passengers == 0
    assert elevator._status == ElevatorStatus.IDLE
    assert len(elevator._requested_floors_outside) == 0
    assert len(elevator._requested_floors_inside) == 0
    assert elevator._current_floor == 1
    assert elevator._direction == Direction.DOWN


def test_elevator_move_to_destination_floor():
    elevator = Elevator((1, 10), 5)

    elevator.call(4)
    assert len(elevator._requested_floors_outside) == 1
    assert elevator._requested_floors_outside[0] == 4

    elevator.move()
    assert elevator._status == ElevatorStatus.MOVING
    assert elevator._current_floor == 1

    elevator.move()
    assert elevator._status == ElevatorStatus.MOVING
    assert elevator._current_floor == 2

    elevator.move()
    assert elevator._status == ElevatorStatus.MOVING
    assert elevator._current_floor == 3

    elevator.move()
    assert elevator._status == ElevatorStatus.MOVING
    assert elevator._current_floor == 4

    elevator.move()
    assert elevator._status == ElevatorStatus.BOARDING
    assert elevator._current_floor == 4


def test_can_enter_elevator(elevator_with_boarding_status_on_first_floor):
    elevator_with_boarding_status_on_first_floor.enter()
    assert elevator_with_boarding_status_on_first_floor._number_of_passengers == 1


def test_can_exit_elevator(elevator_with_boarding_status_on_first_floor):
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.exit()
    assert elevator_with_boarding_status_on_first_floor._number_of_passengers == 0


def test_cant_exit_empty_elevator(elevator_with_boarding_status_on_first_floor):
    with pytest.raises(ElevatorIsEmpty):
        elevator_with_boarding_status_on_first_floor.exit()


def test_cant_enter_full_elevator(elevator_with_boarding_status_on_first_floor):
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    with pytest.raises(ElevatorIsFull):
        elevator_with_boarding_status_on_first_floor.enter()


def test_is_empty_return_valid_value(elevator_with_boarding_status_on_first_floor):
    assert elevator_with_boarding_status_on_first_floor.is_empty
    elevator_with_boarding_status_on_first_floor.enter()
    assert not elevator_with_boarding_status_on_first_floor.is_empty


def test_is_full_return_valid_value(elevator_with_boarding_status_on_first_floor):
    assert not elevator_with_boarding_status_on_first_floor.is_full

    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()

    assert elevator_with_boarding_status_on_first_floor.is_full


def test_is_call_unexpected_floor_raise_exception(elevator_with_boarding_status_on_first_floor):
    with pytest.raises(UnexpectedFloor):
        elevator_with_boarding_status_on_first_floor.call(999)


def test_is_select_unexpected_floor_raise_exception(elevator_with_boarding_status_on_first_floor):
    with pytest.raises(UnexpectedFloor):
        elevator_with_boarding_status_on_first_floor.select(999)


def test_is_boarding_return_expected_value(elevator_with_boarding_status_on_first_floor):
    assert elevator_with_boarding_status_on_first_floor.is_boarding(1)
    assert not elevator_with_boarding_status_on_first_floor.is_boarding(5)


def test_elevator_skip_outside_stops_when_full(elevator_with_boarding_status_on_first_floor):
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.call(2)
    elevator_with_boarding_status_on_first_floor.select(3)
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor._current_floor = 3
    elevator_with_boarding_status_on_first_floor._status = ElevatorStatus.BOARDING


def test_elevator_doesnt_change_direction_before_last_stop(elevator_with_boarding_status_on_first_floor):
    elevator_with_boarding_status_on_first_floor.enter()
    elevator_with_boarding_status_on_first_floor.select(3)
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.select(1)
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor.move()
    elevator_with_boarding_status_on_first_floor._current_floor = 3
    elevator_with_boarding_status_on_first_floor._status = ElevatorStatus.BOARDING
