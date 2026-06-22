"""Interfaces (portas) das quais a camada de use cases depende, sem conhecer
a infraestrutura concreta -- Inversão de Dependência (SOLID-D). Os adaptadores
em infra/repositories implementam estes contratos com SQLite.
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.reservation import Reservation
from domain.ride import Ride
from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def update(self, user: User) -> None: ...


class RideRepository(ABC):
    @abstractmethod
    def create(self, ride: Ride) -> Ride: ...

    @abstractmethod
    def find_by_id(self, ride_id: int) -> Optional[Ride]: ...

    @abstractmethod
    def available(self, search: str, exclude_driver_id: int) -> list[Ride]: ...

    @abstractmethod
    def by_driver(self, driver_id: int) -> list[Ride]: ...

    @abstractmethod
    def take_seat(self, ride_id: int) -> bool: ...

    @abstractmethod
    def release_seat(self, ride_id: int) -> None: ...


class ReservationRepository(ABC):
    @abstractmethod
    def create(self, ride_id: int, passenger_id: int) -> Reservation: ...

    @abstractmethod
    def find_by_id(self, reservation_id: int) -> Optional[Reservation]: ...

    @abstractmethod
    def active_reservation(
        self, ride_id: int, passenger_id: int
    ) -> Optional[Reservation]: ...

    @abstractmethod
    def cancel(self, reservation_id: int) -> None: ...

    @abstractmethod
    def by_passenger(self, passenger_id: int) -> list[Reservation]: ...


class TransactionManager(ABC):
    """Permite que um use case agrupe operações de mais de um repositório numa
    única transação atômica, sem depender da tecnologia de banco concreta.
    """

    @abstractmethod
    def __enter__(self) -> "TransactionManager": ...

    @abstractmethod
    def __exit__(self, exc_type, exc, tb) -> None: ...
