from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .pricing import compute_import_cost, compute_export_cost

DOMAIN = "solis_pricing"

SCAN_INTERVAL = timedelta(minutes=5)

@dataclass
class PricingConfig:
    import_entity: str
    export_entity: str
    import_windows: list[dict]
    export_price: float

def _default_config(hass: HomeAssistant) -> PricingConfig:
    # You can later move this to YAML or config entry
    return PricingConfig(
        import_entity="sensor.solis_inverter_1031040229230153_solis_daily_grid_energy_purchased",
        export_entity="sensor.solis_inverter_1031040229230153_solis_daily_on_grid_energy",
        import_windows=[
            # Example: flat rate 24h
            {"start": 0, "end": 24 * 60, "price": 0.093},  # €0.093/kWh
        ],
        export_price=0.06,  # €0.06/kWh
    )

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    cfg = _default_config(hass)
    entities = [
        SolisImportCostSensor(hass, cfg),
        SolisExportCostSensor(hass, cfg),
    ]
    add_entities(entities, True)

class SolisImportCostSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, cfg: PricingConfig):
        self._hass = hass
        self._cfg = cfg
        self._attr_name = "Solis Import Cost Today"
        self._attr_unique_id = "solis_import_cost_today"
        self._attr_native_unit_of_measurement = "€"
        self._attr_native_value = 0.0

    @property
    def should_poll(self) -> bool:
        return True

    async def async_update(self) -> None:
        cost = await self._hass.async_add_executor_job(
            compute_import_cost,
            self._hass,
            self._cfg.import_entity,
            self._cfg.import_windows,
        )
        self._attr_native_value = cost

class SolisExportCostSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, cfg: PricingConfig):
        self._hass = hass
        self._cfg = cfg
        self._attr_name = "Solis Export Cost Today"
        self._attr_unique_id = "solis_export_cost_today"
        self._attr_native_unit_of_measurement = "€"
        self._attr_native_value = 0.0

    @property
    def should_poll(self) -> bool:
        return True

    async def async_update(self) -> None:
        cost = await self._hass.async_add_executor_job(
            compute_export_cost,
            self._hass,
            self._cfg.export_entity,
            self._cfg.export_price,
        )
        self._attr_native_value = cost
