from datetime import datetime, timedelta

from tests.use_cases.fakes import FakeRideRepository
from use_cases.list_available_rides import ListAvailableRidesUseCase
from use_cases.offer_ride import OfferRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def test_excludes_rides_offered_by_the_viewer():
    rides_repo = FakeRideRepository()
    OfferRideUseCase(rides_repo).execute(
        1,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "3",
            "price_per_seat": "0",
        },
    )

    results = ListAvailableRidesUseCase(rides_repo).execute(viewer_id=1)

    assert results == []


def test_filters_by_search_term():
    rides_repo = FakeRideRepository()
    OfferRideUseCase(rides_repo).execute(
        1,
        {
            "origin": "Barra da Tijuca",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "3",
            "price_per_seat": "0",
        },
    )

    results = ListAvailableRidesUseCase(rides_repo).execute(viewer_id=2, search="Barra")

    assert len(results) == 1
    assert results[0].origin == "Barra da Tijuca"
