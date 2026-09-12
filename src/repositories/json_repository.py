from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.models import VehicleDetails, WarrantyClaim

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "synthetic"


class RecordNotFoundError(LookupError):
    pass


def _load_records(filename: str) -> list[dict[str, Any]]:
    with (DATA_DIR / filename).open(encoding="utf-8") as source:
        return json.load(source)


class ClaimRepository:
    def get(self, claim_id: str) -> WarrantyClaim:
        for record in _load_records("claims.json"):
            if record["claim_id"] == claim_id:
                return WarrantyClaim.model_validate(record)
        raise RecordNotFoundError(f"Synthetic claim not found: {claim_id}")


class VehicleRepository:
    def get(self, vin: str) -> VehicleDetails:
        for record in _load_records("vehicles.json"):
            if record["vin"] == vin:
                return VehicleDetails.model_validate(record)
        raise RecordNotFoundError(f"Synthetic vehicle not found: {vin}")
