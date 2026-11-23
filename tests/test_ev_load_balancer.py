"""EV charger load balancer: a simulated charger + house meter driven through the real blueprint.

The charger follows a new current 5 s after a command, pauses 3 s after the
pause action and resumes 12 s after the resume action, like a cloud charger.
All loads are synthetic.
"""
from __future__ import annotations

import json

import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from homeassistant.core import HomeAssistant

LIMIT, CAP, V = 28.5, 20, 230
HOUSE, CHARGER = "sensor.house_power", "sensor.charger_power"
CURRENT, STATUS, MEMORY = "number.charger_current", "sensor.charger_status", "input_text.balancer"


class Sim:
    def __init__(self, hass, later, load, *, lose=(), silent_from=None, status_at=None):
        self.hass, self.later, self.load = hass, later, load
        self.t, self.status, self.setpoint, self.amps = 0, "Charging", CAP, float(CAP)
        self.pending: list[tuple[int, object]] = []
        self.lose, self.silent_from, self.status_at = set(lose), silent_from, status_at or {}
        self.commands: list[tuple[int, str]] = []
        self.over_s = 0
        self.seen = {"set": 0, "off": 0, "on": 0}

    def publish(self):
        s = self.hass.states
        s.async_set(STATUS, self.status)
        s.async_set(CURRENT, str(self.setpoint), {"min": 6, "max": CAP})
        if self.silent_from is None or self.t < self.silent_from:
            s.async_set(HOUSE, str(round((self.load(self.t) + self.amps) * V, 1)), {"device_class": "power", "unit_of_measurement": "W"})
            s.async_set(CHARGER, str(round(self.amps * V, 1)), {"device_class": "power", "unit_of_measurement": "W"})

    def react(self, calls):
        sets, offs, ons = calls
        for c in sets[self.seen["set"]:]:
            a = int(float(c.data["value"]))
            n = len(self.commands)
            self.commands.append((self.t, f"set {a}"))
            if n in self.lose:
                continue
            def follow(a=a):
                self.setpoint = a
                if self.status == "Charging":
                    self.amps = float(min(a, CAP))
            self.pending.append((self.t + 5, follow))
        for _ in offs[self.seen["off"]:]:
            self.commands.append((self.t, "pause"))
            def pause():
                self.status, self.amps = "Paused", 0.0
            self.pending.append((self.t + 3, pause))
        for _ in ons[self.seen["on"]:]:
            self.commands.append((self.t, "resume"))
            def resume():
                self.status, self.amps = "Charging", float(min(self.setpoint, CAP))
            self.pending.append((self.t + 12, resume))
        self.seen = {"set": len(sets), "off": len(offs), "on": len(ons)}

    async def run(self, seconds, calls, step=5):
        end = self.t + seconds
        while self.t < end:
            for when, fn in sorted([p for p in self.pending if p[0] <= self.t], key=lambda p: p[0]):
                self.pending.remove((when, fn))
                fn()
            if self.t in self.status_at:
                self.status = self.status_at[self.t]
                if self.status != "Charging":
                    self.amps = 0.0
            self.publish()
            await self.later(seconds=0)
            self.react(calls)
            mem = self.hass.states.get(MEMORY).state
            assert len(mem) <= 255, "memory must fit a Text helper"
            if self.load(self.t) + self.amps > LIMIT + 0.5:
                self.over_s += step
            self.t += step
            await self.later(seconds=step)

    def memory(self):
        return json.loads(self.hass.states.get(MEMORY).state)


@pytest.fixture
async def balancer(hass: HomeAssistant, load_blueprint, helpers):
    await helpers(texts=["balancer"])
    calls = (async_mock_service(hass, "number", "set_value"),
             async_mock_service(hass, "switch", "turn_off"),
             async_mock_service(hass, "switch", "turn_on"))
    hass.states.async_set(STATUS, "Charging")
    hass.states.async_set(CURRENT, str(CAP), {"min": 6, "max": CAP})
    hass.states.async_set(HOUSE, "0", {"device_class": "power"})
    hass.states.async_set(CHARGER, "0", {"device_class": "power"})
    await load_blueprint("car/ev_charger_load_balancer.yaml", {
        "house_power": HOUSE, "charger_power": CHARGER, "limit": LIMIT, "charger_current": CURRENT,
        "status": STATUS, "memory": MEMORY,
        "pause_actions": [{"action": "switch.turn_off", "target": {"entity_id": "switch.charger_pause"}}],
        "resume_actions": [{"action": "switch.turn_on", "target": {"entity_id": "switch.charger_pause"}}]})
    return calls


def kitchen(t):
    """Something in the kitchen switching 3 <-> 25 A every 15 s between minutes 5 and 35."""
    return 25.0 if 300 <= t < 2100 and (t // 15) % 2 else 3.0


async def test_pulsing_load_does_not_start_and_stop_all_evening(hass, balancer, later):
    sim = Sim(hass, later, kitchen)
    await sim.run(2700, balancer)
    pauses = [c for c in sim.commands if c[1] == "pause"]
    resumes = [c for c in sim.commands if c[1] == "resume"]
    assert len(pauses) <= 1 and len(resumes) <= 1, sim.commands
    assert len(sim.commands) <= 10, sim.commands
    assert sim.status == "Charging" and sim.amps >= 18, "back to full power after the cooking"
    assert sim.over_s <= 30, "only the reaction time is over the limit"


async def test_lowers_at_once_and_raises_only_after_settling(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 15.0 if 60 <= t < 120 else 3.0)
    await sim.run(400, balancer)
    lowered = next(t for t, c in sim.commands if c == "set 13")
    assert 60 <= lowered <= 65
    raised = next(t for t, c in sim.commands if c == "set 20" and t > lowered)
    assert raised >= lowered + 180, "waits the settle time"


async def test_own_pause_survives_a_scheduled_status_and_resumes(hass, balancer, later):
    """22 Nov bug: the old copy forgot its pause when the charger said 'Scheduled', and never resumed."""
    sim = Sim(hass, later, lambda t: 27.0 if 60 <= t < 200 else 3.0, status_at={100: "Scheduled"})
    await sim.run(900, balancer)
    assert [c for _, c in sim.commands if c in ("pause", "resume")] == ["pause", "resume"], sim.commands
    resumed = next(t for t, c in sim.commands if c == "resume")
    paused = next(t for t, c in sim.commands if c == "pause")
    assert resumed - paused >= 300, "shortest pause"


async def test_a_lost_command_is_sent_again(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 15.0 if t >= 60 else 3.0, lose={1})  # 0 = the first sync to 20 A
    await sim.run(400, balancer)
    sends = [t for t, c in sim.commands if c == "set 13"]
    # 2 min after the command; up to 1 min more here because a flat load only re-checks on the minute timer
    assert len(sends) >= 2 and 120 <= sends[1] - sends[0] <= 185, sim.commands
    assert sim.amps == 13


async def test_a_silent_meter_drops_to_the_minimum(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 3.0, silent_from=200)
    await sim.run(500, balancer)
    six = [t for t, c in sim.commands if c == "set 6"]
    assert six and 320 <= six[0] <= 390, sim.commands


async def test_unplugging_forgets_the_pause(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 27.0 if t >= 60 else 3.0, status_at={200: "Ready"})
    await sim.run(400, balancer)
    assert ("pause" in [c for _, c in sim.commands]) and sim.memory()["p"] == 0
    assert "resume" not in [c for _, c in sim.commands]


async def test_quiet_charge_sends_nothing(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 3.0)
    await sim.run(1800, balancer)
    assert sim.commands == [(0, "set 20")], "only the first sync, nothing after"
