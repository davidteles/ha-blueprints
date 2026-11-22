"""Phone almost flat while away (backlog B6): 3→2, 4→1, repeats, leaving already low, stale, charging, re-arm."""
from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from homeassistant.core import HomeAssistant

from .conftest import settle

BAT, STATE, WHO, ALERTED = "sensor.alex_phone_battery_level", "sensor.alex_phone_battery_state", "person.alex", "input_boolean.alex_low"


@pytest.fixture
def extra():
    return ""


@pytest.fixture
async def phone(hass: HomeAssistant, load_blueprint, helpers, notify, extra):
    await helpers(booleans=["alex_low"])
    hass.states.async_set(BAT, "40", {"device_class": "battery", "unit_of_measurement": "%"})
    hass.states.async_set(STATE, "Not Charging")
    hass.states.async_set(WHO, "not_home")
    second = async_mock_service(hass, "notify", "sam_phone")
    await load_blueprint("presence/phone_battery_critical_away.yaml", {
        "battery": BAT, "battery_state": STATE, "who": WHO, "alerted": ALERTED,
        "name": "Alex's phone", "notify_action": "notify.phone", "extra_notify": extra})
    return {"owner": notify, "second": second}


async def _level(hass, value):
    hass.states.async_set(BAT, str(value), {"device_class": "battery", "unit_of_measurement": "%"})
    await hass.async_block_till_done()
    await settle(hass)


@pytest.mark.parametrize("start,low", [(3, 2), (4, 1)])
async def test_drop_to_or_below_two_alerts_once(hass, phone, start, low):
    await _level(hass, start)
    assert not phone["owner"]
    await _level(hass, low)
    assert len(phone["owner"]) == 1
    assert phone["owner"][0].data["title"] == f"🪫 Alex's phone is at {low}%"
    assert "home" not in phone["owner"][0].data["message"].lower(), "no location in the message"
    assert not phone["second"], "a second recipient is opt-in"


async def test_repeated_reports_do_not_repeat_the_alert(hass, phone):
    await _level(hass, 2)
    await _level(hass, 2.0)
    await _level(hass, 1)
    assert len(phone["owner"]) == 1


async def test_already_low_when_leaving_home(hass, phone):
    hass.states.async_set(WHO, "home")
    await _level(hass, 2)
    assert not phone["owner"], "at home: nothing"
    hass.states.async_set(WHO, "not_home")
    await hass.async_block_till_done()
    await settle(hass)
    assert len(phone["owner"]) == 1


async def test_stale_reading_is_ignored_when_leaving(hass, phone, freezer):
    hass.states.async_set(WHO, "home")
    await _level(hass, 2)
    freezer.tick(3600)  # the last report is an hour old
    hass.states.async_set(WHO, "not_home")
    await hass.async_block_till_done()
    await settle(hass)
    assert not phone["owner"]


async def test_unavailable_is_ignored(hass, phone):
    hass.states.async_set(BAT, "unavailable")
    await hass.async_block_till_done()
    await settle(hass)
    assert not phone["owner"]


async def test_charging_is_ignored(hass, phone):
    hass.states.async_set(STATE, "Charging")
    await _level(hass, 2)
    assert not phone["owner"]


async def test_recharge_re_arms(hass, phone):
    await _level(hass, 2)
    await _level(hass, 4)
    await _level(hass, 2)
    assert len(phone["owner"]) == 1, "4 % is below the re-arm level"
    await _level(hass, 5)
    await _level(hass, 2)
    assert len(phone["owner"]) == 2, "back at 5 % → the next drop alerts again"


@pytest.mark.parametrize("extra", ["notify.sam_phone"])
async def test_second_recipient_only_when_set(hass, phone):
    await _level(hass, 2)
    assert len(phone["owner"]) == 1 and len(phone["second"]) == 1
