import sqlite3
from datetime import datetime
from typing import Optional

from domain.ride import Ride
from use_cases.repositories import RideRepository

_BASE_SELECT = """
    SELECT r.*, u.name AS driver_name, u.phone AS driver_phone
    FROM rides r
    JOIN users u ON u.id = r.driver_id
"""


class SqliteRideRepository(RideRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def create(self, ride: Ride) -> Ride:
        cursor = self._conn.execute(
            """INSERT INTO rides
               (driver_id, origin, destination, departure_at, seats_total, seats_taken, price_per_seat)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ride.driver_id,
                ride.origin,
                ride.destination,
                ride.departure_at,
                ride.seats_total,
                ride.seats_taken,
                ride.price_per_seat,
            ),
        )
        return self.find_by_id(cursor.lastrowid)

    def find_by_id(self, ride_id: int) -> Optional[Ride]:
        row = self._conn.execute(
            _BASE_SELECT + " WHERE r.id = ?", (ride_id,)
        ).fetchone()
        return self._hydrate(row) if row else None

    def available(self, search: str, exclude_driver_id: int) -> list[Ride]:
        sql = _BASE_SELECT + """
            WHERE r.seats_taken < r.seats_total
              AND r.departure_at >= ?
              AND r.driver_id <> ?
        """
        params: list = [datetime.now().strftime("%Y-%m-%d %H:%M"), exclude_driver_id]

        search = search.strip()
        if search != "":
            sql += " AND (r.origin LIKE ? OR r.destination LIKE ?)"
            like = f"%{search}%"
            params += [like, like]

        sql += " ORDER BY r.departure_at ASC"

        rows = self._conn.execute(sql, params).fetchall()
        return [self._hydrate(row) for row in rows]

    def by_driver(self, driver_id: int) -> list[Ride]:
        rows = self._conn.execute(
            _BASE_SELECT + " WHERE r.driver_id = ? ORDER BY r.departure_at DESC",
            (driver_id,),
        ).fetchall()
        return [self._hydrate(row) for row in rows]

    def take_seat(self, ride_id: int) -> bool:
        # O filtro "seats_taken < seats_total" na própria UPDATE torna a operação
        # atômica: o banco recusa a vaga extra se a carona acabou de lotar.
        cursor = self._conn.execute(
            "UPDATE rides SET seats_taken = seats_taken + 1 WHERE id = ? AND seats_taken < seats_total",
            (ride_id,),
        )
        return cursor.rowcount == 1

    def release_seat(self, ride_id: int) -> None:
        self._conn.execute(
            "UPDATE rides SET seats_taken = seats_taken - 1 WHERE id = ? AND seats_taken > 0",
            (ride_id,),
        )

    @staticmethod
    def _hydrate(row: sqlite3.Row) -> Ride:
        return Ride(
            id=row["id"],
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
