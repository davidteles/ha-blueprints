"""Drying-rack reminder: indoors (dehumidifier on) or outside (rain warning to the phones at home)."""
from __future__ import annotations

from datetime import timedelta

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_mock_service

from homeassistant.core import HomeAssistant, SupportsResponse
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util

from .conftest import settle

WAITING, ON_RACK, ALERT = "input_boolean.laundry_waiting", "input_boolean.on_rack", "input_boolean.rain_alert"
PLACE, DEHUM, RAIN, WEATHER = "input_select.drying_place", "humidifier.dehumidifier", "sensor.rain_gauge", "weather.home"


def _phone(hass, entry, name, tracker_state):
    dev = dr.async_get(hass).async_get_or_create(config_entry_id=entry.entry_id, identifiers={("mobile_app", name)}, name=name)
    ent = er.async_get(hass).async_get_or_create("device_tracker", "mobile_app", name, device_id=dev.id, config_entry=entry)
    hass.states.async_set(ent.entity_id, tracker_state)
    return dev.id, ent.entity_id


@pytest.fixture
async def rack(hass: HomeAssistant, load_blueprint, helpers, notify):
    await helpers(booleans=["laundry_waiting", "on_rack", "rain_alert"], datetimes=["reminder_at", "hung_at"])
    assert await async_setup_component(hass, "input_select", {"input_select": {
        "drying_place": {"options": ["Not set", "Indoors", "Outside"]}}})
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    hass.states.async_set(DEHUM, "off")
    hass.states.async_set(RAIN, "0")
    hass.states.async_set(WEATHER, "cloudy")
    entry = MockConfigEntry(domain="mobile_app")
    entry.add_to_hass(hass)
    alex, alex_tracker = _phone(hass, entry, "Alex Phone", "home")
    sam, sam_tracker = _phone(hass, entry, "Sam Phone", "not_home")
    calls = {
        "alex": async_mock_service(hass, "notify", "mobile_app_alex_phone"),
        "sam": async_mock_service(hass, "notify", "mobile_app_sam_phone"),
        "dehum_on": async_mock_service(hass, "humidifier", "turn_on"),
        "forecast": [],
        "rack_notify": notify,
        "trackers": [alex_tracker, sam_tracker],
    }
    forecast = {"items": []}

    def _resp(call):
        calls["forecast"].append(call)
        return {WEATHER: {"forecast": forecast["items"]}}

    hass.services.async_register("weather", "get_forecasts", _resp, supports_response=SupportsResponse.ONLY)
    calls["set_forecast"] = lambda items: forecast.__setitem__("items", items)
    await load_blueprint("laundry/drying_rack_reminder.yaml", {
        "waiting": WAITING, "on_rack": ON_RACK, "reminder_at": "input_datetime.reminder_at",
        "hung_at": "input_datetime.hung_at", "notify_action": "notify.phone",
        "place": PLACE, "dehumidifier": DEHUM, "rain_alert": ALERT, "rain_sensor": RAIN,
        "weather": WEATHER, "phones": [alex, sam]})
    return calls


async def _hang(hass, place=None):
    if place:
        await hass.services.async_call("input_select", "select_option", {"entity_id": PLACE, "option": place}, blocking=True)
    await hass.services.async_call("input_boolean", "turn_off", {"entity_id": WAITING}, blocking=True)
    for _ in range(4):
        await hass.async_block_till_done()


def _titles(calls):
    return [c.data.get("title", c.data.get("message")) for c in calls]


async def test_hung_indoors_switches_the_dehumidifier_on(hass, rack):
    await _hang(hass, "Indoors")
    assert hass.states.get(ON_RACK).state == "on"
    assert len(rack["dehum_on"]) == 1
    assert not rack["alex"] and not rack["sam"], "an explicit choice asks nothing"


async def test_dehumidifier_already_on_is_left_alone(hass, rack):
    hass.states.async_set(DEHUM, "on", {"mode": "laundry"})
    await _hang(hass, "Indoors")
    assert not rack["dehum_on"]


async def test_hung_without_a_choice_counts_as_indoors_and_asks_who_is_home(hass, rack):
    await _hang(hass)
    assert hass.states.get(PLACE).state == "Indoors"
    assert len(rack["dehum_on"]) == 1
    assert _titles(rack["alex"]) == ["👕 Laundry hung — where is it drying?"]
    assert not rack["sam"], "Sam is away"
    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_OUTSIDE"})
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Outside"


async def test_outside_rain_soon_warns_once_then_brought_in(hass, rack, later):
    await _hang(hass, "Outside")
    assert not rack["dehum_on"] and hass.states.get(ALERT).state == "off"
    soon = dt_util.now() + timedelta(minutes=20)
    rack["set_forecast"]([{"datetime": soon.isoformat(), "condition": "rainy", "precipitation_probability": 80}])
    await later(minutes=5)
    await hass.async_block_till_done()
    assert hass.states.get(ALERT).state == "on"
    assert len(rack["alex"]) == 1 and rack["alex"][0].data["title"].startswith("☔ Rain around")
    assert rack["alex"][0].data["data"]["push"] == {"interruption-level": "time-sensitive"}
    assert not rack["sam"]
    await later(minutes=5)
    await hass.async_block_till_done()
    assert len(rack["alex"]) == 1, "warned once, not every 5 minutes"
    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_BROUGHT_IN"})
    for _ in range(6):
        await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Indoors"
    assert hass.states.get(ALERT).state == "off"
    assert len(rack["dehum_on"]) == 1
    assert "clear_notification" in _titles(rack["alex"])


async def test_rain_gauge_warns_everyone_when_nobody_is_home(hass, rack):
    for tracker in rack["trackers"]:
        hass.states.async_set(tracker, "not_home")
    await _hang(hass, "Outside")
    hass.states.async_set(RAIN, "0.4")
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(ALERT).state == "on"
    assert rack["alex"][0].data["title"] == "☔ Rain now — the laundry is outside"
    assert len(rack["sam"]) == 1


async def test_forecast_clears_stands_down(hass, rack, later):
    await _hang(hass, "Outside")
    hass.states.async_set(RAIN, "0.4")
    for _ in range(4):
        await hass.async_block_till_done()
    hass.states.async_set(RAIN, "0")
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(ALERT).state == "off"


async def test_indoors_never_checks_the_forecast(hass, rack, later):
    await _hang(hass, "Indoors")
    await later(minutes=15)
    assert not rack["forecast"]


async def test_put_away_resets_to_not_set(hass, rack):
    await _hang(hass, "Outside")
    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_RACK_DONE"})
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(ON_RACK).state == "off"
    assert hass.states.get(PLACE).state == "Not set"


async def test_without_the_new_inputs_nothing_changes(hass, load_blueprint, helpers, notify, later):
    await helpers(booleans=["laundry_waiting", "on_rack"], datetimes=["reminder_at"])
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    await load_blueprint("laundry/drying_rack_reminder.yaml", {
        "waiting": WAITING, "on_rack": ON_RACK, "reminder_at": "input_datetime.reminder_at", "notify_action": "notify.phone"})
    await _hang(hass)
    await later(minutes=10)
    assert hass.states.get(ON_RACK).state == "on"
    assert not notify


async def test_rain_later_today_does_not_warn_yet(hass, rack, later):
    await _hang(hass, "Outside")
    later_rain = dt_util.now() + timedelta(minutes=90)
    rack["set_forecast"]([{"datetime": later_rain.isoformat(), "condition": "rainy", "precipitation_probability": 90}])
    await later(minutes=5)
    await hass.async_block_till_done()
    assert hass.states.get(ALERT).state == "off" and not rack["alex"]
