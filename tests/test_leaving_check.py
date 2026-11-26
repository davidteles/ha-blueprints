"""Leaving check: what goes on the 'left open' list.

A thermostat's guessed "open window" (tado, Netatmo valves) and a car's
doors and windows belong to a device that also has a climate entity. They
are skipped by default, and listed again when the option is turned off.
"""
from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

BLUEPRINT = "presence/leaving_check.yaml"
REAL_WINDOW = "binary_sensor.kitchen_window"
THERMOSTAT_WINDOW = "binary_sensor.hall_thermostat_open_window"
CAR_DOOR = "binary_sensor.car_door"


def _on_device(hass: HomeAssistant, name: str, entities: list[str]) -> None:
    """Register `entities` on one device called `name`."""
    entry = MockConfigEntry(domain="test", title=name)
    entry.add_to_hass(hass)
    dev = dr.async_get(hass).async_get_or_create(config_entry_id=entry.entry_id, identifiers={("test", name)}, name=name)
    ents = er.async_get(hass)
    for entity_id in entities:
        domain, object_id = entity_id.split(".")
        ents.async_get_or_create(domain, "test", object_id, suggested_object_id=object_id,
                                 config_entry=entry, device_id=dev.id)


@pytest.fixture
async def house(hass: HomeAssistant):
    _on_device(hass, "Kitchen window sensor", [REAL_WINDOW])
    _on_device(hass, "Hall thermostat", [THERMOSTAT_WINDOW, "climate.hall"])
    _on_device(hass, "Car", [CAR_DOOR, "climate.car"])
    hass.states.async_set("zone.home", "1")
    hass.states.async_set("climate.hall", "heat")
    hass.states.async_set("climate.car", "off")
    for entity_id, name in [(REAL_WINDOW, "Kitchen Window"), (THERMOSTAT_WINDOW, "Hall Thermostat Window"),
                            (CAR_DOOR, "Car Door")]:
        dc = "door" if entity_id == CAR_DOOR else "window"
        hass.states.async_set(entity_id, "on", {"device_class": dc, "friendly_name": name})


async def _leave(hass, later) -> None:
    hass.states.async_set("zone.home", "0")
    await later(minutes=2)


async def test_thermostat_and_car_are_skipped_by_default(hass, house, load_blueprint, notify, later):
    await load_blueprint(BLUEPRINT, {"notify_action": "notify.phone", "check_lights": False})
    await _leave(hass, later)
    assert len(notify) == 1
    assert notify[0].data["message"] == "Kitchen Window"


async def test_listed_again_when_the_option_is_off(hass, house, load_blueprint, notify, later):
    await load_blueprint(BLUEPRINT, {"notify_action": "notify.phone", "check_lights": False,
                                     "skip_climate_devices": False})
    await _leave(hass, later)
    assert len(notify) == 1
    listed = notify[0].data["message"].split(", ")
    assert sorted(listed) == ["Car Door", "Hall Thermostat Window", "Kitchen Window"]


async def test_only_a_thermostat_window_sends_nothing(hass, house, load_blueprint, notify, later):
    hass.states.async_set(REAL_WINDOW, "off", {"device_class": "window", "friendly_name": "Kitchen Window"})
    await load_blueprint(BLUEPRINT, {"notify_action": "notify.phone", "check_lights": False})
    await _leave(hass, later)
    assert not notify, "nothing real is open, so nothing is sent"
