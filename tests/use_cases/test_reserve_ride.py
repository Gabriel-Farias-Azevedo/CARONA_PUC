from datetime import datetime, timedelta

import pytest

from tests.use_cases.fakes import (FakeReservationRepository,
                                   FakeRideRepository, FakeTransactionManager)
from use_cases.exceptions import ValidationError
from use_cases.offer_ride import OfferRideUseCase
from use_cases.reserve_ride import ReserveRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def _offer_ride(rides_repo, driver_id=1, seats=1):
    return OfferRideUseCase(rides_repo).execute(
        driver_id,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": str(seats),
            "price_per_seat": "0",
        },
    )


def test_reserves_a_seat_successfully():
    rides_repo = FakeRideRepository()
    ride = _offer_ride(rides_repo)
    use_case = ReserveRideUseCase(
        rides_repo, FakeReservationRepository(), FakeTransactionManager()
    )

    reservation = use_case.execute(ride.id, passenger_id=2)

    assert reservation.passenger_id == 2
    assert rides_repo.find_by_id(ride.id).seats_taken == 1


def test_rejects_reserving_own_ride():
    rides_repo = FakeRideRepository()
    ride = _offer_ride(rides_repo, driver_id=1)
    use_case = ReserveRideUseCase(
        rides_repo, FakeReservationRepository(), FakeTransactionManager()
    )

    with pytest.raises(ValidationError):
        use_case.execute(ride.id, passenger_id=1)


def test_rejects_double_reservation_by_same_passenger():
    rides_repo = FakeRideRepository()
    ride = _offer_ride(rides_repo, seats=2)
    use_case = ReserveRideUseCase(
        rides_repo, FakeReservationRepository(), FakeTransactionManager()
    )
    use_case.execute(ride.id, passenger_id=2)

    with pytest.raises(ValidationError):
        use_case.execute(ride.id, passenger_id=2)


def test_rejects_reservation_when_ride_is_full():
    rides_repo = FakeRideRepository()
    ride = _offer_ride(rides_repo, seats=1)
    use_case = ReserveRideUseCase(
        rides_repo, FakeReservationRepository(), FakeTransactionManager()
    )
    use_case.execute(ride.id, passenger_id=2)

    with pytest.raises(ValidationError):
        use_case.execute(ride.id, passenger_id=3)
