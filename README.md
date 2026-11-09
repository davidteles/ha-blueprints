# Home Assistant blueprints

Small, well-behaved automations from a real home, each one built to stay polite with the people living there. Import them with one click and fill in your own entities.

| Blueprint | What it does | Import |
|---|---|---|
| **Motion light auto-off, with a pause timer** | Light off after no motion; a timer helper pauses it while you're busy there; after the pause it only turns off if the room is really empty | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmotion_light_off_with_pause.yaml) |
| **Pause an appliance while a window is open** | Heater / dehumidifier / AC off while the window is open; back on afterwards, only if the automation paused it | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml) |
| **Alert that clears itself** | Phone alert when a problem sensor stays on; the notification disappears when the problem is gone | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fself_clearing_alert.yaml) |

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

## Live Activities (iPhone lock screen)

> **Needs an iPhone with Live Activities turned on** — iOS 17.2 or later and the Home Assistant app 2026.x. Turn them on in two places: on the iPhone, **Settings → Home Assistant → Live Activities**, and in the Home Assistant app, **Settings → Live Activities** (accept the one-time notice). Without that, nothing is shown. Each blueprint also needs a **Text helper** (max 20) to remember its phase.

| Blueprint | What it does | Import |
|---|---|---|
| **Appliance Live Activity** (washer, dryer, dishwasher) | ⏰ *Programmed* with the finish time → stage, progress bar and "50 min left · done around 15:30" → ✅ *done* with reminders, closing by itself when it's emptied (or after a while). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fappliance_live_activity.yaml) |
| **EV charging Live Activity** | 🔌 *Plugged in, waiting* → ⚡ battery %, power and range → ✅ *charged* (alerts once, quietly at night). Closes when you unplug. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_live_activity.yaml) |
| **Robot vacuum Live Activity** | 🧹 m², minutes and battery while it cleans (⚠️ when it needs help) → ✅ *finished*, closing by itself. Learns how big each job is, then shows a progress bar and the time left. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcleaning%2Frobot_vacuum_live_activity.yaml) |

Each phase is its own Live Activity, so a long delayed start or a long wait for cheap hours can't hit the 8-hour iOS limit.

## Shopping

| Blueprint | What it does | Import |
|---|---|---|
| **"Buy again" ranked by what you really buy** | Counts every item ever on your list and keeps your top items (✓ = already on the list) in a Text helper for dashboard buttons. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fshopping%2Fbuy_again_ranking.yaml) |
| **Add an item without duplicates** *(script)* | Adds by name, or by buy-again position (`slot: 1`). A ticked-off item is reopened instead of added twice. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fshopping%2Fadd_buy_again_item.yaml) |
| **Shopping list by voice** | "We need milk", "put bread on the list", "what's on the shopping list?" (reads it back). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fshopping%2Fshopping_by_voice.yaml) |

Buy-again buttons for a dashboard (one per position; repeat for 2, 3…):

```yaml
type: custom:mushroom-template-card   # or a plain button card
primary: "{{ (states('input_text.buy_again').split('|')[0] | default('')) | replace('✓', '') }}"
icon: "{{ 'mdi:check' if states('input_text.buy_again').split('|')[0].startswith('✓') else 'mdi:cart-plus' }}"
tap_action:
  action: perform-action
  perform_action: script.shopping_add_item   # the script you made from the blueprint
  data: { slot: 1 }
```

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
| **Forgotten phone — ask before arming** | Someone left, another phone still says *home*, but nothing moves → whoever is away is asked *Arm the alarm* / *Someone's home*. Never arms by itself; ignores phone-app reload blips. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fforgotten_phone_ask_to_arm.yaml) |

> **Leaving check tip:** cars and other devices sometimes report "window" sensors; add any you don't care about to *Ignore these*.

## Comfort

| Blueprint | What it does | Import |
|---|---|---|
| **Keep rooms cool on hot afternoons** | Hot and nobody home → sunny-side blinds part-way down (plants keep their light); open again when the sun moves on or someone comes home. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcomfort%2Fkeep_rooms_cool.yaml) |
| **"Close the windows"** | Warmer outside than in while it's already warm, or colder outside while it's already cool → reminder. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcomfort%2Fclose_windows_reminder.yaml) |

## Energy

| Blueprint | What it does | Import |
|---|---|---|
| **Always-on power (night standby)** | Each morning stores the house's lowest night-time draw — what never switches off. Leaves out minutes when the car was charging. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fenergy%2Fnight_standby_baseline.yaml) |
| **Monthly home energy summary** | On the 1st: last month's electricity and gas, cost and change vs the month before, from long-term statistics. Short push, full report in notifications. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fenergy%2Fmonthly_energy_summary.yaml) |

## Lights and buttons

| Blueprint | What it does | Import |
|---|---|---|
| **Shower detection turns the bathroom light on** | Mirror light on and humidity rising fast → main light on. Uses a Derivative helper. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flights%2Fshower_light.yaml) |
| **One button, several jobs** | Single / double / triple / long press each do something different. Works with any event-entity button; press names are configurable. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fbuttons%2Fone_button_several_jobs.yaml) |

## Housekeeping

| Blueprint | What it does | Import |
|---|---|---|
| **Reload a cloud integration that has gone mostly offline** | Every 30 min: an integration with most entities unavailable for 30+ min is reloaded, and you're told if it came back. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Freload_unavailable_integration.yaml) |
| **Restart a smart bulb that dropped offline** | Power-cycles the relay behind a Wi-Fi bulb that went unavailable, then switches the bulb off again. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Frestart_offline_bulb.yaml) |
| **Pause heavy apps while a backup runs** | Stops the apps you choose (a speech model, a media server…) just before the scheduled backup and starts them again when it's done. Safety nets if the backup hangs or Home Assistant restarts. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Fpause_apps_during_backups.yaml) |

## Gas meter

| Blueprint | What it does | Import |
|---|---|---|
| **Gas meter reading from a magnet pulse sensor** | A cheap door sensor on the meter's magnet digit → pulses → kWh for the Energy dashboard. Optional split into **heating** and **cooking + hot water**. Step-by-step in [docs/gas-meter.md](docs/gas-meter.md). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fenergy%2Fgas_meter_pulses.yaml) |

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
| Light on arrival | A **Timer** "Arrival light" |
| Buy again | A **Text** helper "Buy again", max length 255 |
| Gas meter | **Counter** helpers and a **Template** sensor — see [docs/gas-meter.md](docs/gas-meter.md) |
| Keep rooms cool | A **Toggle** "Blinds lowered for heat" |
| Night standby | A **Number** helper "Night standby power" (0–5000 W, box mode) |
| Shower detection | A **Derivative** sensor on the bathroom humidity (time unit: minutes) |

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

## A report page for the weekly safety check

Point *Open when tapped* at a dashboard view with this card, and the phone opens the same report, always up to date:

```yaml
type: markdown
content: >-
  {% set sensors = ['binary_sensor.leak_kitchen', 'binary_sensor.smoke_hallway', 'binary_sensor.front_door'] %}
  {% for e in sensors %}
  - {{ '⚠️' if states(e) in ['unavailable', 'unknown'] else '✅' }} {{ state_attr(e, 'friendly_name') }}
  {% endfor %}
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
