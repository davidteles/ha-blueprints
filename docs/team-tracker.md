# Team Tracker: match window and goal alert

The **Team Tracker match memory** blueprint (`blueprints/automation/sports/`) saves the final-whistle
time and the last goal into helpers. These two template helpers turn that into the two rules a
dashboard or screensaver needs. Keep each rule in one helper and point every card at it.

Create them under Settings → Devices & services → Helpers → Create helper → Template → Binary sensor,
and replace `sensor.my_team` and the helper names with yours.

## Match window

On from 30 minutes before kick-off, during the match (half time included) and for one hour after the
end. If Home Assistant was down at the final whistle, it uses kick-off + 115 minutes.

```jinja
{% set s = states('sensor.my_team') %}
{% set k = state_attr('sensor.my_team', 'date') | as_datetime(none) %}
{% set ts = state_attr('input_datetime.match_ended_at', 'timestamp') %}
{% set e = ts | as_datetime(none) if ts is number else none %}
{% if s == 'IN' %}true
{% elif s == 'PRE' and k is not none %}{{ now() >= k - timedelta(minutes=30) }}
{% elif s == 'POST' and k is not none %}{% set end = e if e is not none and e > k else k + timedelta(minutes=115) %}{{ now() < end + timedelta(hours=1) }}
{% else %}false{% endif %}
```

## Goal alert

On for 5 minutes after a goal, while the match is live.

```jinja
{% set gts = state_attr('input_datetime.last_goal_at', 'timestamp') %}
{% set gby = states('input_text.last_goal_by') %}
{{ is_state('sensor.my_team', 'IN') and gts is number and gby not in ['', 'unknown', 'unavailable']
   and (now().timestamp() - gts) < 300 }}
```

## Good to know

- Team Tracker's `clock` is ESPN's short status: `67'` while playing, `HT` at half time (the state stays
  `IN`), `FT` at the end.
- For a wall-panel strip with both logos that uses these helpers, see
  [ha-wall-panel-kit](https://github.com/davidteles/ha-wall-panel-kit) `docs/match.md`.
