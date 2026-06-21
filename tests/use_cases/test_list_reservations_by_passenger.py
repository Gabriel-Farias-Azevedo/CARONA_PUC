from datetime import datetime, timedelta

from tests.use_cases.fakes import (
    FakeReservationRepository,
    FakeRideRepository,
    FakeTransactionManager,
)
from use_cases.list_reservations_by_passenger import ListReservationsByPassengerUseCase
from use_cases.offer_ride import OfferRideUseCase
from use_cases.reserve_ride import ReserveRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def test_lists_only_reservations_of_the_given_passenger():
    rides_repo = FakeRideRepository()
    ride = OfferRideUseCase(rides_repo).execute(
        1,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "2",
            "price_per_seat": "0",
        },
    )
    reservations_repo = FakeReservationRepository()
    tx = FakeTransactionManager()
    ReserveRideUseCase(rides_repo, reservations_repo, tx).execute(ride.id, passenger_id=2)
    ReserveRideUseCase(rides_repo, reservations_repo, tx).execute(ride.id, passenger_id=3)

    results = ListReservationsByPassengerUseCase(reservations_repo).execute(passenger_id=2)

    assert len(results) == 1
    assert results[0].passenger_id == 2
