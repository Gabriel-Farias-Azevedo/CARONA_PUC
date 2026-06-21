from datetime import datetime, timedelta

import pytest

from tests.use_cases.fakes import FakeRideRepository
from use_cases.exceptions import ValidationError
from use_cases.offer_ride import OfferRideUseCase

FUTURE = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
PAST = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")


def test_offers_a_valid_ride():
    use_case = OfferRideUseCase(FakeRideRepository())

    ride = use_case.execute(
        1,
        {
            "origin": "Barra",
            "destination": "Gávea",
            "departure_at": FUTURE,
            "seats_total": "3",
            "price_per_seat": "10,50",
        },
    )

    assert ride.id is not None
    assert ride.price_per_seat == 10.5
    assert ride.seats_taken == 0


def test_rejects_ride_in_the_past():
    use_case = OfferRideUseCase(FakeRideRepository())

    with pytest.raises(ValidationError):
        use_case.execute(
            1,
            {
                "origin": "Barra",
                "destination": "Gávea",
                "departure_at": PAST,
                "seats_total": "3",
                "price_per_seat": "0",
            },
        )


def test_rejects_more_than_max_seats():
    use_case = OfferRideUseCase(FakeRideRepository())

    with pytest.raises(ValidationError):
        use_case.execute(
            1,
            {
                "origin": "Barra",
                "destination": "Gávea",
                "departure_at": FUTURE,
                "seats_total": "9",
                "price_per_seat": "0",
            },
        )


def test_rejects_negative_price():
    use_case = OfferRideUseCase(FakeRideRepository())

    with pytest.raises(ValidationError):
        use_case.execute(
            1,
            {
                "origin": "Barra",
                "destination": "Gávea",
                "departure_at": FUTURE,
                "seats_total": "2",
                "price_per_seat": "-5",
            },
        )
