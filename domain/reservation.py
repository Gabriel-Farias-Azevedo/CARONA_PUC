from dataclasses import dataclass
from typing import Optional

from domain.ride import Ride


@dataclass(frozen=True)
class Reservation:
    """Reserva de uma vaga feita por um passageiro em uma carona.
    Opcionalmente carrega a Ride associada (preenchida via JOIN) para exibição.
    """

    ACTIVE = "ativa"
    CANCELLED = "cancelada"

    id: Optional[int]
    ride_id: int
    passenger_id: int
    status: str
    created_at: str
    ride: Optional[Ride] = None

    def is_active(self) -> bool:
        return self.status == Reservation.ACTIVE
