from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class FailureCause(StrEnum):
    MANUFACTURING_DEFECT = "manufacturing_defect"
    WEAR_AND_TEAR = "wear_and_tear"
    EXCLUDED_MODIFICATION = "excluded_modification"
    UNRELATED_MODIFICATION = "unrelated_modification"
    UNKNOWN = "unknown"


class WarrantyClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(pattern=r"^CLM-\d{4}$")
    vin: str = Field(pattern=r"^SYNTH-VIN-\d{4}$")
    component: str = Field(min_length=1)
    repair_date: date
    reported_mileage: int = Field(ge=0)
    failure_cause: FailureCause
    repair_cost: Decimal = Field(gt=0)
    documentation_complete: bool
    aftermarket_modification: bool
