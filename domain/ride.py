from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Ride:
    """Carona oferecida por um motorista. Concentra as regras simples de domínio
    sobre vagas -- manter esse cálculo na entidade evita espalhar a mesma conta
    por use cases e templates (DRY) e dá um único lugar para a regra mudar (SRP).
    """

    id: Optional[int]
    driver_id: int
    origin: str
    destination: str
    departure_at: str
    seats_total: int
    seats_taken: int
    price_per_seat: float
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None

    def seats_available(self) -> int:
        return max(0, self.seats_total - self.seats_taken)

    def has_seats(self) -> bool:
        return self.seats_available() > 0

    def is_free(self) -> bool:
        return self.price_per_seat <= 0.0
