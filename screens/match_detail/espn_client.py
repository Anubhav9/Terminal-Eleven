"""Async client + parser for ESPN's soccer match-summary endpoint.

Endpoint:
    GET https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary
        ?event={espn_event_id}

The shape of the response is captured here by example so we know what we map:

* ``header.competitions[0].competitors[]``       team display name + score
* ``header.competitions[0].status.type``         state (pre/in/post), description
* ``header.competitions[0].status.displayClock`` live match clock (e.g. "63'")
* ``keyEvents[]``                                goals / cards (with player + minute)
* ``boxscore.teams[].statistics[]``              possession / shots / passes / etc.
"""

from __future__ import annotations

import httpx

from screens.match_detail.match_data import Card, Goal, MatchSnapshot, TeamStats


_SUMMARY_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary"
)
_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


class EspnFetchError(RuntimeError):
    """Anything that goes wrong between the screen and a usable snapshot."""


# ─── public entry point ────────────────────────────────────────────────────────


async def fetch_match_snapshot(
    *,
    event_id: str,
    fallback_team_a: str,
    fallback_team_b: str,
) -> MatchSnapshot:
    """Fetch one match from ESPN and return a parsed ``MatchSnapshot``.

    ``fallback_team_*`` are used both to align ESPN's competitors[] order with
    our ``team_a / team_b`` convention, and as a graceful fallback when ESPN
    omits a field.

    Raises :class:`EspnFetchError` on any network / JSON / shape problem.
    """
    if not event_id:
        raise EspnFetchError("No ESPN event id available for this fixture.")

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        try:
            resp = await client.get(_SUMMARY_URL, params={"event": event_id})
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise EspnFetchError(f"HTTP error: {exc}") from exc

        try:
            data = resp.json()
        except ValueError as exc:
            raise EspnFetchError(f"Bad JSON from ESPN: {exc}") from exc

    return parse_summary(data, fallback_team_a, fallback_team_b)


# ─── parser ────────────────────────────────────────────────────────────────────

# ESPN stat name → snake_case field on TeamStats
_STAT_FIELD_MAP: dict[str, str] = {
    "possessionPct":  "possession_pct",
    "totalShots":     "shots",
    "shotsOnTarget":  "shots_on_target",
    "totalPasses":    "passes",
    "passPct":        "pass_accuracy_pct",
    "foulsCommitted": "fouls",
    "wonCorners":     "corners",
    "offsides":       "offsides",
}

# ESPN sends some percentages as 0.0–1.0 decimals; these need × 100.
_PCT_DECIMAL_FIELDS: set[str] = {"pass_accuracy_pct"}


def parse_summary(
    data: dict, fallback_a: str, fallback_b: str
) -> MatchSnapshot:
    """Map an ESPN ``/summary`` JSON payload into our domain ``MatchSnapshot``."""
    try:
        comp = data["header"]["competitions"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise EspnFetchError(f"Unexpected response shape: {exc}") from exc

    competitors = comp.get("competitors") or []
    if len(competitors) < 2:
        raise EspnFetchError("Fewer than 2 competitors in response.")

    team_a_data, team_b_data = _align_competitors(
        competitors[0], competitors[1], fallback_a, fallback_b
    )

    team_a = (team_a_data.get("team") or {}).get("displayName") or fallback_a
    team_b = (team_b_data.get("team") or {}).get("displayName") or fallback_b
    team_a_id = (team_a_data.get("team") or {}).get("id")
    team_b_id = (team_b_data.get("team") or {}).get("id")

    score_a = _safe_int(team_a_data.get("score"))
    score_b = _safe_int(team_b_data.get("score"))

    minute, period, is_live = _read_status(comp)

    goals_a, goals_b, cards_a, cards_b = _read_key_events(
        data.get("keyEvents") or [], team_a_id, team_b_id
    )

    stats_a, stats_b = _read_stats(
        data.get("boxscore") or {}, team_a_id, team_b_id
    )

    return MatchSnapshot(
        team_a=team_a,
        team_b=team_b,
        score_a=score_a,
        score_b=score_b,
        minute=minute,
        period=period,
        goals_a=goals_a,
        goals_b=goals_b,
        cards_a=cards_a,
        cards_b=cards_b,
        stats_a=stats_a,
        stats_b=stats_b,
        is_live=is_live,
    )


# ─── helpers ───────────────────────────────────────────────────────────────────


def _align_competitors(
    c0: dict, c1: dict, fallback_a: str, fallback_b: str
) -> tuple[dict, dict]:
    """Reorder ESPN's [c0, c1] so they line up with our (team_a, team_b)."""
    name0 = ((c0.get("team") or {}).get("displayName") or "").lower()
    name1 = ((c1.get("team") or {}).get("displayName") or "").lower()
    fa, fb = fallback_a.lower(), fallback_b.lower()

    if name0 == fa or name1 == fb:
        return c0, c1
    if name1 == fa or name0 == fb:
        return c1, c0
    return c0, c1


def _safe_int(raw: object) -> int:
    if raw in (None, ""):
        return 0
    try:
        return int(raw)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def _read_status(comp: dict) -> tuple[str, str, bool]:
    """Return ``(minute, period, is_live)`` from competition.status."""
    status = comp.get("status") or {}
    type_ = status.get("type") or {}
    state = type_.get("state") or "pre"
    desc = type_.get("description") or ""
    short = type_.get("shortDetail") or ""

    if state == "pre":
        return "0'", "Not Started", False
    if state == "post":
        return "FT", desc or "Full Time", False

    # state == "in" → live
    display_clock = (status.get("displayClock") or "").strip()
    minute = display_clock or short or "—"
    return minute, desc or "Live", True


def _read_key_events(
    events: list[dict], team_a_id: str | None, team_b_id: str | None
) -> tuple[list[Goal], list[Goal], list[Card], list[Card]]:
    goals_a: list[Goal] = []
    goals_b: list[Goal] = []
    cards_a: list[Card] = []
    cards_b: list[Card] = []

    for ev in events:
        if ev.get("shootout"):
            continue

        ev_team_id = (ev.get("team") or {}).get("id")
        if ev_team_id == team_a_id:
            side = "a"
        elif ev_team_id == team_b_id:
            side = "b"
        else:
            continue

        minute_str = ((ev.get("clock") or {}).get("displayValue") or "").strip()
        player = _extract_player_name(ev)

        type_obj = ev.get("type") or {}
        type_text = (type_obj.get("text") or "").lower()

        # ``scoringPlay`` is ESPN's canonical "this counted on the scoreboard"
        # flag — covers regular goals, headers, penalties, and own goals.
        if ev.get("scoringPlay"):
            (goals_a if side == "a" else goals_b).append(
                Goal(scorer=player, minute=minute_str)
            )
            continue

        if "yellow card" in type_text:
            (cards_a if side == "a" else cards_b).append(
                Card(player=player, minute=minute_str, color="yellow")
            )
        elif "red card" in type_text:
            (cards_a if side == "a" else cards_b).append(
                Card(player=player, minute=minute_str, color="red")
            )

    return goals_a, goals_b, cards_a, cards_b


def _extract_player_name(ev: dict) -> str:
    """Pull the primary athlete from an ESPN keyEvent.

    ESPN exposes the player under two different schemas depending on age and
    endpoint version:

    * ``participants[*].athlete.displayName``  (newer / current)
    * ``athletesInvolved[*].displayName``      (older payloads)

    We try both, then fall back to the human-readable ``shortText``.
    """
    participants = ev.get("participants") or []
    if participants and isinstance(participants[0], dict):
        athlete = participants[0].get("athlete") or {}
        name = athlete.get("displayName")
        if name:
            return name

    athletes = ev.get("athletesInvolved") or []
    if athletes and isinstance(athletes[0], dict):
        name = athletes[0].get("displayName")
        if name:
            return name

    short = (ev.get("shortText") or "").strip()
    return short or "Unknown"


def _read_stats(
    boxscore: dict, team_a_id: str | None, team_b_id: str | None
) -> tuple[TeamStats | None, TeamStats | None]:
    stats_a: TeamStats | None = None
    stats_b: TeamStats | None = None
    for tb in boxscore.get("teams") or []:
        team_id = (tb.get("team") or {}).get("id")
        parsed = _parse_team_stats(tb.get("statistics") or [])
        if team_id == team_a_id:
            stats_a = parsed
        elif team_id == team_b_id:
            stats_b = parsed
    return stats_a, stats_b


def _parse_team_stats(statistics: list[dict]) -> TeamStats:
    values: dict[str, int] = {field: 0 for field in _STAT_FIELD_MAP.values()}
    for s in statistics:
        name = s.get("name")
        if name in _STAT_FIELD_MAP:
            field = _STAT_FIELD_MAP[name]
            values[field] = _coerce_stat_value(field, s.get("displayValue", "0"))
    return TeamStats(**values)


def _coerce_stat_value(field: str, raw: str) -> int:
    try:
        as_float = float(raw)
    except (TypeError, ValueError):
        return 0
    if field in _PCT_DECIMAL_FIELDS:
        return int(round(as_float * 100))
    return int(round(as_float))
