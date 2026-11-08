# Home Assistant blueprints

Small, well-behaved automations from a real home, each one built to stay polite with the people living there. Import them with one click and fill in your own entities.

| Blueprint | What it does | Import |
|---|---|---|
| **Motion light auto-off, with a pause timer** | Light off after no motion; a timer helper pauses it while you're busy there; after the pause it only turns off if the room is really empty | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmotion_light_off_with_pause.yaml) |
| **Pause an appliance while a window is open** | Heater / dehumidifier / AC off while the window is open; back on afterwards, only if the automation paused it | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml) |
| **Alert that clears itself** | Phone alert when a problem sensor stays on; the notification disappears when the problem is gone | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fself_clearing_alert.yaml) |

> The import buttons work once this repository is public.

## Laundry

| Blueprint | What it does | Import |
|---|---|---|
| **Laundry done — stays "waiting" until it's emptied** | When the cycle ends, a "laundry waiting" toggle turns on and one notification arrives with *Remind me later* / *Done*. It clears when you press Done, start the next cycle, switch the machine on, or turn the toggle off on a dashboard. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Flaundry_done_until_emptied.yaml) |
| **Drying-rack reminder** | Laundry hung in the morning → reminder that evening; later → the next evening. *Put away* button. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fdrying_rack_reminder.yaml) |
| **Appliance ready but not started** | Remote start left on, but nothing started or scheduled → reminder. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fappliance_ready_not_started.yaml) |

## Car

| Blueprint | What it does | Import |
|---|---|---|
| **Appointment reminders** (car inspection, service…) | Type the booked date into a helper; reminders the day before and on the day. Optional "booked" toggle for dashboards. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fappointment_reminders.yaml) |
| **Electric car not plugged in at night** | You and the car are home, battery below *your* threshold (a Number helper you can change on a dashboard), charger not connected → reminder that turns into "plugged in" and disappears. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_not_plugged_in.yaml) |
| **Charging outside the cheap hours** | Warns once if the car charges outside the cheap-tariff window (a binary sensor or Schedule helper). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_outside_cheap_hours.yaml) |
| **Charger locked with the car plugged in** | It will never charge → notification with an *Unlock* button (Face ID first). Clears however you unlock. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charger_locked_car_plugged.yaml) |
| **Charging session cost at your live price** | Adds up each session at Home Assistant's own electricity price, kWh by kWh; remembers the last session for a dashboard card. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_session_cost.yaml) |
| **Car left unlocked while you're away** | Unlocked for a few minutes while you're more than 100 m from the car → alert. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fcar_unlocked_while_away.yaml) |



## Before you import

Some blueprints need a helper. Create it first under *Settings → Devices & services → Helpers*:

| Blueprint | Helper |
|---|---|
| Motion light auto-off | A **Timer** (e.g. "Entrance auto-off pause"). Add dashboard buttons that start it for 30 min / 1 h / 2 h. |
| Pause an appliance | A **Toggle** (input_boolean, e.g. "Dehumidifier paused by window") |
| Laundry done | A **Toggle** "Laundry waiting" |
| Drying-rack reminder | A **Toggle** "Laundry on the drying rack" and a **Date and time** helper "Drying-rack reminder at" |
| Appointment reminders | A **Date and time** helper "Car inspection booked" (optional **Toggle** "Car inspection is booked") |
| Car not plugged in | A **Number** helper "Car plug-in reminder below" (5–100 %, step 5) |
| Charging session cost | A **Number** helper "Charging session cost" (box mode, step 0.001); optional **Text** helper "Last charging session" |

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

## Notifications

The newer blueprints ask for a **notification action** such as `notify.mobile_app_your_phone`. To reach several phones, make a [notify group](https://www.home-assistant.io/integrations/group/#notify-groups) and use `notify.your_group`. Buttons in notifications (*Done*, *Unlock*…) need the Home Assistant Companion app; press and hold the notification to see them.

## How these are tested

Every blueprint is imported into a real Home Assistant before it lands here, then driven with test helpers and simulated sensors through each path (finished → reminder → button → cleared, and so on), with notifications going to Home Assistant's own notification list.

## Design rules these follow

- **They never fight people.** If someone takes over by hand, the automation steps back.
- **Alerts clear themselves** when they stop being true, and wait a moment before firing.
- **Nothing hidden.** Every input is described, and the logic is short enough to read.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

[MIT](LICENSE)
