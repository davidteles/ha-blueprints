"""Scenario tests for the three 'Start here' blueprints.

Each one covers the normal run plus the cases that make it different:
manual override, unavailable input, duplicate events and a restart where
state must survive.
"""
from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from homeassistant.core import HomeAssistant

# ---------------------------------------------------------------- 1. window pause

WINDOW, APPLIANCE, FLAG = "binary_sensor.bedroom_window", "switch.dehumidifier", "input_boolean.paused_by_window"


@pytest.fixture
async def window_pause(hass: HomeAssistant, load_blueprint, helpers):
    await helpers(booleans=["paused_by_window"])
    hass.states.async_set(WINDOW, "off")
    hass.states.async_set(APPLIANCE, "on")
    calls = {"off": async_mock_service(hass, "switch", "turn_off"), "on": async_mock_service(hass, "switch", "turn_on")}
    await load_blueprint("pause_appliance_while_window_open.yaml",
                         {"window": WINDOW, "appliance": APPLIANCE, "paused_flag": FLAG})
    return calls


async def _device_follows(hass, calls, want: str) -> None:
    """The fake appliance obeys the last command it got."""
    hass.states.async_set(APPLIANCE, want)
    await hass.async_block_till_done()


async def test_window_pauses_and_resumes(hass, window_pause, later):
    hass.states.async_set(WINDOW, "on")
    await later(minutes=4)
    assert not window_pause["off"], "not before 5 minutes"
    await later(minutes=2)
    assert len(window_pause["off"]) == 1 and hass.states.get(FLAG).state == "on"
    await _device_follows(hass, window_pause, "off")

    hass.states.async_set(WINDOW, "off")
    await later(minutes=2)
    assert len(window_pause["on"]) == 1, "turned back on after the window closed"
    assert hass.states.get(FLAG).state == "off"


async def test_appliance_already_off_stays_off(hass, window_pause, later):
    hass.states.async_set(APPLIANCE, "off")
    hass.states.async_set(WINDOW, "on")
    await later(minutes=6)
    hass.states.async_set(WINDOW, "off")
    await later(minutes=2)
    assert not window_pause["off"] and not window_pause["on"], "it never paused it, so it never turns it on"


async def test_switched_on_by_hand_while_open_is_left_alone(hass, window_pause, later):
    hass.states.async_set(WINDOW, "on")
    await later(minutes=6)
    await _device_follows(hass, window_pause, "off")
    await _device_follows(hass, window_pause, "on")  # someone wants it on anyway
    assert hass.states.get(FLAG).state == "off", "the pause is handed back to the person"
    hass.states.async_set(WINDOW, "off")
    await later(minutes=2)
    assert len(window_pause["off"]) == 1 and not window_pause["on"], "no extra commands"


async def test_unavailable_appliance_is_not_paused(hass, window_pause, later):
    hass.states.async_set(APPLIANCE, "unavailable")
    hass.states.async_set(WINDOW, "on")
    await later(minutes=6)
    assert not window_pause["off"] and hass.states.get(FLAG).state == "off"


async def test_short_opening_does_nothing(hass, window_pause, later):
    hass.states.async_set(WINDOW, "on")
    await later(minutes=2)
    hass.states.async_set(WINDOW, "off")
    await later(minutes=6)
    assert not window_pause["off"] and not window_pause["on"]


# ---------------------------------------------------------------- 2. laundry

MACHINE, WAITING = "sensor.washer_job_state", "input_boolean.laundry_waiting"


@pytest.fixture
async def laundry(hass: HomeAssistant, load_blueprint, helpers, notify):
    await helpers(booleans=["laundry_waiting"], datetimes=["washer_finished_at"])
    hass.states.async_set(MACHINE, "wash")
    await load_blueprint("laundry/laundry_done_until_emptied.yaml", {
        "machine_state": MACHINE, "waiting": WAITING, "finished_at": "input_datetime.washer_finished_at",
        "notify_action": "notify.phone"})
    return notify


def _sent(notify) -> list[str]:
    return [c.data.get("message", "") for c in notify]


async def test_laundry_finished_then_done(hass, laundry):
    hass.states.async_set(MACHINE, "finish")
    await hass.async_block_till_done()
    assert hass.states.get(WAITING).state == "on"
    assert len(laundry) == 1 and laundry[0].data["data"]["tag"] == "laundry"

    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_DONE"})
    # The toggle turning off starts a second run of the same automation (the
    # "turned off anywhere" branch), which clears the phone a moment later.
    for _ in range(3):
        await hass.async_block_till_done()
    assert hass.states.get(WAITING).state == "off"
    assert _sent(laundry)[-1] == "clear_notification", "the phone notification is removed too"


async def test_laundry_attribute_updates_dont_repeat_the_alert(hass, laundry):
    hass.states.async_set(MACHINE, "finish", {"remaining": 0})
    await hass.async_block_till_done()
    hass.states.async_set(MACHINE, "finish", {"remaining": 0, "updated": "again"})  # attribute-only change
    await hass.async_block_till_done()
    assert len(laundry) == 1


async def test_laundry_unavailable_blip_doesnt_repeat_the_alert(hass, laundry):
    hass.states.async_set(MACHINE, "finish")
    await hass.async_block_till_done()
    hass.states.async_set(MACHINE, "unavailable")
    await hass.async_block_till_done()
    hass.states.async_set(MACHINE, "finish")  # the cloud comes back
    await hass.async_block_till_done()
    assert len(laundry) == 1


async def test_laundry_next_cycle_clears_it(hass, laundry):
    hass.states.async_set(MACHINE, "finish")
    await hass.async_block_till_done()
    hass.states.async_set(MACHINE, "weight_sensing")
    await hass.async_block_till_done()
    assert hass.states.get(WAITING).state == "off"


async def test_laundry_turned_off_on_a_dashboard_clears_the_phone(hass, laundry):
    hass.states.async_set(MACHINE, "finish")
    await hass.async_block_till_done()
    await hass.services.async_call("input_boolean", "turn_off", {"entity_id": WAITING}, blocking=True)
    await hass.async_block_till_done()
    assert _sent(laundry)[-1] == "clear_notification"


async def test_laundry_remind_me_later(hass, laundry, later):
    hass.states.async_set(MACHINE, "finish")
    await hass.async_block_till_done()
    hass.bus.async_fire("mobile_app_notification_action", {"action": "LAUNDRY_SNOOZE"})
    await later(minutes=31)
    await later(seconds=1)
    assert len(laundry) == 2 and "still waiting" in laundry[-1].data["title"]


# ---------------------------------------------------------------- 3. EV charging Live Activity

CHARGING, BATTERY, PLUG, PHASE = ("sensor.car_charging_state", "sensor.car_battery",
                                  "binary_sensor.car_plugged", "input_text.car_live_phase")


@pytest.fixture
async def ev(hass: HomeAssistant, load_blueprint, helpers, notify):
    await helpers(texts=["car_live_phase"])
    hass.states.async_set(CHARGING, "ready_for_charging")
    hass.states.async_set(BATTERY, "60", {"device_class": "battery", "unit_of_measurement": "%"})
    hass.states.async_set(PLUG, "off")
    await load_blueprint("car/ev_charging_live_activity.yaml", {
        "charging_state": CHARGING, "battery": BATTERY, "plug": PLUG, "phase_helper": PHASE,
        "name": "Car", "notify_action": "notify.phone"})
    return notify


def _cards(notify) -> list[tuple[str, str]]:
    """(tag, 'show' | 'clear') for every Live Activity message."""
    out = []
    for c in notify:
        tag = c.data.get("data", {}).get("tag")
        out.append((tag, "clear" if c.data.get("message") == "clear_notification" else "show"))
    return out


async def test_ev_plug_charge_unplug(hass, ev, later):
    hass.states.async_set(PLUG, "on")
    await later(minutes=1, seconds=5)  # the plug trigger waits 1 min
    assert _cards(ev)[-1] == ("live_car_plugged", "show")
    await later(seconds=20)

    hass.states.async_set(CHARGING, "charging")
    await later(seconds=20)
    assert ("live_car_plugged", "clear") in _cards(ev)
    assert _cards(ev)[-1] == ("live_car_charging", "show")

    hass.states.async_set(PLUG, "off")
    hass.states.async_set(CHARGING, "ready_for_charging")
    await later(minutes=1, seconds=20)
    assert _cards(ev)[-1] == ("live_car_charging", "clear"), "closes when unplugged"
    assert hass.states.get(PHASE).state == "none"


async def test_ev_several_changes_at_once_start_one_card(hass, ev, later):
    hass.states.async_set(PLUG, "on")
    await later(minutes=1, seconds=5)
    await later(seconds=20)
    # Charging starts and the battery and power change in the same second.
    hass.states.async_set(CHARGING, "charging")
    hass.states.async_set(BATTERY, "61", {"device_class": "battery", "unit_of_measurement": "%"})
    hass.states.async_set(BATTERY, "62", {"device_class": "battery", "unit_of_measurement": "%"})
    await later(seconds=60)
    starts = [i for i, (tag, kind) in enumerate(_cards(ev)) if tag == "live_car_charging" and kind == "show"]
    clears_of_plugged = [x for x in _cards(ev) if x == ("live_car_plugged", "clear")]
    assert starts, "a charging card"
    assert len(clears_of_plugged) == 1, "the plugged card is closed once, not once per queued run"


async def test_ev_unavailable_charging_state_is_ignored(hass, ev, later):
    hass.states.async_set(CHARGING, "unavailable")
    await later(seconds=5)
    assert not ev, "a sensor dropping out sends nothing"


# ---------------------------------------------------------------- safety sensor offline

from pytest_homeassistant_custom_component.common import MockConfigEntry  # noqa: E402

from homeassistant.helpers import entity_registry as er  # noqa: E402


@pytest.fixture
async def offline(hass: HomeAssistant, load_blueprint, notify):
    """Five Zigbee sensors registered to one (fake) Zigbee integration."""
    entry = MockConfigEntry(domain="zha", title="Coordinator for alex@example.com")
    entry.add_to_hass(hass)
    reg = er.async_get(hass)
    ids = []
    for i in range(5):
        ent = reg.async_get_or_create("binary_sensor", "zha", f"leak{i}", config_entry=entry,
                                      suggested_object_id=f"leak_{i}", original_name=f"Leak {i}")
        hass.states.async_set(ent.entity_id, "off", {"friendly_name": f"Leak {i}"})
        ids.append(ent.entity_id)
    await load_blueprint("safety/safety_sensor_offline.yaml", {"sensors": ids, "notify_action": "notify.phone"})
    return ids


async def test_offline_one_zigbee_device(hass, offline, notify, later):
    hass.states.async_set(offline[0], "unavailable", {"friendly_name": "Leak 0"})
    await later(hours=1, minutes=1)
    msg, title = notify[-1].data["message"], notify[-1].data["title"]
    assert title == "⚠️ Leak 0 offline"
    assert msg.startswith("Zigbee, last heard ") and "Only this device: usually a weak Zigbee signal" in msg
    assert "example.com" not in msg + title, "never the integration's title (it can hold an e-mail)"


async def test_offline_whole_integration(hass, offline, notify, later):
    for e in offline[:4]:
        hass.states.async_set(e, "unavailable", {"friendly_name": e[-6:]})
    await later(hours=1, minutes=1)
    msgs = [c.data["message"] for c in notify]
    assert any("4 of 5 Zigbee entities are offline too" in m for m in msgs), msgs


async def test_back_online_after_a_real_outage(hass, offline, notify, later):
    hass.states.async_set(offline[0], "unavailable", {"friendly_name": "Leak 0"})
    await later(hours=1, minutes=1)
    hass.states.async_set(offline[0], "off", {"friendly_name": "Leak 0"})
    await later(seconds=1)
    assert notify[-1].data["title"] == "✅ Leak 0 back" and "(Zigbee)" in notify[-1].data["message"]


async def test_short_blip_sends_nothing(hass, offline, notify, later):
    hass.states.async_set(offline[0], "unavailable", {"friendly_name": "Leak 0"})
    await later(minutes=5)
    hass.states.async_set(offline[0], "off", {"friendly_name": "Leak 0"})
    await later(seconds=1)
    assert not notify
