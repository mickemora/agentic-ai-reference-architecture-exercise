from src.models import VehicleDetails
from src.repositories.json_repository import VehicleRepository


def get_vehicle_details(vin: str) -> VehicleDetails:
    """Return one validated synthetic vehicle by VIN."""
    return VehicleRepository().get(vin)
