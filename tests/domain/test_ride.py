from domain.ride import Ride


def make_ride(seats_total=4, seats_taken=0, price=0.0) -> Ride:
    return Ride(
        id=1,
        driver_id=10,
        origin="Barra",
        destination="Gávea",
        departure_at="2026-01-01 10:00",
        seats_total=seats_total,
        seats_taken=seats_taken,
        price_per_seat=price,
    )


def test_seats_available_subtracts_taken_from_total():
    ride = make_ride(seats_total=4, seats_taken=1)
    assert ride.seats_available() == 3


def test_seats_available_never_negative():
    ride = make_ride(seats_total=2, seats_taken=5)
    assert ride.seats_available() == 0


def test_has_seats_true_when_available():
    assert make_ride(seats_total=2, seats_taken=1).has_seats() is True


def test_has_seats_false_when_full():
    assert make_ride(seats_total=2, seats_taken=2).has_seats() is False


def test_is_free_true_for_zero_price():
    assert make_ride(price=0.0).is_free() is True


def test_is_free_false_for_positive_price():
    assert make_ride(price=12.5).is_free() is False
