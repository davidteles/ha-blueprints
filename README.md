# Home Assistant blueprints

Small, well-behaved automations from a real home, each one built to stay polite with the people living there. Import them with one click and fill in your own entities.

| Blueprint | What it does | Import |
|---|---|---|
| **Motion light auto-off, with a pause timer** | Light off after no motion; a timer helper pauses it while you're busy there; after the pause it only turns off if the room is really empty | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmotion_light_off_with_pause.yaml) |
| **Pause an appliance while a window is open** | Heater / dehumidifier / AC off while the window is open; back on afterwards, only if the automation paused it | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml) |
| **Alert that clears itself** | Phone alert when a problem sensor stays on; the notification disappears when the problem is gone | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fself_clearing_alert.yaml) |

> The import buttons work once this repository is public.

## Safety

| Blueprint | What it does | Import |
|---|---|---|
| **Smoke / CO / heat alarm response** | Escape-route lights on, bedroom lights red, blinds opened part-way, spoken warning, critical phone alert. Ignores self-tests. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fsmoke_co_heat_response.yaml) |
| **Weekly safety check** | Every week: are the leak / smoke / door / motion sensors online, how are their batteries? Full report in Home Assistant's notifications, short summary on the phone. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fweekly_safety_check.yaml) |
| **Safety sensor offline** | A safety sensor offline for an hour can't warn you → message; another when it's back. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fsafety_sensor_offline.yaml) |
| **Door left open** (fridge, garage, freezer…) | Open too long → alert that turns into "closed after N min" and disappears. Optional two-step *Close* button for garage doors. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fdoor_left_open.yaml) |

## Leaving and arriving

| Blueprint | What it does | Import |
|---|---|---|
| **Leaving check — anything left open or on?** | When the last person leaves: one list of open doors/windows, garage doors and lights, with *Turn off all lights*. Silent when all is well. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fleaving_check.yaml) |
| **Light on when someone arrives after dark** | Stairs / porch light on for 15 min on arrival after sunset; left alone if someone had switched it on by hand. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Farrival_light.yaml) |

> **Leaving check tip:** cars and other devices sometimes report "window" sensors; add any you don't care about to *Ignore these*.

## Before you import

Some blueprints need a helper. Create it first under *Settings → Devices & services → Helpers*:

| Blueprint | Helper |
|---|---|
| Motion light auto-off | A **Timer** (e.g. "Entrance auto-off pause"). Add dashboard buttons that start it for 30 min / 1 h / 2 h. |
| Pause an appliance | A **Toggle** (input_boolean, e.g. "Dehumidifier paused by window") |

### Pause buttons for the motion light (dashboard YAML)

```yaml
type: grid
columns: 4
square: false
cards:
  - type: button
    name: 30 min
    icon: mdi:timer-pause-outline
    tap_action:
      action: perform-action
      perform_action: timer.start
      target: { entity_id: timer.entrance_auto_off_pause }
      data: { duration: "00:30:00" }
  # …repeat for 1 h, 2 h, 4 h; a "Resume" button calls timer.cancel
```

## Design rules these follow

- **They never fight people.** If someone takes over by hand, the automation steps back.
- **Alerts clear themselves** when they stop being true, and wait a moment before firing.
- **Nothing hidden.** Every input is described, and the logic is short enough to read.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

[MIT](LICENSE)
