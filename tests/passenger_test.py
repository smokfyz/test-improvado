import pytest
from unittest.mock import Mock, PropertyMock

from elevator import Passenger


def test_can_enter_empty_elevator_with_boarding_status():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=True)
    type(elevator).is_full = PropertyMock(return_value=False)

    passenger = Passenger(1, 10)

    assert passenger.can_enter(elevator)

    elevator.is_boarding.assert_called_once_with(1)


def test_cant_enter_full_elevator():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=True)
    type(elevator).is_full = PropertyMock(return_value=True)

    passenger = Passenger(1, 10)

    assert not passenger.can_enter(elevator)


def test_cant_enter_elevator_not_in_boarding_status():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=False)
    type(elevator).is_full = PropertyMock(return_value=False)

    passenger = Passenger(1, 10)

    assert not passenger.can_enter(elevator)


def test_can_exit_elevator_with_boarding_status():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=True)

    passenger = Passenger(1, 10)

    assert passenger.can_exit(elevator)



    elevator.is_boarding.assert_called_once_with(10)


def test_can_exit_elevator_with_not_boarding_status():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=False)

    passenger = Passenger(1, 10)

    assert not passenger.can_exit(elevator)


def test_passenger_can_call_elevator_floor():
    elevator = Mock()

    passenger = Passenger(1, 5)

    passenger.call(elevator)
    elevator.call.assert_called_once_with(1)


def test_passenger_can_select_elevator_floor():
    elevator = Mock()

    passenger = Passenger(1, 5)

    passenger.select(elevator)
    elevator.select.assert_called_once_with(5)


def test_passenger_enter_elevator_return_valid_result():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=True)
    type(elevator).is_full = PropertyMock(return_value=True)

    passenger = Passenger(1, 5)

    passenger.enter(elevator)
    elevator.enter.assert_called_once()


def test_passenger_exit_elevator_return_valid_result():
    elevator = Mock()
    elevator.is_boarding = Mock(return_value=True)

    passenger = Passenger(1, 5)

    passenger.exit(elevator)
    elevator.exit.assert_called_once()



