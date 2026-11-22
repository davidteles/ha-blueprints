"""EV charging Live Activity: unplugging, the wall charger starting first, and the time left."""
from __future__ import annotations

import pytest

from homeassistant.core import HomeAssistant

from .conftest import settle

STATE, PLUG, CHARGER, CAR = "sensor.car_charging_state", "binary_sensor.car_plug", "sensor.wallbox_status", "device_tracker.car"
BATTERY, LIMIT, POWER, LEFT, PHASE = "sensor.car_battery", "sensor.car_limit", "sensor.car_power", "sensor.car_time_left", "input_text.car_phase"


@pytest.fixture
def start():
    """Starting states; tests override what they need."""
    return {STATE: "ready_for_charging", PLUG: "on", CHARGER: "Ready", CAR: "not_home", LEFT: ("unknown", "min")}


@pytest.fixture
async def ev(hass: HomeAssistant, load_blueprint, helpers, notify, start):
    await helpers(texts=["car_phase"])
    for entity, value in start.items():
        if entity == LEFT:
            hass.states.async_set(LEFT, value[0], {"unit_of_measurement": value[1], "device_class": "duration"})
        else:
            hass.states.async_set(entity, value)
    hass.states.async_set(BATTERY, "55", {"device_class": "battery", "unit_of_measurement": "%"})
    hass.states.async_set(LIMIT, "80")
    hass.states.async_set(POWER, "123.9")
    await load_blueprint("car/ev_charging_live_activity.yaml", {
        "charging_state": STATE, "plug": PLUG, "charger_status": CHARGER, "car_location": CAR,
        "battery": BATTERY, "limit": LIMIT, "power": POWER, "remaining_time": LEFT,
        "phase_helper": PHASE, "notify_action": "notify.phone"})
    return notify


def _cards(calls):
    return [(c.data.get("title"), c.data.get("message")) for c in calls if c.data.get("message") != "clear_notification"]


async def test_charging_card_shows_time_left_not_the_percentage_twice(hass, ev, later):
    hass.states.async_set(LEFT, "15", {"unit_of_measurement": "min", "device_class": "duration"})
    hass.states.async_set(STATE, "charging")
    await later(seconds=1)
    title, message = _cards(ev)[-1]
    assert title == "⚡ Car charging"
    assert message.startswith("15 min left · 80% at "), message
    assert "124 kW" in message, "DC power is rounded"
    assert "55% →" not in message, "the percentage is already on the card"
    assert hass.states.get(PHASE).state == "charging"


@pytest.mark.parametrize("start", [{STATE: "ready_for_charging", PLUG: "on", CHARGER: "Ready", CAR: "not_home", LEFT: ("1.5", "h")}])
async def test_time_left_in_hours(hass, ev, later):
    hass.states.async_set(STATE, "charging")
    await later(seconds=1)
    assert _cards(ev)[-1][1].startswith("1 h 30 min left"), _cards(ev)[-1][1]


async def test_no_estimate_says_charging_to_the_limit(hass, ev, later):
    hass.states.async_set(STATE, "charging")
    await later(seconds=1)
    assert _cards(ev)[-1][1].startswith("Charging to 80%")


async def test_unplugging_never_flashes_a_plugged_in_card(hass, ev, later):
    hass.states.async_set(STATE, "charging")
    await later(seconds=20)
    before = len(_cards(ev))
    # The car says "connect cable" a few seconds before its plug sensor turns off.
    hass.states.async_set(STATE, "connect_cable")
    await later(seconds=5)
    assert len(_cards(ev)) == before, f"no new card after unplugging: {_cards(ev)[before:]}"
    assert hass.states.get(PHASE).state == "none"
    assert any(c.data.get("message") == "clear_notification" for c in ev), "the charging card is closed"


@pytest.mark.parametrize("start", [{STATE: "connect_cable", PLUG: "off", CHARGER: "Ready", CAR: "unknown", LEFT: ("unknown", "min")}])
async def test_wall_charger_starts_the_card_before_the_car_reports(hass, ev, later):
    hass.states.async_set(CHARGER, "Charging")
    await later(seconds=1)
    assert _cards(ev) and _cards(ev)[-1][0] == "⚡ Car charging", _cards(ev)
    assert hass.states.get(PHASE).state == "charging"


@pytest.mark.parametrize("start", [{STATE: "charging", PLUG: "on", CHARGER: "Charging", CAR: "home", LEFT: ("30", "min")}])
async def test_charger_waiting_for_the_car_after_charging_means_charged(hass, ev, later):
    hass.states.async_set(POWER, "7.2")  # any trigger: the card starts as charging
    await later(seconds=20)
    assert hass.states.get(PHASE).state == "charging"
    hass.states.async_set(STATE, "ready_for_charging")
    hass.states.async_set(CHARGER, "Waiting for car demand")
    await later(seconds=20)
    assert hass.states.get(PHASE).state == "charged", "the car is full even before its battery % arrives"
    assert _cards(ev)[-1][0] == "✅ Car charged"


@pytest.mark.parametrize("start", [{STATE: "connect_cable", PLUG: "off", CHARGER: "Ready", CAR: "not_home", LEFT: ("unknown", "min")}])
async def test_charger_status_is_ignored_while_the_car_is_away(hass, ev, later):
    hass.states.async_set(CHARGER, "Charging")  # someone else's car on our charger, ours is away
    await settle(hass)
    await later(seconds=1)
    assert not _cards(ev)
