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
HOUSE_PF = "sensor.house_pf"


class Sim:
    def __init__(self, hass, later, load, *, lose=(), silent_from=None, silent_until=None, status_at=None,
                 report_every=5, skew=False, unit="W", pf=None, resume_fails=False, set_delay=5, reject=None,
                 other_controller=None):
        self.hass, self.later, self.load = hass, later, load
        self.t, self.status, self.setpoint, self.amps = 0, "Charging", CAP, float(CAP)
        self.pending: list[tuple[int, object]] = []
        self.lose, self.silent_from, self.status_at = set(lose), silent_from, status_at or {}
        self.silent_until = silent_until
        self.report_every, self.skew, self.unit, self.pf = report_every, skew, unit, pf
        self.resume_fails, self.set_delay, self.reject = resume_fails, set_delay, reject
        self.other_controller = other_controller  # (every_s, amps): someone else keeps setting the charger
        self.commands: list[tuple[int, str]] = []
        self.setpoint_at_resume: list[int] = []
        self.over_s = 0
        self.seen = {"set": 0, "off": 0, "on": 0}

    def publish(self):
        s = self.hass.states
        s.async_set(STATUS, self.status)
        s.async_set(CURRENT, str(self.setpoint), {"min": 6, "max": CAP})
        silent = self.silent_from is not None and self.t >= self.silent_from and (
            self.silent_until is None or self.t < self.silent_until)
        if not silent and self.t % self.report_every == 0:
            scale = 1000 if self.unit == "kW" else 1
            frac = 1.0 if self.pf is None else (abs(self.pf) if abs(self.pf) <= 1 else abs(self.pf) / 100)
            attrs = {"device_class": "power", "unit_of_measurement": self.unit}
            if self.pf is not None:
                s.async_set(HOUSE_PF, str(self.pf), {"device_class": "power_factor"})
            if not self.skew or self.t == 0 or (self.t // 5) % 2 == 0:
                s.async_set(HOUSE, str(round((self.load(self.t) + self.amps) * V * frac / scale, 4)), attrs)
            if not self.skew or self.t == 0 or (self.t // 5) % 2 == 1:
                s.async_set(CHARGER, str(round(self.amps * V / scale, 4)), attrs)

    def react(self, calls):
        sets, offs, ons = calls
        for c in sets[self.seen["set"]:]:
            a = int(float(c.data["value"]))
            n = len(self.commands)
            self.commands.append((self.t, f"set {a}"))
            if n in self.lose or (self.reject and self.reject(self.t)):
                continue
            def follow(a=a):
                self.setpoint = a
                if self.status == "Charging":
                    self.amps = float(min(a, CAP))
            self.pending.append((self.t + self.set_delay, follow))
        for _ in offs[self.seen["off"]:]:
            self.commands.append((self.t, "pause"))
            def pause():
                self.status, self.amps = "Paused", 0.0
            self.pending.append((self.t + 3, pause))
        for _ in ons[self.seen["on"]:]:
            self.commands.append((self.t, "resume"))
            self.setpoint_at_resume.append(self.setpoint)
            if self.resume_fails:
                continue
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
            if self.other_controller and self.t and self.t % self.other_controller[0] == 0:
                self.setpoint = self.other_controller[1]
                if self.status == "Charging":
                    self.amps = float(min(self.setpoint, CAP))
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


async def setup_balancer(hass, load_blueprint, helpers, unit="W", **extra):
    await helpers(texts=["balancer"])
    calls = (async_mock_service(hass, "number", "set_value"),
             async_mock_service(hass, "switch", "turn_off"),
             async_mock_service(hass, "switch", "turn_on"))
    hass.states.async_set(STATUS, "Charging")
    hass.states.async_set(CURRENT, str(CAP), {"min": 6, "max": CAP})
    # The meters start in the unit the test uses: a "0 W" left over from setup is a valid
    # reading, and on a slow runner the balancer could act on it before the test starts.
    hass.states.async_set(HOUSE, "0", {"device_class": "power", "unit_of_measurement": unit})
    hass.states.async_set(CHARGER, "0", {"device_class": "power", "unit_of_measurement": unit})
    await load_blueprint("car/ev_charger_load_balancer.yaml", {
        "house_power": HOUSE, "charger_power": CHARGER, "limit": LIMIT, "charger_current": CURRENT,
        "status": STATUS, "memory": MEMORY,
        "pause_actions": [{"action": "switch.turn_off", "target": {"entity_id": "switch.charger_pause"}}],
        "resume_actions": [{"action": "switch.turn_on", "target": {"entity_id": "switch.charger_pause"}}], **extra})
    return calls


@pytest.fixture
async def balancer(hass: HomeAssistant, load_blueprint, helpers):
    await helpers(texts=["balancer"])
    calls = (async_mock_service(hass, "number", "set_value"),
             async_mock_service(hass, "switch", "turn_off"),
             async_mock_service(hass, "switch", "turn_on"))
    hass.states.async_set(STATUS, "Charging")
    hass.states.async_set(CURRENT, str(CAP), {"min": 6, "max": CAP})
    hass.states.async_set(HOUSE, "0", {"device_class": "power", "unit_of_measurement": "W"})
    hass.states.async_set(CHARGER, "0", {"device_class": "power", "unit_of_measurement": "W"})
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


# --- B1: never resume on an unconfirmed current; bounded, visible retries ------

def cooking(t):
    """No room 60-200 s (pause), then a quiet house."""
    return 27.0 if 60 <= t < 200 else 3.0


async def test_resume_waits_until_the_charger_shows_the_new_current(hass, balancer, later):
    sim = Sim(hass, later, cooking, set_delay=150)   # a slow cloud: a new current shows 2.5 min later
    await sim.run(1200, balancer)
    resumes = [t for t, c in sim.commands if c == "resume"]
    assert resumes, sim.commands
    last_set = [c for t, c in sim.commands if c.startswith("set") and t < resumes[0]][-1]
    assert sim.setpoint_at_resume[0] == int(last_set.split()[1]), "resumed only once the charger showed the current"


async def test_a_current_the_charger_never_takes_never_leads_to_a_resume(hass, balancer, later):
    sim = Sim(hass, later, cooking, reject=lambda t: t >= 200)   # every command after the pause is lost
    await sim.run(1800, balancer)
    assert "resume" not in [c for _, c in sim.commands], sim.commands
    after = [c for t, c in sim.commands if t >= 200]
    assert 1 <= len(after) <= 3, f"bounded retries, then it gives up: {sim.commands}"
    assert sim.memory()["f"] == 3 and sim.memory()["p"] == 1, "remembered: paused, gave up"


async def test_a_resume_that_doesnt_take_is_retried_at_most_3_times(hass, balancer, later):
    sim = Sim(hass, later, cooking, resume_fails=True)   # the resume action is accepted but nothing happens
    await sim.run(3600, balancer)
    resumes = [t for t, c in sim.commands if c == "resume"]
    assert 1 <= len(resumes) <= 3, sim.commands
    assert sim.memory()["f"] == 3 and sim.status == "Paused"
    assert not [c for t, c in sim.commands if t > resumes[-1] + 400], "quiet after giving up"


async def test_after_a_restart_a_remembered_pending_resume_still_needs_confirmation(hass, balancer, later):
    import time
    now = int(time.time())
    seeded = {"p": 1, "pt": now - 2000, "c": now - 2000, "sp": 1, "s": 6, "b": now // 30 - 40,
              "l": [25] * 10, "lr": now - 2000, "r": 12, "rs": 0, "f": 0}
    await hass.services.async_call("input_text", "set_value", {"entity_id": MEMORY, "value": json.dumps(seeded)}, blocking=True)
    sim = Sim(hass, later, lambda t: 3.0)
    sim.status, sim.setpoint, sim.amps = "Paused", 6, 0.0
    await sim.run(900, balancer)
    resumes = [t for t, c in sim.commands if c == "resume"]
    # the remembered slots are 20 min old: it needs ~4-5 min of fresh pairs (the first slot may be partial)
    assert resumes and resumes[0] >= 240, f"old readings from before the restart don't count: {sim.commands}"
    assert sim.setpoint_at_resume[0] != 6, "the resume current was set and confirmed first"


# --- B2: no room inferred from gaps, repeats or unpaired readings --------------

async def test_sparse_readings_never_count_as_room(hass, balancer, later):
    sim = Sim(hass, later, cooking, report_every=60)   # fresh (< 2 min) but only one pair a minute
    await sim.run(1800, balancer)
    assert "pause" in [c for _, c in sim.commands]
    assert "resume" not in [c for _, c in sim.commands], f"half the slots are empty: no resume {sim.commands}"


async def test_sparse_readings_never_raise(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 15.0 if 60 <= t < 120 else 3.0, report_every=60)
    await sim.run(900, balancer)
    sets = [(t, c) for t, c in sim.commands if c.startswith("set")]
    lowered = next(t for t, c in sets if c == "set 13")
    assert not [c for t, c in sets if t > lowered and c == "set 20"], sim.commands


async def test_meters_that_never_report_together_drop_to_the_minimum(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 3.0, skew=True)   # house and charger always 5 s apart
    await sim.run(900, balancer)
    six = next(t for t, c in sim.commands if c == "set 6")
    assert 120 <= six <= 200, sim.commands
    assert not [c for t, c in sim.commands if t > six and c != "set 6"], "never raised on unpaired readings"


async def test_after_an_outage_it_raises_only_once_the_window_has_refilled(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 3.0, silent_from=200, silent_until=500)
    await sim.run(1200, balancer)
    six = next(t for t, c in sim.commands if c == "set 6")
    assert 320 <= six <= 390
    back = next(t for t, c in sim.commands if c == "set 20" and t > six)
    assert back >= 500 + 120, f"minutes of fresh pairs before raising again: {sim.commands}"


async def test_unknown_charger_status_sends_nothing(hass, balancer, later):
    sim = Sim(hass, later, cooking, status_at={300: "unavailable"})
    await sim.run(1200, balancer)
    assert not [c for t, c in sim.commands if t >= 300], sim.commands


async def test_another_controller_fighting_it_is_answered_at_most_every_2_minutes(hass, balancer, later):
    sim = Sim(hass, later, lambda t: 15.0, other_controller=(30, 16))
    await sim.run(1200, balancer)
    ours = [t for t, c in sim.commands if c == "set 13"]
    assert len(ours) <= 1 + 1200 // 120, sim.commands


@pytest.mark.parametrize("unit", ["W", "kW"])
async def test_kilowatt_meters_give_the_same_decisions(hass, balancer, later, unit):
    sim = Sim(hass, later, lambda t: 15.0 if 60 <= t < 120 else 3.0, unit=unit)
    await sim.run(400, balancer)
    assert [c for _, c in sim.commands][:3] == ["set 20", "set 13", "set 20"], sim.commands


async def test_an_unknown_power_unit_counts_as_no_reading(hass, load_blueprint, helpers, later):
    calls = await setup_balancer(hass, load_blueprint, helpers, unit="VA")
    sim = Sim(hass, later, lambda t: 3.0, unit="VA")
    await sim.run(400, calls)
    assert [c for _, c in sim.commands] == ["set 6"], sim.commands


@pytest.mark.parametrize("pf", [-50, 50, 0.5, -0.5])
async def test_power_factor_as_percent_fraction_or_negative(hass, load_blueprint, helpers, later, pf):
    calls = await setup_balancer(hass, load_blueprint, helpers, house_power_factor=HOUSE_PF)
    # real power with PF 0.5: 35 A drawn shows as half the watts; the balancer must still see 35 A
    sim = Sim(hass, later, lambda t: 15.0 if t >= 60 else 3.0, pf=pf)
    await sim.run(200, calls)
    assert "set 13" in [c for _, c in sim.commands], sim.commands
