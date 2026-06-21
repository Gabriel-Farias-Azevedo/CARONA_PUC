from datetime import datetime
from typing import Optional

from domain.ride import Ride
from use_cases.exceptions import ValidationError
from use_cases.repositories import RideRepository

MAX_SEATS = 8


class OfferRideUseCase:
    """Publica uma nova carona. Valida a entrada antes de persistir, mantendo
    a regra em um só lugar (SRP).
    """

    def __init__(self, rides: RideRepository):
        self._rides = rides

    def execute(self, driver_id: int, data: dict) -> Ride:
        origin = str(data.get("origin") or "").strip()
        destination = str(data.get("destination") or "").strip()
        departure_at = self._normalize_datetime(str(data.get("departure_at") or ""))
        seats = self._to_int(data.get("seats_total"))
        price = self._to_float(data.get("price_per_seat"))

        errors: list[str] = []
        if origin == "":
            errors.append("Informe o ponto de partida.")
        if destination == "":
            errors.append("Informe o destino.")
        if departure_at is None:
            errors.append("Informe uma data e hora válidas.")
        elif departure_at < datetime.now().strftime("%Y-%m-%d %H:%M"):
            errors.append("A data da carona deve ser no futuro.")
        if seats < 1:
            errors.append("Ofereça pelo menos 1 vaga.")
        elif seats > MAX_SEATS:
            errors.append(f"Máximo de {MAX_SEATS} vagas por carona.")
        if price < 0:
            errors.append("O valor por pessoa não pode ser negativo.")

        if errors:
            raise ValidationError(errors)

        ride = Ride(
            id=None,
            driver_id=driver_id,
            origin=origin,
            destination=destination,
            departure_at=departure_at,
            seats_total=seats,
            seats_taken=0,
            price_per_seat=price,
        )
        return self._rides.create(ride)

    @staticmethod
    def _normalize_datetime(raw: str) -> Optional[str]:
        raw = raw.strip()
        if raw == "":
            return None
        for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(raw, fmt).strftime("%Y-%m-%d %H:%M")
            except ValueError:
                continue
        return None

    @staticmethod
    def _to_int(value) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _to_float(value) -> float:
        try:
            return float(str(value).replace(",", "."))
        except (TypeError, ValueError):
            return 0.0
