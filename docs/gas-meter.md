# Gas meter with a magnet pulse sensor

Read your gas meter for a few euros, and optionally split it into **heating** and **cooking + hot water**.

## 1. Hardware

- Look at the last digit wheel of your meter: many have a small magnet or a silver/reflective spot, and a label like **1 imp = 0.01 m³**.
- Tape a **door/window contact sensor** (Zigbee, Z-Wave or Wi-Fi) so its reed switch sits right next to that digit. Turn on the hot water and watch the sensor flip as the digit passes 0.
- The magnet part of the sensor is not needed.

## 2. Helpers (Settings → Devices & services → Helpers)

| Helper | Type | Notes |
|---|---|---|
| Gas pulses | **Counter** | Step 1, no maximum. Set its value to your current meter reading ÷ 0.01 if you want the totals to match the meter. |
| Gas pulses heating *(optional)* | **Counter** | For the split |
| Gas pulses other *(optional)* | **Counter** | For the split |
| Gas energy | **Template → Sensor** | See below |

Template sensor for each counter you want in the Energy dashboard:

- **State:** `{{ (states('counter.gas_pulses') | float(0) * 0.01 * 11.2) | round(3) }}`
- **Unit:** kWh · **Device class:** Energy · **State class:** Total increasing

`0.01` is the m³ per pulse printed on your meter. `11.2` is the kWh per m³ on your gas bill (the calorific value; it varies a little by country and month).

Prefer m³? Use `{{ (states('counter.gas_pulses') | float(0) * 0.01) | round(3) }}` with unit m³, device class Gas.

## 3. Automation

Import **Gas meter reading from a magnet pulse sensor** and pick the pulse sensor and the counters. For the split, also pick what tells it the heating is running:

- a **thermostat**: it counts as heating while `hvac_action` is *heating*;
- a **binary sensor** (e.g. boiler burner on): heating while on;
- a **numeric sensor** (e.g. heating power %): heating while above 0.

## 4. Energy dashboard

Settings → Dashboards → Energy → **Add gas source** → pick the template sensor(s). With the split, add both: *heating* and *cooking + hot water*. Don't also add the total, or gas is counted twice.

## What the split shows

In a home with gas heating, cooking and hot water, a winter month is typically 80–90 % heating, while cooking + hot water stays at a few kWh a day all year. That's the number that tells you whether a better thermostat schedule or insulation is worth it.

## History from before you started (advanced)

If the total sensor already has months of history, you can estimate the split backwards: for every past hour, take the gas used while the heating was running, minus that month's usual gas for the same hour of day when the heating was off. Write the result with the `recorder.import_statistics` action. This is not automated here yet, because every home's data is different. Open an issue if you'd like to try it.
