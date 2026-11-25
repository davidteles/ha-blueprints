# Team Tracker: match window and goal alert

The **Team Tracker match memory** blueprint (`blueprints/automation/sports/`) saves the final-whistle
time and the last goal into helpers. These two template helpers turn that into the two rules a
dashboard or screensaver needs. Keep each rule in one helper and point every card at it.

Create them under Settings → Devices & services → Helpers → Create helper → Template → Binary sensor,
and replace `sensor.my_team` and the helper names with yours.

## One sensor per competition (not only "all")

Team Tracker's **"all"** league reads the team's fixture list, not the live scoreboards: it never
reports `IN` or a score, and at kick-off it jumps to the next fixture. Make one Team Tracker sensor per
competition (sport *soccer*, custom league path such as `por.1`, `uefa.champions`,
`por.taca.portugal`) and give the blueprint all of them; keep "all" only as a fallback for
competitions ESPN has no feed for. Then one template sensor picks which one to show (the live match,
else one finished in the last 4 hours, else the nearest kick-off):

```jinja
{%- set ids = ['sensor.my_team_league', 'sensor.my_team_champions', 'sensor.my_team_cup', 'sensor.my_team_all'] -%}
{%- set ns = namespace(live=none, post=none, post_k=none, pre=none, pre_k=none) -%}
{%- for e in ids -%}
{%- set s = states(e) -%}{%- set k = state_attr(e, 'date') | as_datetime(none) -%}
{%- if s == 'IN' and ns.live is none -%}{%- set ns.live = e -%}
{%- elif s == 'POST' and k is not none and now() < k + timedelta(hours=4) and (ns.post_k is none or k > ns.post_k) -%}{%- set ns.post = e -%}{%- set ns.post_k = k -%}
{%- elif s == 'PRE' and k is not none and (ns.pre_k is none or k < ns.pre_k) -%}{%- set ns.pre = e -%}{%- set ns.pre_k = k -%}
{%- endif -%}
{%- endfor -%}
{{ ns.live or ns.post or ns.pre or ids | last }}
```

In the two helpers below, replace `sensor.my_team` with `states('sensor.my_team_match_source')`
read into a variable (`{% set src = states('sensor.my_team_match_source') %}`, then `states(src)`,
`state_attr(src, 'date')`, `is_state(src, 'IN')`).

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
