from domain.reservation import Reservation
from use_cases.exceptions import ValidationError
from use_cases.repositories import (ReservationRepository, RideRepository,
                                    TransactionManager)


class ReserveRideUseCase:
    """Reserva uma vaga numa carona. Coordena dois repositórios dentro de uma
    transação para que vaga ocupada e reserva criada andem sempre juntas --
    nunca uma sem a outra.
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

    def execute(self, ride_id: int, passenger_id: int) -> Reservation:
        ride = self._rides.find_by_id(ride_id)
        if ride is None:
            raise ValidationError(["Carona não encontrada."])
        if ride.driver_id == passenger_id:
            raise ValidationError(["Você não pode reservar a sua própria carona."])
        if self._reservations.active_reservation(ride_id, passenger_id) is not None:
            raise ValidationError(["Você já reservou esta carona."])

        with self._tx:
            if not self._rides.take_seat(ride_id):
                raise ValidationError(["Não há mais vagas nesta carona."])
            reservation = self._reservations.create(ride_id, passenger_id)

        return reservation
