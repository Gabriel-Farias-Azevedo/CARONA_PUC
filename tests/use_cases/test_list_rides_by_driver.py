from datetime import datetime, timedelta

from tests.use_cases.fakes import FakeRideRepository
from use_cases.list_rides_by_driver import ListRidesByDriverUseCase
from use_cases.offer_ride import OfferRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def test_lists_only_rides_of_the_given_driver():
    rides_repo = FakeRideRepository()
    OfferRideUseCase(rides_repo).execute(
        1,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "2",
            "price_per_seat": "0",
        },
    )
    OfferRideUseCase(rides_repo).execute(
        2,
        {
            "origin": "Leblon",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "2",
            "price_per_seat": "0",
        },
    )

    results = ListRidesByDriverUseCase(rides_repo).execute(driver_id=1)

    assert len(results) == 1
    assert results[0].driver_id == 1
