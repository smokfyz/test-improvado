import pytest

from elevator import Elevator


@pytest.fixture
def elevator_with_idle_status_on_first_floor():
    return Elevator((1, 10), 5)


@pytest.fixture
def elevator_with_boarding_status_on_first_floor():
    elevator = Elevator((1, 10), 5)
    elevator.call(1)
    elevator.move()
    return elevator
