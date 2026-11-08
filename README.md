# Home Assistant blueprints

Small, well-behaved automations from a real home, each one built to stay polite with the people living there. Import them with one click and fill in your own entities.

| Blueprint | What it does | Import |
|---|---|---|
| **Motion light auto-off, with a pause timer** | Light off after no motion; a timer helper pauses it while you're busy there; after the pause it only turns off if the room is really empty | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fmotion_light_off_with_pause.yaml) |
| **Pause an appliance while a window is open** | Heater / dehumidifier / AC off while the window is open; back on afterwards, only if the automation paused it | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fpause_appliance_while_window_open.yaml) |
| **Alert that clears itself** | Phone alert when a problem sensor stays on; the notification disappears when the problem is gone | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdavidteles%2Fha-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fself_clearing_alert.yaml) |

> The import buttons work once this repository is public.

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
