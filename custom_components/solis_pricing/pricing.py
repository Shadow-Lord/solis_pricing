from __future__ import annotations
from datetime import datetime, timedelta
from homeassistant.core import HomeAssistant
from homeassistant.components.recorder.history import statistics_during_period

def _today_range():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    return start, end

def _compute_deltas(stats):
    """Convert cumulative statistics into per-interval kWh deltas for today."""
    start, end = _today_range()
    entries = [e for e in stats if start <= e["start"] < end]
    deltas = []
    for i in range(1, len(entries)):
        prev = entries[i - 1].get("sum") or 0
        curr = entries[i].get("sum") or 0
        delta = curr - prev
        if 0 < delta < 5:
            deltas.append({"start": entries[i]["start"], "kwh": delta})
    return deltas

def _price_for_minute(minute: int, windows: list[dict]) -> float:
    for w in windows:
        s = w["start"]
        e = w["end"]
        p = w["price"]
        if s <= e:
            if s <= minute < e:
                return p
        else:
            if minute >= s or minute < e:
                return p
    return 0.0

def compute_import_cost(hass: HomeAssistant, entity_id: str, import_windows: list[dict]) -> float:
    start, end = _today_range()
    stats = statistics_during_period(
        hass,
        start,
        end,
        [entity_id],
        "hour",
        True,
        True,
    ).get(entity_id, [])

    deltas = _compute_deltas(stats)
    total = 0.0
    for entry in deltas:
        ts = entry["start"]
        mins = ts.hour * 60 + ts.minute
        price = _price_for_minute(mins, import_windows)
        total += entry["kwh"] * price
    return round(total, 2)

def compute_export_cost(hass: HomeAssistant, entity_id: str, export_price: float) -> float:
    start, end = _today_range()
    stats = statistics_during_period(
        hass,
        start,
        end,
        [entity_id],
        "hour",
        True,
        True,
    ).get(entity_id, [])

    deltas = _compute_deltas(stats)
    total = sum(d["kwh"] * export_price for d in deltas)
    return round(total, 2)
