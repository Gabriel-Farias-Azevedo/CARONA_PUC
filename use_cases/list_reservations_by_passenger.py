from domain.reservation import Reservation
from use_cases.repositories import ReservationRepository


class ListReservationsByPassengerUseCase:
    """Lista as reservas (ativas e canceladas) de um passageiro."""

    def __init__(self, reservations: ReservationRepository):
        self._reservations = reservations

    def execute(self, passenger_id: int) -> list[Reservation]:
        return self._reservations.by_passenger(passenger_id)
