from domain.reservation import Reservation


def test_is_active_true_for_active_status():
    reservation = Reservation(
        id=1,
        ride_id=1,
        passenger_id=2,
        status=Reservation.ACTIVE,
        created_at="2026-01-01",
    )
    assert reservation.is_active() is True


def test_is_active_false_for_cancelled_status():
    reservation = Reservation(
        id=1,
        ride_id=1,
        passenger_id=2,
        status=Reservation.CANCELLED,
        created_at="2026-01-01",
    )
    assert reservation.is_active() is False
