from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class VehicleDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vin: str = Field(pattern=r"^SYNTH-VIN-\d{4}$")
    model_year: int = Field(ge=2000, le=2100)
    in_service_date: date
    mileage: int = Field(ge=0)
