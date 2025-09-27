from pathlib import Path
import json
from typing import Dict, Optional
from pydantic import BaseModel

# Path to the static database file
DATA_PATH = Path(__file__).parent / "catchments.json"

# Schema for a catchment record
class Catchment(BaseModel):
    catchment_id: str
    A_km2: float
    C: float
    Qcap_m3s: float
    k: float = 8.0   # logistic curve steepness, default 8

# Cache to avoid reloading the file every request
_cache: Dict[str, Catchment] = {}

def load_db() -> Dict[str, Catchment]:
    """
    Load the catchments.json file into a dictionary of Catchment objects.
    Only loads once, then caches in memory.
    """
    global _cache
    if not _cache:
        raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        for row in raw:
            c = Catchment(**row)
            _cache[c.catchment_id] = c
    return _cache

def get_catchment(catchment_id: str) -> Optional[Catchment]:
    """
    Get a single catchment by ID.
    Returns None if not found.
    """
    return load_db().get(catchment_id)

def list_catchments() -> Dict[str, Catchment]:
    """
    Get all catchments as a dictionary.
    """
    return load_db()

