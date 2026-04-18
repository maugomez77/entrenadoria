"""JSON-file-backed store for EntrenadorIA."""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any

STORE_PATH = Path(os.environ.get("ENTRENADORIA_STORE", Path.home() / ".entrenadoria" / "store.json"))

DEFAULT_STATE: dict[str, Any] = {
    "clients": [],
    "workouts": [],
    "progress": [],
    "form_analyses": [],
    "nutrition_plans": [],
    "appointments": [],
    "messages": [],
}


def load() -> dict[str, Any]:
    if not STORE_PATH.exists():
        return json.loads(json.dumps(DEFAULT_STATE))
    try:
        data = json.loads(STORE_PATH.read_text())
    except json.JSONDecodeError:
        return json.loads(json.dumps(DEFAULT_STATE))
    for k, v in DEFAULT_STATE.items():
        data.setdefault(k, v)
    return data


def save(state: dict[str, Any]) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(state, indent=2, default=str))


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"
