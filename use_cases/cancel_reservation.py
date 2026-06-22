from use_cases.exceptions import ValidationError
from use_cases.repositories import (ReservationRepository, RideRepository,
                                    TransactionManager)


class CancelReservationUseCase:
    """Cancela uma reserva e libera a vaga correspondente. Verifica a posse
    antes de cancelar: ninguém cancela reserva alheia.
    """

    def __init__(
        self,
        rides: RideRepository,
        reservations: ReservationRepository,
        tx: TransactionManager,
    ):
        self._rides = rides
        self._reservations = reservations
        self._tx = tx

    def execute(self, reservation_id: int, passenger_id: int) -> None:
        reservation = self._reservations.find_by_id(reservation_id)

        if reservation is None or reservation.passenger_id != passenger_id:
            raise ValidationError(["Reserva não encontrada."])
        if not reservation.is_active():
            raise ValidationError(["Esta reserva já foi cancelada."])

        with self._tx:
            self._reservations.cancel(reservation_id)
            self._rides.release_seat(reservation.ride_id)
