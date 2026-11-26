# Changelog

All notable changes to this project. Versions follow [semantic versioning](https://semver.org/); each entry links to its full release notes on GitHub, which also say how each change was tested.

## [1.18.0] — 2026-11-26

Leaving check: the climate rule stated exactly, plus "Always list these" ([#43](https://github.com/davidteles/ha-blueprints/pull/43)).

- **The option says what it does:** *Skip door/window sensors on a device that has a climate entity*. A car without a climate entity is not skipped (use the ignore label), and a real contact on a device with a thermostat is.
- **New input "Always list these":** sensors listed even if that rule would skip them. *Ignore these* and the ignore label still win.
- Defaults are unchanged.
- Tests: one fixture house covers both directions, the include list, ignore beating it, option off and the `opening` class. A flaky EV load balancer test setup is fixed (test-only).

_Upgrading:_ re-import the leaving check. Nothing changes unless you add sensors to *Always list these*.

## [1.17.0] — 2026-11-26

Leaving check skips thermostats and cars; vacuum Live Activity keeps one card.

- **Leaving check: skip doors/windows of thermostats and cars** ([#40](https://github.com/davidteles/ha-blueprints/pull/40)).
- **Robot vacuum Live Activity: one card per job** ([#41](https://github.com/davidteles/ha-blueprints/pull/41)).

_Upgrading:_ re-import both blueprints. The leaving check skips thermostat and car sensors by default; turn the new option off if you want them listed. For the vacuum card nothing else is needed: cards left by the old version close on the next phase change.

## [1.16.0] — 2026-11-26

Team Tracker match memory: several competitions ([#39](https://github.com/davidteles/ha-blueprints/pull/39)).

_Upgrading:_ nothing to do. To follow several competitions, re-import the blueprint and add the other sensors to `team`.

## [1.15.0] — 2026-11-24

New: Team Tracker match memory.

- **New: Team Tracker match memory** ([#38](https://github.com/davidteles/ha-blueprints/pull/38)), in a new **Sports** section. It remembers what a [Team Tracker](https://github.com/vasqued2/ha-teamtracker) sensor does not keep.
- **Final whistle (IN → POST):** saves the time in a Date and time helper. A dashboard can then show the match until an hour after the end, even after a restart; `last_changed` resets on restart.
- **Goals (optional):** a score that goes up while the match stays IN saves who scored and when.
- **docs/team-tracker.md:** two template helpers that use these.

_Upgrading:_ nothing changes for existing blueprints.

## [1.14.0] — 2026-11-23

EV balancer: confirmed resume, no room from gaps.

- **EV charger load balancer: resume only on a confirmed current; no room inferred from gaps** ([#37](https://github.com/davidteles/ha-blueprints/pull/37))
- **Resumes only once the charger shows the resume current.** It sets the current first and resumes after the charger confirms it.
- **Never counts gaps or a repeated old reading as room.** Raising and resuming need a fresh pair of readings in every 30-second slot of their window; with gaps it only holds, lowers or pauses.
- **Meters that stop reporting together** (no pair within the new *pairing time*, default 2 s) for 2 minutes while charging are treated like a silent meter: minimum current.
- **Charger status unknown or unavailable:** nothing is sent.
- **Units and power factor:** power in W, kW or MW. Power factor in %, as a fraction, or negative; a Shelly EM's −86 % used to be ignored and treated as 100 %, underestimating the house current.
- **Steady loads:** it re-checks every 15 s, so a steady load still fills every slot.
- **Drying-rack reminder:** "one load on the rack at a time" is now documented and tested. A new load hung elsewhere while the earlier one still dries sets the rack's place.

_Upgrading:_ Re-import the balancer, or let Home Assistant update it. Its memory carries over. To raise or resume, your meters must now report at least every 30 seconds; slower meters only hold, lower or pause. Any power unit other than W, kW or MW now counts as no reading.

## [1.13.0] — 2026-11-23

New: EV charger load balancer.

- **New: EV charger load balancer** ([#36](https://github.com/davidteles/ha-blueprints/pull/36)) — keeps the house + charger under your supply limit by setting the charger's current.
- **Lowers** at once when the room drops.
- **Raises** only after a settle time, and only to the lowest room of the last ~3 minutes.
- **Pauses** below the minimum current, and **resumes** only after the shortest pause once there has been room for ~5 minutes. A load that switches on and off every few seconds (an induction hob, an oven) no longer stops and starts the charger all evening.
- **Safety nets:** a command the charger didn't take is sent again after 2 minutes, and a meter that goes silent while charging drops it to the minimum current.
- It forgets its own pause only when the car is unplugged or someone resumes the charger by hand.
- You choose the pause and resume actions, e.g. a pause switch, or a Wallbox's *Resume schedule* button so it stays on its schedule.
- **Needs:** a whole-house and a charger power meter, and a Text helper (max 255) for its memory.

## [1.12.0] — 2026-11-23

Drying rack: buttons belong to their load; new 'phone almost flat' blueprint.

- **Drying-rack reminder** ([#35](https://github.com/davidteles/ha-blueprints/pull/35))
- **Buttons belong to their load:** *Put away*, *Indoors*, *Outside* and *It's indoors* carry the load they were sent for, so an old notification can no longer empty or move the laundry drying now. Add the "Hung at" helper for this to be exact.
- **A missing forecast isn't "dry":** a failed or empty forecast keeps the rain warning; a real dry forecast clears it; a warning with no forecast for 3 hours expires.
- **One rack:** picking *Not hung* for a second load while the first is drying keeps the first load's place and its rain watch.
- A forecast rain amount of 0.2 mm or more counts as rain (same rule as the drying advice).

## [1.11.0] — 2026-11-22

EV Live Activity: time left, wall charger starts the card.

- **Time left instead of repeating the %:** the charging card reads `15 min left · 80% at 13:35 · 124 kW · 223 km`. New optional input *Remaining charging time* (minutes or hours), counted down between car updates, refreshed every 10 min. Without it: `Charging to 80%`.
- **The wall charger starts the card:** with a charger status set, "car connected / charging" states (new editable input) start the card as soon as the charger does, while the car isn't away. "Waiting for car demand" after charging counts as charged.
- **No "plugged in" flash on unplug:** new input *"Cable not connected" values* (default `connect_cable, disconnected, …`) ends the card at once; cars report it seconds before their plug sensor turns off.

## [1.10.1] — 2026-11-19

Laundry hung: a late tap can't overwrite an answer.

- **Laundry hung (script):** a phone answered "Hung outside", and a dashboard "Hung indoors" tap a moment later was applied as a change of location, so the late tap won. Found in a review and reproduced in a real Home Assistant.

## [1.10.0] — 2026-11-19

Laundry: drying advice, choose where you hung it, nothing to hang.

- **Laundry drying advice** (automation)
- **Laundry hung** (script) for dashboard buttons: *Indoors*, *Outside*, *Not hung* or *Change*. It runs one tap at a time and acts only while something is pending.
- **Laundry done** — a new optional "Where did you hang it?" section.

## [1.9.0] — 2026-11-19

Drying-rack reminder: indoors or outside, with a rain warning.

- **Drying-rack reminder: indoors or outside.** A new optional section. Without it, the blueprint works exactly as before.

## [1.8.1] — 2026-11-18

Integration watchdog wording, how to remove one.

- **Reload an integration when most of it is unavailable:** the messages now read "1 of 1 entity has been unavailable…", "1 of 3 entities has been…", "2 of 3 entities have been…" (and the same in "… still unavailable"). Wording only; behaviour is unchanged.
- **How these are tested** now mentions the automated scenario tests (`pytest`) for the three starter picks and the offline alert, and how to run them. Tested Home Assistant versions are listed.
- New **Remove one** section.

## [1.8.0] — 2026-11-18

Offline alerts say what's dead.

- **Safety sensor offline** now says which integration the sensor belongs to, when it was last heard, and whether the **whole integration** is down (most entities of the same integration entry offline: a cloud or hub problem) or **only this device** (for Zigbee, Z-Wave or…
- The integration is named by its type, never by its title (titles can contain an account e-mail).
- Titles say which sensor and whether it's offline or back; one notification per sensor, replaced when it's back.

## [1.7.1] — 2026-11-18

Clearer Live Activities, Start here, scenario tests.

- **Live Activities don't say the same thing twice.** The side text already shows the key number, so the message no longer repeats it.
- **Start here** in the README: three picks with what each needs, whether it changes devices or only notifies, and a quick check. The safety section says these blueprints add to real alarms and don't replace them.
- **Scenario tests:** 14 tests run the three *Start here* blueprints in a test Home Assistant on every change (normal run, manual override, unavailable input, duplicate events, delays).

## [1.7.0] — 2026-11-17

Guest at home + hide Live Activities until done.

- **Guest at home** (optional switch) for the blueprints that act on an empty house. While someone stays without you.
- **Hide until done** (optional switch) for the **car**, **robot vacuum** and **appliance** Live Activities.
- Robot vacuum: keeps learning each job's area even while the card is hidden.
- Car: 'conserving' (the charger holding the car at its limit) counts as charged.
- Gas meter: a template that wrote `false` as text now writes a real boolean.

## [1.6.0] — 2026-11-16

IKEA BILRESA scroll wheel.

- **IKEA BILRESA scroll wheel (Matter)**: the whole remote in one automation instead of one per channel.

## [1.5.2] — 2026-11-16

- **Live Activity blueprints** (EV charging, appliance, robot vacuum): cards no longer show up twice on the phone. When several sensors changed in the same second, each queued run saw the old phase and started its own card.

## [1.5.1] — 2026-11-16

- **"Buy again" ranking** (shopping): while a cloud to-do list (iCloud Reminders, for example) is unavailable, it now waits quietly and keeps the last ranking instead of logging an error on every change. It refreshes as soon as the list is back.

## [1.5.0] — 2026-11-16

Close-windows reminder names the open windows.

- **Close-windows reminder** (comfort): now only reminds you when a window is actually open, and ends with the open ones ("Open: Kitchen Window and Bedroom Window.").

## [1.4.0] — 2026-11-16

Integration freeze watchdog, weather warning push.

- **Reload an integration when one entity freezes or goes unavailable** (system): reloads the integration when the entity you pick stops reporting or stays unavailable; cooldown and a first-time message.
- **Weather warning push** (safety): notifications for the warning levels you choose from any warning-level sensor; updated when the level changes, removed when it's over.

## [1.3.1] — 2026-11-10

Laundry times survive restarts.

- **Drying-rack reminder:** *Laundry hung at*, for "Drying since …".
- **Laundry done — stays waiting until emptied:** *Finished at*, for "Done since …" when you tap *Remind me later*. A dashboard can show it too.
- **Appliance Live Activity:** *Phase started at*. It keeps three things right after a restart.

## [1.3.0] — 2026-11-10

IPhone widgets, vacuum pause button, Live Activity fixes.

- **Refresh iPhone widgets when something changes:** sends the Home Assistant app's silent *update_widgets* command when the entities in your widget change, so it shows new values straight away. At most once every 5 minutes, because iOS allows only about 40–70 widget reloads a day.
- **Robot vacuum — pause or continue** *(script)*: one button that pauses the robot while it cleans and continues when it's paused or stuck. Put it in an iPhone widget or behind a notification button.
- **[iPhone widget guide](https://github.com/davidteles/ha-blueprints/blob/main/docs/iphone-widgets.md):** a car widget in every size (small, medium and large Home Screen widgets, plus Lock Screen gauge and details), with template sensors to copy.
- **Robot vacuum Live Activity:** the ⚠️ card can say what's wrong, from an optional error text entity. If the robot stays stuck, paused or cleaning for an hour without any change, the card closes by itself and stays closed until the robot is docked again.
- **EV charging Live Activity:** with your wall charger's status sensor (optional), the card closes as soon as you unplug. Car sensors can take hours to notice. An optional car location keeps cards for charging away from home.
- **Appliance ready but not started:** an optional **Start now** button that runs the action you choose, only while remote start is still on.

## [1.2.1] — 2026-11-10

Done card closes when emptied.

- **Appliance Live Activity:** machines that keep reporting "finished" for a long time (many dishwashers and dryers) no longer hold the ✅ done card.
- **Appliance Live Activity:** an optional **"emptied" button** (a Button helper, e.g. a *Hung it up* button on a wall panel). Pressing it closes the done card on every phone and turns off the "laundry waiting" toggle, if you use one.

## [1.2.0] — 2026-11-10

Washer ready phase, vacuum dock fix.

- **Appliance Live Activity:** a new optional **🧺 Ready** phase. While remote start is on (e.g. a Samsung washer's Smart Control) and nothing is programmed or running, a grey card says *Waiting for a programme or Start*.
- **Robot vacuum Live Activity:** lifting the robot off its dock (to clean it, say) reports an error for a few seconds. That no longer starts a "needs help" → "finished" card. An error only counts while it's cleaning.

## [1.1.0] — 2026-11-09

Live Activities, forgotten phone, backup pause.

- **Appliance Live Activity** (washer, dryer, dishwasher): ⏰ programmed with the finish time → stage, progress bar and "50 min left · done around 15:30" → ✅ done with reminders, closing by itself when it's emptied.
- **EV charging Live Activity:** 🔌 plugged in, waiting → ⚡ battery %, power and range → ✅ charged; closes when you unplug.
- **Robot vacuum Live Activity:** m², minutes and battery while it cleans → ✅ finished. Learns each job's size, then shows a progress bar and the time left.
- **Forgotten phone — ask before arming:** someone left, another phone still says *home*, but nothing moves → whoever is away is asked *Arm the alarm* / *Someone's home*. It never arms by itself.
- **Pause heavy apps while a backup runs:** stops the apps you choose just before the scheduled backup and starts them again afterwards.
- **Leaving check** and **Arrival light** no longer react when a phone's Home Assistant app reloads (its person goes *unknown* for a split second, which looked like leaving and arriving).

## [1.0.0] — 2026-11-09

30 blueprints from a real home.

- **Laundry:** done until emptied (with *Remind me later*), drying-rack reminder, ready but not started.
- **Car:** appointment reminders, not plugged in at night (threshold you set on a dashboard), charging outside cheap hours, charger locked with the car plugged in, charging session cost at your live price, car left unlocked while away.
- **Safety:** door left open, safety sensor offline, smoke/CO/heat response, weekly safety check.
- **Leaving and arriving:** leaving check (ignore anything with a label), arrival light.
- **Comfort, energy and housekeeping:** close-windows reminder, keep rooms cool, monthly energy summary, night standby baseline, gas meter from a magnet pulse sensor (with heating split, see docs/gas-meter.md), reload an unavailable integration, restart an offline bulb.
- **Lights and buttons:** motion light with a pause timer, shower light, one button for several jobs.
- **Shopping:** buy-again ranking, add without duplicates (script), shopping list by voice.
- **Small helpers:** pause an appliance while a window is open, alert that clears itself.

[1.18.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.18.0
[1.17.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.17.0
[1.16.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.16.0
[1.15.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.15.0
[1.14.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.14.0
[1.13.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.13.0
[1.12.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.12.0
[1.11.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.11.0
[1.10.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.10.1
[1.10.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.10.0
[1.9.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.9.0
[1.8.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.8.1
[1.8.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.8.0
[1.7.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.7.1
[1.7.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.7.0
[1.6.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.6.0
[1.5.2]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.5.2
[1.5.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.5.1
[1.5.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.5.0
[1.4.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.4.0
[1.3.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.3.1
[1.3.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.3.0
[1.2.1]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.2.1
[1.2.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.2.0
[1.1.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.1.0
[1.0.0]: https://github.com/davidteles/ha-blueprints/releases/tag/v1.0.0
