"""Laundry advice, the wash-done choice buttons and the 'laundry hung' script."""
from __future__ import annotations

import os
import shutil
from datetime import timedelta

import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from homeassistant.core import HomeAssistant, SupportsResponse
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util

from .conftest import REPO, settle

ADVICE, MET, LOCAL, GAUGE = "input_text.drying_advice", "weather.met", "weather.local", "sensor.rain_gauge"
MACHINE, WAITING, FINISHED, PLACE, RACK = (
    "sensor.washer_job_state", "input_boolean.laundry_waiting", "input_datetime.washer_finished_at",
    "input_select.drying_place", "input_boolean.on_rack")


def _hours(start_offset_h, values):
    """Hourly forecast items from now (rounded down to the hour), one per value dict."""
    base = dt_util.now().replace(minute=0, second=0, microsecond=0)
    return [{"datetime": (base + timedelta(hours=start_offset_h + i)).isoformat(), "condition": "cloudy", **v}
            for i, v in enumerate(values)]


@pytest.fixture
async def advice(hass: HomeAssistant, load_blueprint, helpers):
    await helpers(texts=["drying_advice"])
    hass.states.async_set(MET, "cloudy")
    hass.states.async_set(LOCAL, "cloudy")
    hass.states.async_set(GAUGE, "0")
    data = {MET: [], LOCAL: []}

    async def _handler(call):
        ids = call.data.get("entity_id") or []
        return {e: {"forecast": data.get(e, [])} for e in ids}

    hass.services.async_register("weather", "get_forecasts", _handler, supports_response=SupportsResponse.ONLY)
    await load_blueprint("laundry/drying_advice.yaml", {
        "advice": ADVICE, "forecasts": [MET, LOCAL], "rain_now": GAUGE})
    return data


async def _refresh(hass):
    hass.bus.async_fire("laundry_advice_refresh")
    for _ in range(6):
        await hass.async_block_till_done()
    return hass.states.get(ADVICE).state.split("|")


async def test_advice_dry_forecast_is_outdoors(hass, advice):
    advice[MET] = _hours(0, [{"precipitation": 0}] * 4)
    a = await _refresh(hass)
    assert a[0] == "outdoors" and a[1] == "No rain forecast in the next 3 h"
    assert a[2] == "forecast_and_local"


async def test_advice_rain_later_is_indoors_with_the_time(hass, advice):
    advice[MET] = _hours(0, [{"precipitation": 0}, {"precipitation": 0}, {"precipitation": 0.6}, {"precipitation": 0}])
    advice[LOCAL] = _hours(0, [{"precipitation_probability": 10}] * 4)
    a = await _refresh(hass)
    when = (dt_util.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)).strftime("%H:%M")
    assert a[0] == "indoors" and a[1] == f"Rain likely around {when}" and a[3] == when


async def test_advice_unknown_chances_never_count_as_dry(hass, advice):
    advice[LOCAL] = _hours(0, [{"precipitation_probability": -99}] * 4)  # IPMA's "unknown"
    a = await _refresh(hass)
    assert a[0] == "unknown" and a[2] == "insufficient"


async def test_advice_rain_gauge_wins_over_a_dry_forecast(hass, advice):
    advice[MET] = _hours(0, [{"precipitation": 0}] * 4)
    hass.states.async_set(GAUGE, "0.3")
    a = await _refresh(hass)
    assert a[0] == "indoors" and a[2] == "local_hazard"


@pytest.fixture
async def done(hass: HomeAssistant, load_blueprint, helpers, notify):
    await helpers(booleans=["laundry_waiting"], texts=["drying_advice"], datetimes=["washer_finished_at"])
    assert await async_setup_component(hass, "input_select", {"input_select": {
        "drying_place": {"options": ["Not set", "Indoors", "Outside", "Not hung"]}}})
    await hass.services.async_call("input_text", "set_value", {
        "entity_id": ADVICE, "value": "outdoors|No rain forecast in the next 3 h|forecast_only||10:00"}, blocking=True)
    refreshes = []
    hass.bus.async_listen("laundry_advice_refresh", lambda e: refreshes.append(e))
    hass.states.async_set(MACHINE, "spin")
    await load_blueprint("laundry/laundry_done_until_emptied.yaml", {
        "machine_state": MACHINE, "waiting": WAITING, "finished_at": FINISHED, "notify_action": "notify.phone",
        "place": PLACE, "advice": ADVICE})
    return {"notify": notify, "refreshes": refreshes}


async def _finish(hass, later, before="spin"):
    hass.states.async_set(MACHINE, before)
    await settle(hass)
    hass.states.async_set(MACHINE, "finish")
    await later(seconds=11)  # the advice refresh waits up to 10 s for a new value
    await hass.async_block_till_done()


async def test_wash_done_asks_where_with_the_advice(hass, done, later):
    await _finish(hass, later)
    assert done["refreshes"], "fresh advice is asked for"
    msg = done["notify"][-1].data
    assert msg["title"] == "🧺 Washing done · Outside recommended"
    load = int(hass.states.get(FINISHED).attributes["timestamp"])
    assert [a["action"] for a in msg["data"]["actions"]] == [
        f"LAUNDRY_HUNG_INDOORS_{load}", f"LAUNDRY_HUNG_OUTSIDE_{load}", f"LAUNDRY_NONE_{load}"]
    assert msg["data"]["actions"][1]["title"] == "Hung outside (recommended)"
    hass.bus.async_fire("mobile_app_notification_action", {"action": f"LAUNDRY_HUNG_OUTSIDE_{load}"})
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Outside"
    assert hass.states.get(WAITING).state == "off"
    assert done["notify"][-1].data["message"] == "clear_notification"


async def test_a_button_from_an_older_wash_is_ignored(hass, done, later):
    await _finish(hass, later)
    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_HUNG_INDOORS_1234"})
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(WAITING).state == "on" and hass.states.get(PLACE).state == "Not set"


async def test_washer_dryer_cycle_comes_out_dry(hass, done, later):
    await _finish(hass, later, before="drying")
    msg = done["notify"][-1].data
    assert msg["title"] == "✅ Wash and dry done"
    load = int(hass.states.get(FINISHED).attributes["timestamp"])
    assert msg["data"]["actions"] == [{"action": f"LAUNDRY_NONE_{load}", "title": "Taken out"}]
    hass.bus.async_fire("mobile_app_notification_action", {"action": f"LAUNDRY_NONE_{load}"})
    for _ in range(4):
        await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Not hung" and hass.states.get(WAITING).state == "off"


@pytest.fixture
async def hung_script(hass: HomeAssistant, helpers):
    await helpers(booleans=["laundry_waiting", "on_rack"])
    assert await async_setup_component(hass, "input_select", {"input_select": {
        "drying_place": {"options": ["Not set", "Indoors", "Outside", "Not hung"]}}})
    target = hass.config.path("blueprints", "script", "test", "laundry_hung.yaml")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy(REPO / "blueprints" / "script" / "laundry" / "laundry_hung.yaml", target)
    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "script", {"script": {"laundry_hung": {"use_blueprint": {
        "path": "test/laundry_hung.yaml", "input": {"waiting": WAITING, "on_rack": RACK, "place": PLACE}}}}})
    await hass.async_block_till_done()


async def _hung(hass, place):
    await hass.services.async_call("script", "laundry_hung", {"place": place}, blocking=True)
    await hass.async_block_till_done()


async def test_script_answers_while_waiting(hass, hung_script):
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    await _hung(hass, "Outside")
    assert hass.states.get(PLACE).state == "Outside" and hass.states.get(WAITING).state == "off"


async def test_script_change_swaps_on_the_rack(hass, hung_script):
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": RACK}, blocking=True)
    await hass.services.async_call("input_select", "select_option", {"entity_id": PLACE, "option": "Indoors"}, blocking=True)
    await _hung(hass, "Change")
    assert hass.states.get(PLACE).state == "Outside"
    await _hung(hass, "Change")
    assert hass.states.get(PLACE).state == "Indoors"


async def test_script_does_nothing_when_nothing_is_pending(hass, hung_script):
    await _hung(hass, "Outside")
    assert hass.states.get(PLACE).state == "Not set"



async def test_script_late_hung_tap_cannot_overwrite_an_answer(hass, hung_script):
    """The phone answered Outside; a dashboard 'Hung indoors' tap lands a moment later."""
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    await _hung(hass, "Outside")                     # the first answer (as the phone button would)
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": RACK}, blocking=True)  # rack automation
    await hass.services.async_call("script", "laundry_hung", {"place": "Indoors", "step": "hung"}, blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Outside", "a late 'hung' answer is ignored"
    await hass.services.async_call("script", "laundry_hung", {"place": "Change", "step": "move"}, blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Indoors", "a deliberate change of location still works"


async def test_script_move_does_nothing_while_still_waiting(hass, hung_script):
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    await hass.services.async_call("script", "laundry_hung", {"place": "Outside", "step": "move"}, blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(PLACE).state == "Not set" and hass.states.get(WAITING).state == "on"
