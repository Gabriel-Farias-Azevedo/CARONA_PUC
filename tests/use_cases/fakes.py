"""Repositórios em memória usados nos testes para isolar a lógica de negócio
dos use cases da infraestrutura real (SQLite). Implementam os mesmos
contratos (use_cases.repositories) que os adaptadores SQLite de produção.
"""

from dataclasses import replace
from typing import Optional

from domain.reservation import Reservation
from domain.ride import Ride
from domain.user import User
from use_cases.repositories import (
    ReservationRepository,
    RideRepository,
    TransactionManager,
    UserRepository,
)


class FakeUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.email == email), None)

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def save(self, user: User) -> User:
        saved = replace(user, id=self._next_id)
        self._users[self._next_id] = saved
        self._next_id += 1
        return saved

    def update(self, user: User) -> None:
        self._users[user.id] = user


class FakeRideRepository(RideRepository):
    def __init__(self):
        self._rides: dict[int, Ride] = {}
        self._next_id = 1

    def create(self, ride: Ride) -> Ride:
        saved = replace(ride, id=self._next_id)
        self._rides[self._next_id] = saved
        self._next_id += 1
        return saved

    def find_by_id(self, ride_id: int) -> Optional[Ride]:
        return self._rides.get(ride_id)

    def available(self, search: str, exclude_driver_id: int) -> list[Ride]:
        results = [
            r
            for r in self._rides.values()
            if r.seats_taken < r.seats_total and r.driver_id != exclude_driver_id
        ]
        if search:
            term = search.lower()
            results = [r for r in results if term in r.origin.lower() or term in r.destination.lower()]
        return sorted(results, key=lambda r: r.departure_at)

    def by_driver(self, driver_id: int) -> list[Ride]:
        return [r for r in self._rides.values() if r.driver_id == driver_id]

    def take_seat(self, ride_id: int) -> bool:
        ride = self._rides.get(ride_id)
        if ride is None or ride.seats_taken >= ride.seats_total:
            return False
        self._rides[ride_id] = replace(ride, seats_taken=ride.seats_taken + 1)
        return True

    def release_seat(self, ride_id: int) -> None:
        ride = self._rides.get(ride_id)
        if ride is not None and ride.seats_taken > 0:
            self._rides[ride_id] = replace(ride, seats_taken=ride.seats_taken - 1)


class FakeReservationRepository(ReservationRepository):
    def __init__(self):
        self._reservations: dict[int, Reservation] = {}
        self._next_id = 1

    def create(self, ride_id: int, passenger_id: int) -> Reservation:
        reservation = Reservation(
            id=self._next_id,
            ride_id=ride_id,
            passenger_id=passenger_id,
            status=Reservation.ACTIVE,
            created_at="2026-01-01 00:00:00",
        )
        self._reservations[self._next_id] = reservation
        self._next_id += 1
        return reservation

    def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self._reservations.get(reservation_id)

    def active_reservation(self, ride_id: int, passenger_id: int) -> Optional[Reservation]:
        return next(
            (
                r
                for r in self._reservations.values()
                if r.ride_id == ride_id and r.passenger_id == passenger_id and r.is_active()
            ),
            None,
        )

    def cancel(self, reservation_id: int) -> None:
        current = self._reservations[reservation_id]
        self._reservations[reservation_id] = replace(current, status=Reservation.CANCELLED)

    def by_passenger(self, passenger_id: int) -> list[Reservation]:
        return [r for r in self._reservations.values() if r.passenger_id == passenger_id]


class FakeTransactionManager(TransactionManager):
    def __enter__(self) -> "FakeTransactionManager":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        pass
