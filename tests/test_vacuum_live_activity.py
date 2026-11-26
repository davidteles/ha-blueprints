"""Robot vacuum Live Activity: one card per job.

"Finished" updates the cleaning card in place (no second card that could be
left frozen on the lock screen), the card closes only when the job is over,
and cards from the older one-card-per-phase version are cleaned up.
"""
from __future__ import annotations

import pytest

from homeassistant.core import HomeAssistant

VAC, AREA, PHASE, HIDE = "vacuum.robot", "sensor.robot_area", "input_text.robot_phase", "input_boolean.robot_hide"
TAG, OLD_TAGS = "live_robot", {"live_robot_cleaning", "live_robot_done"}


@pytest.fixture
async def robot(hass: HomeAssistant, load_blueprint, helpers, notify):
    await helpers(texts=["robot_phase"], booleans=["robot_hide"])
    hass.states.async_set(VAC, "docked", {"battery_level": 100})
    hass.states.async_set(AREA, "0", {"unit_of_measurement": "m²"})
    await load_blueprint("cleaning/robot_vacuum_live_activity.yaml", {
        "vacuum": VAC, "area": AREA, "phase_helper": PHASE, "hide_switch": HIDE,
        "name": "Robot", "notify_action": "notify.phone"})
    return notify


def _cards(calls):
    return [c for c in calls if c.data.get("message") != "clear_notification"]


def _cleared(calls):
    return [c.data["data"]["tag"] for c in calls if c.data.get("message") == "clear_notification"]


async def test_one_card_from_cleaning_to_finished(hass, robot, later):
    hass.states.async_set(VAC, "cleaning", {"battery_level": 90})
    await later(seconds=20)
    hass.states.async_set(AREA, "12", {"unit_of_measurement": "m²"})
    await later(seconds=20)
    hass.states.async_set(VAC, "docked", {"battery_level": 85})
    await later(seconds=20)

    cards = _cards(robot)
    assert {c.data["data"]["tag"] for c in cards} == {TAG}, "every update uses the same card"
    assert cards[0].data["title"] == "🧹 Robot is cleaning"
    finished = cards[-1]
    assert finished.data["title"] == "✅ Robot finished"
    assert finished.data["data"]["chronometer"] is False, "the countdown stops on the finished card"
    assert TAG not in _cleared(robot), "finishing does not close the card first"
    assert hass.states.get(PHASE).state == "done"


async def test_finished_card_closes_after_the_wait(hass, robot, later):
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=20)
    hass.states.async_set(VAC, "docked")
    await later(seconds=20)
    assert TAG not in _cleared(robot)
    await later(minutes=31)
    assert TAG in _cleared(robot), "closed 30 min after finishing"
    assert hass.states.get(PHASE).state == "none"


async def test_new_clean_while_finished_is_showing_keeps_one_card(hass, robot, later):
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=20)
    hass.states.async_set(VAC, "docked")
    await later(seconds=20)
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=1)
    assert _cards(robot)[-1].data["title"] == "🧹 Robot is cleaning"
    assert {c.data["data"]["tag"] for c in _cards(robot)} == {TAG}
    assert TAG not in _cleared(robot)


async def test_stuck_closes_the_card_and_keeps_it_closed(hass, robot, later):
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=20)
    await later(minutes=61)
    assert TAG in _cleared(robot)
    assert hass.states.get(PHASE).state == "stale"
    before = len(_cards(robot))
    hass.states.async_set(VAC, "paused")
    await later(seconds=1)
    assert len(_cards(robot)) == before, "no card comes back until the robot is docked"


async def test_old_version_cards_are_closed_on_a_phase_change(hass, robot, later):
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=20)
    assert OLD_TAGS <= set(_cleared(robot)), "an upgrade mid-clean leaves no old card behind"


async def test_hide_closes_the_card_and_sends_one_note_at_the_end(hass, robot, later):
    hass.states.async_set(VAC, "cleaning")
    await later(seconds=20)
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": HIDE}, blocking=True)
    await later(seconds=1)
    assert {TAG} | OLD_TAGS <= set(_cleared(robot))
    before = len(_cards(robot))
    hass.states.async_set(VAC, "docked")
    await later(seconds=1)
    new = _cards(robot)[before:]
    assert len(new) == 1 and new[0].data["data"]["tag"] == "live_robot_hidden_done"
    assert "live_update" not in new[0].data["data"], "a normal notification, not a card"
