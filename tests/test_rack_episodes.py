"""Drying rack across two loads (A then B): stale phone answers, missing forecasts, Nothing to hang.

Backlog B1-B3 (week of 23 Nov 2026). Every action id is read from the notification
that was really sent, so the tests keep working if ids gain an episode suffix.
"""
from __future__ import annotations

from datetime import timedelta

from homeassistant.util import dt as dt_util

from .test_drying_place import ALERT, ON_RACK, PLACE, RAIN, WAITING, _hang, rack, rack_inputs  # noqa: F401 (fixtures)


async def _run(hass, n=6):
    for _ in range(n):
        await hass.async_block_till_done()


def _action(calls, prefix):
    """The id of the last button whose id starts with prefix, from the notifications sent."""
    ids = [a["action"] for c in calls for a in (c.data.get("data") or {}).get("actions", []) if a["action"].startswith(prefix)]
    assert ids, f"no {prefix} button was sent"
    return ids[-1]


async def _tap(hass, action):
    hass.bus.async_fire("mobile_app_notification_action", {"action": action})
    await _run(hass)


async def _put_away(hass):
    await hass.services.async_call("input_boolean", "turn_off", {"entity_id": ON_RACK}, blocking=True)
    await _run(hass)


async def _new_wash(hass):
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": WAITING}, blocking=True)
    await _run(hass)


def _rain_soon(rack):
    rack["set_forecast"]([{"datetime": (dt_util.now() + timedelta(minutes=10)).isoformat(),
                           "condition": "rainy", "precipitation_probability": 90}])


def _dry(rack):
    rack["set_forecast"]([{"datetime": (dt_util.now() + timedelta(hours=h)).isoformat(),
                           "condition": "sunny", "precipitation_probability": 0} for h in range(4)])


# ---------------------------------------------------------------- B1: old answers replayed during load B

async def test_b1_old_put_away_does_not_clear_the_next_load(hass, rack, later):
    await _hang(hass, "Outside")                       # load A
    await later(hours=30)                              # A's reminder is sent
    await _run(hass)
    old_done = _action(rack["rack_notify"], "LAUNDRY_RACK_DONE")
    await _put_away(hass)                              # A put away from the dashboard
    await _new_wash(hass)
    await _hang(hass, "Indoors")                       # load B
    await _tap(hass, old_done)                         # A's old "Put away" button
    assert hass.states.get(ON_RACK).state == "on", "B is still on the rack"
    assert hass.states.get(PLACE).state == "Indoors"


async def test_b1_old_place_answer_does_not_move_the_next_load(hass, rack, later):
    await _hang(hass)                                  # A, no choice → question
    old_outside = _action(rack["alex"], "LAUNDRY_OUTSIDE")
    await _tap(hass, _action(rack["alex"], "LAUNDRY_INDOORS"))
    await _put_away(hass)
    await later(hours=20)                              # the next load, the next day
    await _run(hass)
    await _new_wash(hass)
    await _hang(hass, "Indoors")                       # B
    await _tap(hass, old_outside)                      # A's other button, pressed late
    assert hass.states.get(PLACE).state == "Indoors", "B stays indoors"


async def test_b1_old_rain_answer_does_not_move_the_next_load(hass, rack, later):
    await _hang(hass, "Outside")                       # A
    _rain_soon(rack)
    await later(minutes=5)
    await _run(hass)
    old_in = _action(rack["alex"], "LAUNDRY_BROUGHT_IN")
    await _put_away(hass)
    await _new_wash(hass)
    _dry(rack)
    await _hang(hass, "Outside")                       # B, dry evening
    await _tap(hass, old_in)
    assert hass.states.get(PLACE).state == "Outside", "B is still outside"
    assert not rack["dehum_on"]


async def test_b1_current_answers_still_work(hass, rack, later):
    await _hang(hass, "Outside")
    _rain_soon(rack)
    await later(minutes=5)
    await _run(hass)
    await _tap(hass, _action(rack["alex"], "LAUNDRY_BROUGHT_IN"))
    assert hass.states.get(PLACE).state == "Indoors"
    await later(hours=30)
    await _run(hass)
    await _tap(hass, _action(rack["rack_notify"], "LAUNDRY_RACK_DONE"))
    assert hass.states.get(ON_RACK).state == "off"


async def test_b1_conflicting_answers_last_one_wins(hass, rack):
    await _hang(hass)
    await _tap(hass, _action(rack["alex"], "LAUNDRY_OUTSIDE"))
    await _tap(hass, _action(rack["alex"], "LAUNDRY_INDOORS"))
    assert hass.states.get(PLACE).state == "Indoors"


# ---------------------------------------------------------------- B2: a missing forecast is not an all-clear

async def test_b2_failed_or_empty_forecast_keeps_the_warning(hass, rack, later):
    await _hang(hass, "Outside")
    _rain_soon(rack)
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "on"
    rack["set_forecast"]([])                           # forecast service returns nothing
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "on", "no data is not 'dry'"
    _dry(rack)                                         # a real dry forecast
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "off"


async def test_b2_stale_warning_expires(hass, rack, later):
    await _hang(hass, "Outside")
    _rain_soon(rack)
    await later(minutes=5)
    await _run(hass)
    rack["set_forecast"]([])
    for _ in range(4):
        await later(hours=1, minutes=40)
        await _run(hass)
    assert hass.states.get(ALERT).state == "off", "a warning with no data for hours expires"


# ---------------------------------------------------------------- B3: load B finishes while A is outside

async def test_b3_nothing_to_hang_keeps_a_outside_and_watched(hass, rack, later):
    await _hang(hass, "Outside")                       # A outside
    await _new_wash(hass)                              # B finishes
    assert hass.states.get(PLACE).state == "Outside", "A's place survives B finishing"
    await hass.services.async_call("input_select", "select_option", {"entity_id": PLACE, "option": "Not hung"}, blocking=True)
    await hass.services.async_call("input_boolean", "turn_off", {"entity_id": WAITING}, blocking=True)
    await _run(hass)                                   # B: Nothing to hang
    assert hass.states.get(ON_RACK).state == "on"
    assert hass.states.get(PLACE).state == "Outside", "A is still outside"
    _rain_soon(rack)
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "on", "A's rain watch still runs"


# ---------------------------------------------------------------- B4: forecast amount without a rainy condition

async def test_b4_forecast_amount_alone_counts_as_rain(hass, rack, later):
    """Same rule as the drying advice: 0.2 mm or more is wet, whatever the condition says."""
    await _hang(hass, "Outside")
    rack["set_forecast"]([{"datetime": (dt_util.now() + timedelta(minutes=15)).isoformat(),
                           "condition": "cloudy", "precipitation": 0.6}])
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "on"


async def test_b4_a_trace_amount_is_not_rain(hass, rack, later):
    await _hang(hass, "Outside")
    rack["set_forecast"]([{"datetime": (dt_util.now() + timedelta(minutes=15)).isoformat(),
                           "condition": "cloudy", "precipitation": 0.1, "precipitation_probability": 20}])
    await later(minutes=5)
    await _run(hass)
    assert hass.states.get(ALERT).state == "off"
