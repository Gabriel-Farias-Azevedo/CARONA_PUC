import sqlite3
from typing import Optional

from domain.reservation import Reservation
from domain.ride import Ride
from use_cases.repositories import ReservationRepository

_BY_PASSENGER_SQL = """
    SELECT res.*,
           r.driver_id, r.origin, r.destination, r.departure_at,
           r.seats_total, r.seats_taken, r.price_per_seat,
           u.name AS driver_name, u.phone AS driver_phone
    FROM reservations res
    JOIN rides r ON r.id = res.ride_id
    JOIN users u ON u.id = r.driver_id
    WHERE res.passenger_id = ?
    ORDER BY res.created_at DESC
"""


class SqliteReservationRepository(ReservationRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def create(self, ride_id: int, passenger_id: int) -> Reservation:
        cursor = self._conn.execute(
            "INSERT INTO reservations (ride_id, passenger_id, status) VALUES (?, ?, ?)",
            (ride_id, passenger_id, Reservation.ACTIVE),
        )
        return self.find_by_id(cursor.lastrowid)

    def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
        row = self._conn.execute(
            "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
        ).fetchone()
        return self._hydrate(row) if row else None

    def active_reservation(self, ride_id: int, passenger_id: int) -> Optional[Reservation]:
        row = self._conn.execute(
            "SELECT * FROM reservations WHERE ride_id = ? AND passenger_id = ? AND status = ?",
            (ride_id, passenger_id, Reservation.ACTIVE),
        ).fetchone()
        return self._hydrate(row) if row else None

    def cancel(self, reservation_id: int) -> None:
        self._conn.execute(
            "UPDATE reservations SET status = ? WHERE id = ?",
            (Reservation.CANCELLED, reservation_id),
        )

    def by_passenger(self, passenger_id: int) -> list[Reservation]:
        rows = self._conn.execute(_BY_PASSENGER_SQL, (passenger_id,)).fetchall()
        return [self._hydrate_with_ride(row) for row in rows]

    @staticmethod
    def _hydrate(row: sqlite3.Row) -> Reservation:
        return Reservation(
            id=row["id"],
            ride_id=row["ride_id"],
            passenger_id=row["passenger_id"],
            status=row["status"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _hydrate_with_ride(row: sqlite3.Row) -> Reservation:
        ride = Ride(
            id=row["ride_id"],
            driver_id=row["driver_id"],
            origin=row["origin"],
            destination=row["destination"],
            departure_at=row["departure_at"],
            seats_total=row["seats_total"],
            seats_taken=row["seats_taken"],
            price_per_seat=row["price_per_seat"],
            driver_name=row["driver_name"],
            driver_phone=row["driver_phone"],
        )
        return Reservation(
            id=row["id"],
            ride_id=row["ride_id"],
            passenger_id=row["passenger_id"],
            status=row["status"],
            created_at=row["created_at"],
            ride=ride,
        )
