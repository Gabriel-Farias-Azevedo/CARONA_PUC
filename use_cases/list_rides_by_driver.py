from domain.ride import Ride
from use_cases.repositories import RideRepository


class ListRidesByDriverUseCase:
    """Lista as caronas oferecidas por um motorista específico."""

    def __init__(self, rides: RideRepository):
        self._rides = rides

    def execute(self, driver_id: int) -> list[Ride]:
        return self._rides.by_driver(driver_id)
