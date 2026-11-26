"""Leaving check: which open doors/windows go on the 'left open' list.

The rule behind "Skip door/window sensors on a device that has a climate
entity" is exactly that: the sensor's device also has a climate.* entity.
These fixtures cover both ways it can be wrong, and the ways out:

| fixture                                   | default | listed when            |
|-------------------------------------------|---------|------------------------|
| plain window contact                      | listed  | always                 |
| thermostat's guessed "open window"        | skipped | option off             |
| car door, car has a climate entity        | skipped | option off             |
| car door, car has no climate entity       | LISTED  | (use the ignore label) |
| real contact on a hub with a thermostat   | SKIPPED | "Always list these"    |
| sensor with the ignore label              | skipped | never (ignore wins)    |
| `opening` device class (a gate)           | listed  | always                 |
"""
from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er, label_registry as lr

BLUEPRINT = "presence/leaving_check.yaml"

PLAIN = ("binary_sensor.kitchen_window", "window", "Kitchen Window")
THERMOSTAT = ("binary_sensor.hall_thermostat_open_window", "window", "Hall Thermostat Window")
CAR_WITH_CLIMATE = ("binary_sensor.car_door", "door", "Car Door")
CAR_NO_CLIMATE = ("binary_sensor.old_car_door", "door", "Old Car Door")
HUB_CONTACT = ("binary_sensor.hub_bedroom_window", "window", "Bedroom Window")
LABELLED = ("binary_sensor.fridge_door", "door", "Fridge Door")
GATE = ("binary_sensor.side_gate", "opening", "Side Gate")

DEVICES = {
    "Kitchen window sensor": [PLAIN[0]],
    "Hall thermostat": [THERMOSTAT[0], "climate.hall"],
    "Car": [CAR_WITH_CLIMATE[0], "climate.car"],
    "Old car": [CAR_NO_CLIMATE[0]],
    "Hub with thermostat": [HUB_CONTACT[0], "climate.hub"],
    "Fridge": [LABELLED[0]],
    "Gate sensor": [GATE[0]],
}
ALL = [PLAIN, THERMOSTAT, CAR_WITH_CLIMATE, CAR_NO_CLIMATE, HUB_CONTACT, LABELLED, GATE]


@pytest.fixture
async def house(hass: HomeAssistant):
    devices, entities = dr.async_get(hass), er.async_get(hass)
    label = lr.async_get(hass).async_create("Ignore")
    for name, members in DEVICES.items():
        entry = MockConfigEntry(domain="test", title=name)
        entry.add_to_hass(hass)
        dev = devices.async_get_or_create(config_entry_id=entry.entry_id, identifiers={("test", name)}, name=name)
        for entity_id in members:
            domain, object_id = entity_id.split(".")
            entities.async_get_or_create(domain, "test", object_id, suggested_object_id=object_id,
                                         config_entry=entry, device_id=dev.id)
    entities.async_update_entity(LABELLED[0], labels={label.label_id})
    hass.states.async_set("zone.home", "1")
    for climate in ("climate.hall", "climate.car", "climate.hub"):
        hass.states.async_set(climate, "heat")
    for entity_id, device_class, name in ALL:
        hass.states.async_set(entity_id, "on", {"device_class": device_class, "friendly_name": name})
    return label.label_id


async def _listed(hass, load_blueprint, notify, later, **inputs) -> set[str]:
    await load_blueprint(BLUEPRINT, {"notify_action": "notify.phone", "check_lights": False, **inputs})
    hass.states.async_set("zone.home", "0")
    await later(minutes=2)
    assert len(notify) <= 1
    return set(notify[0].data["message"].split(", ")) if notify else set()


async def test_default_rule_both_directions(hass, house, load_blueprint, notify, later):
    listed = await _listed(hass, load_blueprint, notify, later, ignore_label=house)
    assert listed == {PLAIN[2], CAR_NO_CLIMATE[2], GATE[2]}
    # The two ways the rule is wrong, kept visible on purpose:
    assert CAR_NO_CLIMATE[2] in listed, "a car without a climate entity is NOT skipped (use the ignore label)"
    assert HUB_CONTACT[2] not in listed, "a real contact on a device with a thermostat IS skipped by default"


async def test_always_list_brings_a_real_contact_back(hass, house, load_blueprint, notify, later):
    listed = await _listed(hass, load_blueprint, notify, later, ignore_label=house,
                           always_list=[HUB_CONTACT[0], LABELLED[0]])
    assert HUB_CONTACT[2] in listed, "'Always list these' overrides the climate rule"
    assert LABELLED[2] not in listed, "the ignore label still wins over 'Always list these'"
    assert THERMOSTAT[2] not in listed and CAR_WITH_CLIMATE[2] not in listed


async def test_option_off_lists_everything_except_ignored(hass, house, load_blueprint, notify, later):
    listed = await _listed(hass, load_blueprint, notify, later, ignore_label=house, skip_climate_devices=False)
    assert listed == {name for _, _, name in ALL} - {LABELLED[2]}


async def test_only_skipped_sensors_open_sends_nothing(hass, house, load_blueprint, notify, later):
    for entity_id, device_class, name in (PLAIN, CAR_NO_CLIMATE, HUB_CONTACT, GATE, LABELLED):
        hass.states.async_set(entity_id, "off", {"device_class": device_class, "friendly_name": name})
    assert await _listed(hass, load_blueprint, notify, later, ignore_label=house) == set()
