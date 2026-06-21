from datetime import datetime, timedelta

import pytest

from tests.use_cases.fakes import (
    FakeReservationRepository,
    FakeRideRepository,
    FakeTransactionManager,
)
from use_cases.cancel_reservation import CancelReservationUseCase
from use_cases.exceptions import ValidationError
from use_cases.offer_ride import OfferRideUseCase
from use_cases.reserve_ride import ReserveRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def _setup_active_reservation(seats=1):
    rides_repo = FakeRideRepository()
    ride = OfferRideUseCase(rides_repo).execute(
        1,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": str(seats),
            "price_per_seat": "0",
        },
    )
    reservations_repo = FakeReservationRepository()
    tx = FakeTransactionManager()
    reservation = ReserveRideUseCase(rides_repo, reservations_repo, tx).execute(ride.id, passenger_id=2)
    return rides_repo, reservations_repo, tx, ride, reservation


def test_cancels_an_active_reservation_and_releases_the_seat():
    rides_repo, reservations_repo, tx, ride, reservation = _setup_active_reservation()

    CancelReservationUseCase(rides_repo, reservations_repo, tx).execute(reservation.id, passenger_id=2)

    assert rides_repo.find_by_id(ride.id).seats_taken == 0
    assert not reservations_repo.find_by_id(reservation.id).is_active()


def test_rejects_cancelling_someone_elses_reservation():
    rides_repo, reservations_repo, tx, _ride, reservation = _setup_active_reservation()

    with pytest.raises(ValidationError):
        CancelReservationUseCase(rides_repo, reservations_repo, tx).execute(reservation.id, passenger_id=99)


def test_rejects_cancelling_twice():
    rides_repo, reservations_repo, tx, _ride, reservation = _setup_active_reservation()
    use_case = CancelReservationUseCase(rides_repo, reservations_repo, tx)
    use_case.execute(reservation.id, passenger_id=2)

    with pytest.raises(ValidationError):
        use_case.execute(reservation.id, passenger_id=2)
