"""Run the real blueprint files in a test Home Assistant.

`load_blueprint` copies a blueprint from this repository into the test
instance and creates an automation from it. Devices are plain states the
test sets; the services the blueprint calls are recorded, not executed, so
each test decides what the "device" does next.
"""
from __future__ import annotations

import shutil
from datetime import timedelta
from pathlib import Path

import pytest
from pytest_homeassistant_custom_component.common import async_fire_time_changed, async_mock_service

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture
async def load_blueprint(hass: HomeAssistant):
    async def _load(path: str, inputs: dict, domain: str = "automation") -> None:
        target = Path(hass.config.path("blueprints", domain, "test", Path(path).name))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / "blueprints" / domain / path, target)
        assert await async_setup_component(hass, "homeassistant", {})
        assert await async_setup_component(hass, domain, {domain: [{
            "alias": f"test {Path(path).stem}",
            "use_blueprint": {"path": f"test/{Path(path).name}", "input": inputs},
        }]})
        await hass.async_block_till_done()
        state = hass.states.get(f"{domain}.test_{Path(path).stem}")
        assert state is not None and state.state == "on", f"blueprint did not load: {state}"
    return _load


@pytest.fixture
async def helpers(hass: HomeAssistant):
    """Create input_boolean / input_text / input_datetime helpers by name."""
    async def _make(booleans=(), texts=(), datetimes=()) -> None:
        if booleans:
            assert await async_setup_component(hass, "input_boolean", {"input_boolean": {b: {} for b in booleans}})
        if texts:
            assert await async_setup_component(hass, "input_text", {"input_text": {t: {"max": 255} for t in texts}})
        if datetimes:
            assert await async_setup_component(hass, "input_datetime", {"input_datetime": {
                d: {"has_date": True, "has_time": True} for d in datetimes}})
    return _make


@pytest.fixture
def notify(hass: HomeAssistant) -> list[ServiceCall]:
    """notify.phone: every notification the blueprint sends."""
    return async_mock_service(hass, "notify", "phone")


@pytest.fixture
def later(hass: HomeAssistant):
    """Move Home Assistant's timers forward ('for:' triggers, delays) and let them run."""
    elapsed = timedelta()

    async def _later(**delta) -> None:
        nonlocal elapsed
        await hass.async_block_till_done()  # let state changes start their timers first
        elapsed += timedelta(**delta)
        async_fire_time_changed(hass, dt_util.utcnow() + elapsed)
        await hass.async_block_till_done()
    return _later
