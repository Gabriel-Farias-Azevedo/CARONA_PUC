import sqlite3
from dataclasses import dataclass

from infra.db.transaction import SqliteTransactionManager
from infra.repositories.sqlite_reservation_repository import SqliteReservationRepository
from infra.repositories.sqlite_ride_repository import SqliteRideRepository
from infra.repositories.sqlite_user_repository import SqliteUserRepository
from use_cases.cancel_reservation import CancelReservationUseCase
from use_cases.list_available_rides import ListAvailableRidesUseCase
from use_cases.list_reservations_by_passenger import ListReservationsByPassengerUseCase
from use_cases.list_rides_by_driver import ListRidesByDriverUseCase
from use_cases.login_user import LoginUserUseCase
from use_cases.offer_ride import OfferRideUseCase
from use_cases.register_user import RegisterUserUseCase
from use_cases.reserve_ride import ReserveRideUseCase
from use_cases.update_profile import UpdateProfileUseCase


@dataclass
class Container:
    """Raiz de composição: liga as interfaces de repositório (use_cases.repositories)
    às implementações concretas SQLite (infra) e monta os use cases prontos para
    uso pelas rotas -- Inversão de Dependência (SOLID-D) aplicada na prática.
    """

    users: SqliteUserRepository
    rides: SqliteRideRepository
    reservations: SqliteReservationRepository

    register_user: RegisterUserUseCase
    login_user: LoginUserUseCase
    update_profile: UpdateProfileUseCase
    offer_ride: OfferRideUseCase
    list_available_rides: ListAvailableRidesUseCase
    list_rides_by_driver: ListRidesByDriverUseCase
    reserve_ride: ReserveRideUseCase
    cancel_reservation: CancelReservationUseCase
    list_reservations_by_passenger: ListReservationsByPassengerUseCase

    @classmethod
    def build(cls, conn: sqlite3.Connection) -> "Container":
        users = SqliteUserRepository(conn)
        rides = SqliteRideRepository(conn)
        reservations = SqliteReservationRepository(conn)
        tx = SqliteTransactionManager(conn)

        return cls(
            users=users,
            rides=rides,
            reservations=reservations,
            register_user=RegisterUserUseCase(users),
            login_user=LoginUserUseCase(users),
            update_profile=UpdateProfileUseCase(users),
            offer_ride=OfferRideUseCase(rides),
            list_available_rides=ListAvailableRidesUseCase(rides),
            list_rides_by_driver=ListRidesByDriverUseCase(rides),
            reserve_ride=ReserveRideUseCase(rides, reservations, tx),
            cancel_reservation=CancelReservationUseCase(rides, reservations, tx),
            list_reservations_by_passenger=ListReservationsByPassengerUseCase(reservations),
        )
