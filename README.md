# Home Assistant blueprints

Small, well-behaved automations from a real home, each one built to stay polite with the people living there. Import them with one click and fill in your own entities.

## Start here: three picks

New to these? Start with one of these three. Each one is a single automation, says exactly what it needs, and can be checked in a couple of minutes.

### 1. Pause an appliance while a window is open
**The problem:** the heater, dehumidifier or AC keeps running with the window open, and a simple "window closed → turn it back on" automation also turns on things you had switched off yourself.
**What's different:** it only turns the appliance back on if **it** was the one that paused it. Switch it on by hand while the window is open and it's left alone.

| You need | Changes devices? | Works with |
|---|---|---|
| A window/door sensor, the appliance (humidifier, climate, fan or switch) and a **Toggle** helper, e.g. "Dehumidifier paused by window" | **Yes**: switches the appliance off and back on | Any Home Assistant |

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml)

**Check it (about 10 min with the defaults: 5 min open, 1 min closed):**
1. Appliance **on** → open the window → after 5 min it switches **off** and the toggle turns on → close it → after 1 min it's back **on**.
2. Appliance **off** → open and close the window → it **stays off** (the automation never paused it).

### 2. Laundry done, until someone empties the machine
**The problem:** "washing done" alerts are easy to miss, and once the machine powers itself off the dashboard forgets there's wet laundry inside.
**What's different:** a "laundry waiting" toggle stays on until someone deals with it, and clears itself (notification included) when you press **Done**, start the next cycle or switch the machine on.

| You need | Changes devices? | Works with |
|---|---|---|
| The machine's state sensor (e.g. job state) and a **Toggle** helper "Laundry waiting". Optional: a power sensor and a **Date and time** helper "Washer finished at" | **No**: notification and helper only | Any Home Assistant, any phone with the companion app |

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Flaundry_done_until_emptied.yaml)

**Check it (2 min):** in *Developer tools → States*, set the machine's state sensor to `finish` → the toggle turns on and one notification arrives → press **Done** → the toggle turns off and the notification disappears. (The integration puts the real state back at its next update.)

### 3. EV charging on the iPhone lock screen
**The problem:** opening the car app just to see whether it's charging and how far it's got.
**What's different:** one Live Activity per phase (🔌 plugged in → ⚡ charging → ✅ charged), so long waits for cheap hours never hit the iPhone's 8-hour limit; it closes when you unplug.

| You need | Changes devices? | Works with |
|---|---|---|
| The car's charging-state and battery sensors and a **Text** helper (max 20), e.g. "Car live phase". Optional: plug, charge limit, power, range, wall charger status | **No**: notifications only | **iPhone only**: iOS 17.2+ and the Home Assistant app 2026.x with Live Activities on ([how](#live-activities-iphone-lock-screen)) |

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_live_activity.yaml)

**Check it (next time you charge):** plug in → 🔌 card on the lock screen → charging starts → ⚡ with battery and power → unplug → the card closes.

---

# The full collection

## General

| Blueprint | What it does | Import |
|---|---|---|
| **Motion light auto-off, with a pause timer** | Light off after no motion; a timer helper pauses it while you're busy there; after the pause it only turns off if the room is really empty | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmotion_light_off_with_pause.yaml) |
| **Pause an appliance while a window is open** | Heater / dehumidifier / AC off while the window is open; back on afterwards, only if the automation paused it | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml) |
| **Alert that clears itself** | Phone alert when a problem sensor stays on; the notification disappears when the problem is gone | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fself_clearing_alert.yaml) |

## Laundry

| Blueprint | What it does | Import |
|---|---|---|
| **Laundry done — stays "waiting" until it's emptied** | When the cycle ends, a "laundry waiting" toggle turns on and one notification arrives with *Remind me later* / *Done*. It clears when you press Done, start the next cycle, switch the machine on, or turn the toggle off on a dashboard. Optional: **Hung indoors / Hung outside / Nothing to hang** buttons with the drying advice in the title, and "the laundry is dry" after a washer-dryer cycle. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Flaundry_done_until_emptied.yaml) |
| **Drying-rack reminder** | Laundry hung in the morning → reminder that evening; later → the next evening. *Put away* button. Optional **indoors or outside**: indoors switches a dehumidifier on; outside watches the rain gauge and forecast and warns the phones at home before it rains, with an *It's indoors* button. Taken out without a choice → it waits for a person (nothing is switched on); *Not hung* puts nothing on the rack. **One load on the rack at a time:** if a new load is hung somewhere else while the earlier one is still drying, the newest answer sets the rack's place (an earlier load left outside stops being watched), so bring it in first. |
| **Laundry drying advice** | "Outside recommended · no rain forecast in the next 3 h" or "Indoors · rain likely around 15:00", from one or more hourly forecasts and a rain gauge. Advice only: a person still chooses. Unknown forecast hours never count as dry. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fdrying_advice.yaml) |
| **Laundry hung** *(script)* | One script for every laundry button on a dashboard: *Indoors*, *Outside*, *Not hung* or *Change*. One tap at a time, and only while something is pending. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Flaundry%2Flaundry_hung.yaml) | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fdrying_rack_reminder.yaml) |
| **Appliance ready but not started** | Remote start left on, but nothing started or scheduled → reminder, with an optional *Start now* button. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fappliance_ready_not_started.yaml) |

## Car

| Blueprint | What it does | Import |
|---|---|---|
| **Appointment reminders** (car inspection, service…) | Type the booked date into a helper; reminders the day before and on the day. Optional "booked" toggle for dashboards. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fappointment_reminders.yaml) |
| **Electric car not plugged in at night** | You and the car are home, battery below *your* threshold (a Number helper you can change on a dashboard), charger not connected → reminder that turns into "plugged in" and disappears. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_not_plugged_in.yaml) |
| **Charging outside the cheap hours** | Warns once if the car charges outside the cheap-tariff window (a binary sensor or Schedule helper). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_outside_cheap_hours.yaml) |
| **Charger locked with the car plugged in** | It will never charge → notification with an *Unlock* button (Face ID first). Clears however you unlock. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charger_locked_car_plugged.yaml) |
| **EV charger load balancer** | Keeps the house + charger under your supply limit by setting the charger's current. Lowers at once; raises, pauses and resumes only when there has been room for a while, so an induction hob doesn't stop and start the charger all evening. Raises and resumes only on fresh readings for the whole window; resumes only after the charger shows the new current, retrying at most 3 times. Sends a lost command again, and drops to the minimum current if a meter goes silent or the two meters stop reporting together. **A comfort tool, not a protection device:** keep your breaker and the charger's installer limit. Tested against a simulated cloud charger only; this blueprint hasn't run on a real charger yet. Needs a whole-house and a charger power meter, and a Text helper for its memory. Your own pause and resume actions (e.g. a Wallbox's *Resume schedule*). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charger_load_balancer.yaml) |
| **Charging session cost at your live price** | Adds up each session at Home Assistant's own electricity price, kWh by kWh; remembers the last session for a dashboard card. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_session_cost.yaml) |
| **Car left unlocked while you're away** | Unlocked for a few minutes while you're more than 100 m from the car → alert. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fcar_unlocked_while_away.yaml) |

## Live Activities (iPhone lock screen)

> **Needs an iPhone with Live Activities turned on** — iOS 17.2 or later and the Home Assistant app 2026.x. Turn them on in two places: on the iPhone, **Settings → Home Assistant → Live Activities**, and in the Home Assistant app, **Settings → Live Activities** (accept the one-time notice). Without that, nothing is shown. Each blueprint also needs a **Text helper** (max 20) to remember its phase.

| Blueprint | What it does | Import |
|---|---|---|
| **Appliance Live Activity** (washer, dryer, dishwasher) | 🧺 *Ready* while remote start is on (optional) → ⏰ *programmed* with the finish time → stage, progress bar and "50 min left · done around 15:30" → ✅ *done* with reminders, closing on every phone when you press an optional *emptied* button or turn off a *laundry waiting* toggle (or after a while). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flaundry%2Fappliance_live_activity.yaml) |
| **EV charging Live Activity** | 🔌 *Plugged in, waiting* → ⚡ battery %, power and range → ✅ *charged* (alerts once, quietly at night). Closes when you unplug — at once if your wall charger reports it. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcar%2Fev_charging_live_activity.yaml) |
| **Robot vacuum Live Activity** | 🧹 m², minutes and battery while it cleans (⚠️ with what's wrong when it needs help) → ✅ *finished*, closing by itself — and after an hour stuck. Learns how big each job is, then shows a progress bar and the time left. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fcleaning%2Frobot_vacuum_live_activity.yaml) |

Each phase is its own Live Activity, so a long delayed start or a long wait for cheap hours can't hit the 8-hour iOS limit.

Live Activities can't have buttons (an iOS app limit): tapping one opens the page you set. For buttons on the lock screen or Home Screen, use a widget:

| Blueprint | What it does | Import |
|---|---|---|
| **Robot vacuum — pause or continue** *(script)* | One button: pauses the robot while it cleans, continues when it's paused or stuck. Put it in an iPhone widget or behind a notification button. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fcleaning%2Fvacuum_pause_or_continue.yaml) |
| **Refresh iPhone widgets when something changes** | Sends the silent *update_widgets* command when the entities in your widget change, at most every 5 minutes (iOS allows ~40–70 reloads a day). Step-by-step widget guide, with a car widget example: [docs/iphone-widgets.md](docs/iphone-widgets.md). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Frefresh_iphone_widgets.yaml) |

## Shopping

| Blueprint | What it does | Import |
|---|---|---|
| **"Buy again" ranked by what you really buy** | Counts every item ever on your list and keeps your top items (✓ = already on the list) in a Text helper for dashboard buttons. Waits quietly while a cloud list is down. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fshopping%2Fbuy_again_ranking.yaml) |
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

> These add to your smoke, CO and leak alarms and to a monitored alarm system. They don't replace them: a blueprint can only act while Home Assistant, your network and the sensors are working.

| Blueprint | What it does | Import |
|---|---|---|
| **Smoke / CO / heat alarm response** | Escape-route lights on, bedroom lights red, blinds opened part-way, spoken warning, critical phone alert. Ignores self-tests. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fsmoke_co_heat_response.yaml) |
| **Weekly safety check** | Every week: are the leak / smoke / door / motion sensors online, how are their batteries? Full report in Home Assistant's notifications, short summary on the phone. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fweekly_safety_check.yaml) |
| **Safety sensor offline** | A safety sensor offline for an hour can't warn you → message; another when it's back. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fsafety_sensor_offline.yaml) |
| **Weather warning push** | Any warning-level sensor (green / yellow / orange / red): a notification for the levels you pick, updated when the level changes and removed when it's over. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fweather_warning_push.yaml) |
| **Door left open** (fridge, garage, freezer…) | Open too long → alert that turns into "closed after N min" and disappears. Optional two-step *Close* button for garage doors. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsafety%2Fdoor_left_open.yaml) |

## Leaving and arriving

| Blueprint | What it does | Import |
|---|---|---|
| **Leaving check — anything left open or on?** | When the last person leaves: one list of open doors/windows, garage doors and lights, with *Turn off all lights*. Silent when all is well. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fleaving_check.yaml) |
| **Light on when someone arrives after dark** | Stairs / porch light on for 15 min on arrival after sunset; left alone if someone had switched it on by hand. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Farrival_light.yaml) |
| **Forgotten phone — ask before arming** | Someone left, another phone still says *home*, but nothing moves → whoever is away is asked *Arm the alarm* / *Someone's home*. Never arms by itself; ignores phone-app reload blips. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fforgotten_phone_ask_to_arm.yaml) |
| **Phone almost flat while away** | A phone away from home reports 2 % or less → one quiet heads-up to its owner (a second recipient only if you add one). Re-arms after charging; skips stale, unavailable and charging readings; no location in the message. Best effort: phones don't always report every %. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpresence%2Fphone_battery_critical_away.yaml) |

> **Leaving check tip:** with *Skip door/window sensors on a device that has a climate entity* on (the default), a door, window or opening sensor is left out when its device also has a `climate.*` entity. That hides a thermostat's guessed "open window" (tado, Netatmo valves) and a car's doors when the car has a climate entity. It does not hide a car without one (give it the ignore label), and it would hide a real contact wired into a thermostat or hub with a climate entity: add those to *Always list these*. *Ignore these* and the ignore label always win.

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

## Sports

| Blueprint | What it does | Import |
|---|---|---|
| **Team Tracker match memory** | Saves when your team's last match ended and who scored the last goal (and when), from a [Team Tracker](https://github.com/vasqued2/ha-teamtracker) sensor. Restarts and the next match never count as a goal; a goal taken back clears it. Template helpers for "show the match from 30 min before until 1 h after" and "GOAL for 5 minutes" are in [docs/team-tracker.md](docs/team-tracker.md). | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsports%2Fteam_tracker_match_memory.yaml) |

## Lights and buttons

| Blueprint | What it does | Import |
|---|---|---|
| **Shower detection turns the bathroom light on** | Mirror light on and humidity rising fast → main light on. Uses a Derivative helper. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Flights%2Fshower_light.yaml) |
| **One button, several jobs** | Single / double / triple / long press each do something different. Works with any event-entity button; press names are configurable. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fbuttons%2Fone_button_several_jobs.yaml) |
| **IKEA BILRESA scroll wheel (Matter)** | The whole remote in one automation: each of the 3 channels dims its own lights with the wheel (faster turn = bigger step) and toggles them with a press; double / triple / long press per channel or on every channel. Entities are preselected for the first remote. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fbuttons%2Fikea_bilresa_scroll_wheel.yaml) |

## Housekeeping

| Blueprint | What it does | Import |
|---|---|---|
| **Reload a cloud integration that has gone mostly offline** | Every 30 min: an integration with most entities unavailable for 30+ min is reloaded, and you're told if it came back. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Freload_unavailable_integration.yaml) |
| **Reload an integration when one entity freezes or goes unavailable** | Watches one entity: when it stops reporting (values frozen) or stays unavailable, its integration is reloaded — with a cooldown, and one message the first time. | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fsystem%2Freload_when_entity_freezes.yaml) |
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
| Drying-rack reminder | A **Toggle** "Laundry on the drying rack" and a **Date and time** helper "Drying-rack reminder at". For indoors/outside: a **Dropdown** "Laundry drying place" (*Not set*, *Indoors*, *Outside*, *Not hung*) and a **Toggle** "Laundry rain alert" |
| Laundry drying advice | A **Text** helper "Laundry drying advice" (max length 255) |
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

## Remove one

Delete the automation made from it (*Settings → Automations & scenes*), then the blueprint itself under *Blueprints* and any helper you created only for it. Nothing else is left behind.

## Notifications

The newer blueprints ask for a **notification action** such as `notify.mobile_app_your_phone`. To reach several phones, make a [notify group](https://www.home-assistant.io/integrations/group/#notify-groups) and use `notify.your_group`. Buttons in notifications (*Done*, *Unlock*…) need the Home Assistant Companion app; press and hold the notification to see them.

### Laundry buttons for a dashboard

Create one script from **Laundry hung** (e.g. `script.laundry_hung`), then add buttons that call it. They show while the laundry is waiting:

```yaml
type: grid
columns: 3
square: false
cards:
  - type: button
    name: Hung indoors
    icon: mdi:home
    tap_action: { action: perform-action, perform_action: script.laundry_hung, data: { place: Indoors } }
  - type: button
    name: Hung outside
    icon: mdi:weather-sunny
    tap_action: { action: perform-action, perform_action: script.laundry_hung, data: { place: Outside } }
  - type: button
    name: Nothing to hang
    icon: mdi:close-circle-outline
    tap_action: { action: perform-action, perform_action: script.laundry_hung, data: { place: Not hung } }
visibility:
  - { condition: state, entity: input_boolean.laundry_waiting, state: "on" }
```

Once it's on the rack, a button with `place: Change` swaps indoors and outside. Show a red card while "Laundry rain alert" is on, with a tap that calls the script with `place: Indoors`.

> **Mushroom template cards:** if you give one an `entity`, also set `icon_tap_action`. Otherwise, tapping the icon toggles that entity instead of running your action.

## How these are tested

Every blueprint is imported into a real Home Assistant before it lands here, then driven with test helpers and simulated sensors through each path (finished → reminder → button → cleared, and so on), with notifications going to Home Assistant's own notification list.

The three starter picks, the offline alert, the drying-rack indoors/outside rain warning, the drying advice, the wash-done choice buttons and the laundry-hung script also have **automated scenario tests** (`pytest`, in [tests/](tests/)) that run the real blueprint files on every change: the normal run, a manual override, an unavailable sensor, a repeated event and a short blip that must stay quiet. Run them with Python 3.13: `pip install -r requirements_test.txt && pytest`. What only a phone or a real device can show stays on the manual checks above. The EV charger load balancer has its own scenario tests too (lost, late and refused commands, a resume that doesn't take, sparse, unpaired and silent meters, a restart with remembered state, kW meters and power-factor shapes), all against a **simulated** charger. For the Live Activity blueprints the tests check what is sent; what a real iPhone shows is recorded separately, by date, only after it was seen.

In daily use on Home Assistant **2026.11.2**; the automated tests run on 2026.2.

## Design rules these follow

- **They never fight people.** If someone takes over by hand, the automation steps back.
- **Alerts clear themselves** when they stop being true, and wait a moment before firing.
- **Nothing hidden.** Every input is described, and the logic is short enough to read.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

[MIT](LICENSE)
