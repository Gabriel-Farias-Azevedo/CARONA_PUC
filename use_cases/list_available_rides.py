from domain.ride import Ride
from use_cases.repositories import RideRepository


class ListAvailableRidesUseCase:
    """Busca caronas futuras, com vaga, oferecidas por outros estudantes."""

    def __init__(self, rides: RideRepository):
        self._rides = rides

    def execute(self, viewer_id: int, search: str = "") -> list[Ride]:
        return self._rides.available(search, viewer_id)
