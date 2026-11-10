# iPhone widgets: a car widget, in every size

Widgets on the iPhone Home Screen and Lock Screen keep showing your car's stats when it's unplugged, unlike a Live Activity, which only lives while something is happening. This guide builds a car widget with the Home Assistant app's own widgets. The same steps work for any device.

Widgets are set up **in the iPhone app**, not in Home Assistant, so there's nothing to import for the widget itself. Home Assistant's part is to give it good entities and to tell the iPhone when they change.

**Needs:** the Home Assistant app on iOS 17 or later.

## 1. Entities that read well on a small tile

A widget tile shows one entity's name and state. Two template sensors make a car widget much easier to read. Create them in **Settings → Devices & services → Helpers → Create helper → Template → Template a sensor**. Change the entity ids to yours.

**Car status** — one line for what the car is doing:

```jinja
{%- set charging = is_state('sensor.my_car_charging_state', 'charging') -%}
{%- set plugged = is_state('binary_sensor.my_car_charger_connected', 'on') -%}
{%- set soc = states('sensor.my_car_battery') | int(0) -%}
{%- set target = states('number.my_car_charge_limit') | int(80) -%}
{%- if charging -%}⚡ Charging {{ states('sensor.my_charger_power') | float(0) | round(1) }} kW to {{ target }}%
{%- elif plugged and soc >= target - 1 -%}✅ Charged to {{ soc }}%
{%- elif plugged -%}🔌 Plugged in, waiting
{%- elif is_state('device_tracker.my_car', 'home') -%}🅿️ Parked at home
{%- else -%}🚗 Away{%- endif %}
```

**Last charge** — if you use the *Charging session cost* blueprint, its Text helper holds `kWh|km|timestamp`:

```jinja
{%- set p = states('input_text.ev_last_session').split('|') -%}
{%- if p | count == 3 and p[0] | is_number -%}
{{ p[0] | float | round(1) }} kWh · +{{ p[1] }} km · {{ as_datetime(p[2] | int) | as_local | as_timestamp | timestamp_custom('%a %H:%M') }}
{%- else -%}No charge yet{%- endif %}
```

## 2. Home Screen: a Custom widget (small, medium, large)

In the Home Assistant app: **Settings → Companion app → Widgets → Create widget**. Name it (e.g. "Car") and add items **in this order**. Smaller sizes show only the first items: small shows 3, medium 6, large 12.

| # | Item | Tap behaviour | Shown in |
|---|---|---|---|
| 1 | Car status | More info | small, medium, large |
| 2 | Battery % | More info | small, medium, large |
| 3 | Range | More info | small, medium, large |
| 4 | Door lock | Icon: *Lock*, with **Require confirmation** | medium, large |
| 5 | Air conditioning / climate | Icon: *Toggle*, with **Require confirmation** | medium, large |
| 6 | Last charge | More info | medium, large |
| 7 | Charge limit | More info | large |
| 8 | Charging power | More info | large |
| 9 | Outside temperature | More info | large |
| 10 | Windows | More info | large |
| 11 | Car location | Navigate to your car dashboard | large |
| 12 | Charger lock (if you have one) | Icon: *Toggle*, with **Require confirmation** | large |

Then, on the Home Screen: touch and hold → **Edit → Add widget → Home Assistant → Custom**. Pick the size, add it, then touch and hold it → **Edit widget** → choose "Car". Add it a second time in another size if you like.

Tip: for anything that unlocks or opens, use **Lock** rather than **Toggle** on the icon, and keep **Require confirmation** on.

## 3. Lock Screen

- **Battery ring (circular):** add the **Gauge** widget → *Entity* → your battery sensor (min 0, max 100), type *Capacity*.
- **Three lines (rectangular):** add the **Details** widget → *Template*:
  - Upper: `🚗 {{ states('sensor.my_car_battery') }}% · {{ states('sensor.my_car_range') }} km`
  - Lower: `{{ states('sensor.car_status') }}`
  - Details: `{{ states('sensor.car_last_charge') }}`

  Templates need an administrator account. Otherwise use *Entity* instead.
- **One line (inline):** the **Details** widget in the inline size shows the upper line only.

## 4. Keep it fresh

iOS refreshes widgets every 15 minutes at best. Import **Refresh iPhone widgets when something changes** and give it the same entities. It sends the app's silent `update_widgets` command when any of them changes, at most once every 5 minutes, because iOS allows only about 40–70 reloads a day.

## Buttons for the lock screen

Live Activities can't have buttons. For a *pause / continue* button for a robot vacuum, make a script from **Robot vacuum — pause or continue**. Then add it to a widget: the **Scripts** widget (circular on the Lock Screen), or a Custom widget item with *Run script*.
