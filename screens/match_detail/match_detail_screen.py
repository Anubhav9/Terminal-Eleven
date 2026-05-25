from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import datetime

from textual import work
from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Static

from screens.match_detail.big_digits import render_big_number
from screens.match_detail.espn_client import EspnFetchError, fetch_match_snapshot
from screens.match_detail.match_data import (
    Card,
    Goal,
    MatchSnapshot,
    TeamStats,
    demo_snapshot,
)
from screens.match_detail.sound import play as play_sound
from static_data.fixtures.loader import Fixture


REFRESH_INTERVAL_SECONDS = 60.0


def _format_goals(goals: list[Goal]) -> str:
    if not goals:
        return "—"
    return "\n".join(f"⚽ {g.scorer}  {g.minute}" for g in goals)


def _format_cards(cards: list[Card]) -> str:
    if not cards:
        return "—"
    lines = []
    for c in cards:
        marker = "🟨" if c.color == "yellow" else "🟥"
        lines.append(f"{marker} {c.player}  {c.minute}")
    return "\n".join(lines)


_STAT_ROWS: list[tuple[str, str]] = [
    ("Possession",       "possession_pct"),
    ("Shots",            "shots"),
    ("Shots on target",  "shots_on_target"),
    ("Passes",           "passes"),
    ("Pass accuracy",    "pass_accuracy_pct"),
    ("Fouls",            "fouls"),
    ("Corners",          "corners"),
    ("Offsides",         "offsides"),
]
_PCT_STATS = {"possession_pct", "pass_accuracy_pct"}


def _format_stat(stat: TeamStats | None, attr: str) -> str:
    if stat is None:
        return "—"
    val = getattr(stat, attr)
    return f"{val}%" if attr in _PCT_STATS else str(val)


def _is_half_time(snap: MatchSnapshot) -> bool:
    """ESPN sends period descriptions like "Halftime" / "Half Time"."""
    period = snap.period.lower()
    return "halftime" in period or "half time" in period or "half-time" in period


def _is_full_time(snap: MatchSnapshot) -> bool:
    """Match is over (state == 'post' in ESPN parlance)."""
    period = snap.period.lower()
    return (
        "full time" in period
        or "final" in period
        or snap.minute.upper() == "FT"
    )


class MatchDetailScreen(Screen[None]):
    """Live score / match detail for a single fixture.

    Refreshes its snapshot every ``REFRESH_INTERVAL_SECONDS`` seconds.
    Today the snapshot comes from ``demo_snapshot``; once the ESPN fetch is
    wired in, swap the body of :meth:`_fetch_snapshot`.
    """

    CSS_PATH = "match_detail.tcss"
    BINDINGS = [
        ("b", "app.pop_screen", "Back"),
        ("escape", "app.pop_screen", "Back"),
        ("t", "test_sounds", "Test sounds (goal + whistle)"),
        ("s", "simulate_match", "Simulate a live match (dev)"),
    ]

    def __init__(self, fixture: Fixture, snapshot: MatchSnapshot) -> None:
        super().__init__()
        self._fixture = fixture
        self._snap = snapshot
        # Sounds only start firing after the first successful real fetch,
        # so we don't pop a "GOAL!" when we transition from the placeholder
        # demo snapshot to ESPN's actual data.
        self._sounds_armed = False

    # ── compose ─────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        snap = self._snap
        with VerticalScroll(id="match-shell"):
            with Horizontal(id="team-header-row"):
                yield Static(snap.team_a.upper(), id="team-a-name", classes="team-name team-a-color")
                yield Static("VS", id="vs-label")
                yield Static(snap.team_b.upper(), id="team-b-name", classes="team-name team-b-color")

            with Horizontal(id="score-row"):
                yield Static(render_big_number(snap.score_a), id="score-a", classes="big-score team-a-color")
                with Vertical(id="clock-block"):
                    yield Static(snap.minute, id="match-minute")
                    yield Static(snap.period, id="match-period")
                    yield Static("● LIVE" if snap.is_live else "○ NOT LIVE", id="live-badge")
                yield Static(render_big_number(snap.score_b), id="score-b", classes="big-score team-b-color")

            yield Static("── GOALS ──", classes="section-divider")
            with Horizontal(id="goals-row"):
                yield Static(_format_goals(snap.goals_a), id="goals-a", classes="side-block team-a-color")
                yield Static(_format_goals(snap.goals_b), id="goals-b", classes="side-block team-b-color")

            yield Static("── CARDS ──", classes="section-divider")
            with Horizontal(id="cards-row"):
                yield Static(_format_cards(snap.cards_a), id="cards-a", classes="side-block team-a-color")
                yield Static(_format_cards(snap.cards_b), id="cards-b", classes="side-block team-b-color")

            yield Static("── MATCH STATS ──", classes="section-divider")
            with Grid(id="stats-grid"):
                yield Static(snap.team_a, id="stats-header-a", classes="stats-header team-a-color")
                yield Static("", classes="stats-header")
                yield Static(snap.team_b, id="stats-header-b", classes="stats-header team-b-color")
                for label, attr in _STAT_ROWS:
                    yield Static(
                        _format_stat(snap.stats_a, attr),
                        id=f"stat-{attr}-a",
                        classes="stat-value team-a-color",
                    )
                    yield Static(label, classes="stat-label")
                    yield Static(
                        _format_stat(snap.stats_b, attr),
                        id=f"stat-{attr}-b",
                        classes="stat-value team-b-color",
                    )

            yield Static(
                f"Venue: {self._fixture.venue}   ·   ESPN id: {self._fixture.espn_event_id or '—'}",
                id="match-meta",
            )
            yield Static("", id="match-refreshed-at")
            yield Static("Press b / Esc to go back", id="match-back-hint")

    # ── lifecycle ────────────────────────────────────────────────────

    def on_mount(self) -> None:
        self._apply_snapshot(self._snap)
        self._refresh()
        self.set_interval(REFRESH_INTERVAL_SECONDS, self._refresh)

    # ── data fetch (async worker → ESPN) ────────────────────────────

    @work(exclusive=True)
    async def _refresh(self) -> None:
        """Fetch a fresh snapshot from ESPN and re-render.

        Runs as an exclusive Textual worker so a tick that arrives while a
        previous fetch is still in flight cancels the old one instead of
        stacking up. Failures are reported in the footer; the screen keeps
        showing the last good snapshot.
        """
        fixture = self._fixture
        self._set_status_line(
            f"Fetching ESPN summary for event {fixture.espn_event_id or '—'}…"
        )

        if not fixture.espn_event_id:
            self._set_status_line(
                "No ESPN event id for this fixture — showing demo snapshot."
            )
            return

        try:
            snap = await fetch_match_snapshot(
                event_id=fixture.espn_event_id,
                fallback_team_a=fixture.team_a,
                fallback_team_b=fixture.team_b,
            )
        except EspnFetchError as exc:
            self._set_status_line(f"Fetch failed: {exc}")
            return

        previous = self._snap
        self._snap = snap
        self._apply_snapshot(snap)

        # Only diff against the previous *real* snapshot. The very first
        # successful fetch transitions us from the placeholder demo, and we
        # don't want a phantom "GOAL!" beep at that boundary.
        if self._sounds_armed:
            self._announce_changes(previous, snap)
        self._sounds_armed = True

    # ── live-event detection ────────────────────────────────────────

    def _announce_changes(
        self, old: MatchSnapshot, new: MatchSnapshot
    ) -> None:
        """Compare two snapshots and emit sound + toast for newsworthy diffs."""
        if new.score_a > old.score_a:
            self._announce_goal(
                team=new.team_a,
                score_line=f"{new.score_a}-{new.score_b}",
                goals=new.goals_a,
                previous_count=len(old.goals_a),
            )
        if new.score_b > old.score_b:
            self._announce_goal(
                team=new.team_b,
                score_line=f"{new.score_a}-{new.score_b}",
                goals=new.goals_b,
                previous_count=len(old.goals_b),
            )

        if _is_half_time(new) and not _is_half_time(old):
            play_sound("half_time", app=self.app)
            self.app.notify(
                f"⏸  HALF TIME — {new.team_a} {new.score_a}-{new.score_b} {new.team_b}",
                title="Half-Time",
                severity="information",
                timeout=10,
            )
        elif _is_full_time(new) and not _is_full_time(old):
            play_sound("full_time", app=self.app)
            self.app.notify(
                f"🏁  FULL TIME — {new.team_a} {new.score_a}-{new.score_b} {new.team_b}",
                title="Full-Time",
                severity="information",
                timeout=10,
            )

    def _announce_goal(
        self,
        *,
        team: str,
        score_line: str,
        goals: list[Goal],
        previous_count: int,
    ) -> None:
        play_sound("goal", app=self.app)
        scorer_suffix = ""
        if len(goals) > previous_count and goals:
            latest = goals[-1]
            scorer_suffix = f" — {latest.scorer} ({latest.minute})"
        self.app.notify(
            f"⚽ GOAL! {team} {score_line}{scorer_suffix}",
            title="Goal",
            severity="information",
            timeout=10,
        )

    # ── dev / manual test ──────────────────────────────────────────

    def action_test_sounds(self) -> None:
        """Play goal + half-time + full-time and pop a toast — verifies
        audio works even when watching a finished demo match where nothing
        actually changes."""
        play_sound("goal", app=self.app)
        self.app.notify(
            "Sound check: goal stinger now → half-time whistle in 5s "
            "→ full-time whistle in 7s",
            title="Sound check",
            severity="information",
            timeout=8,
        )
        self.set_timer(5.0, lambda: play_sound("half_time", app=self.app))
        self.set_timer(7.0, lambda: play_sound("full_time", app=self.app))

    @work(exclusive=True)
    async def action_simulate_match(self) -> None:
        """Pretend the current snapshot is a live match.

        Walks through a scripted timeline (goal A → goal B → half-time →
        goal A → full-time) by mutating ``self._snap`` and running it
        through the same :meth:`_announce_changes` diff path that the real
        ESPN refresh uses. Useful when there's no real live match to watch
        (which is most of the time before the tournament starts).
        """
        # Reset to a clean 0–0 first-half snapshot so the simulation is
        # repeatable no matter what we were just looking at.
        base = replace(
            self._snap,
            score_a=0,
            score_b=0,
            minute="0'",
            period="1st Half",
            is_live=True,
            goals_a=[],
            goals_b=[],
        )
        previous = base
        self._snap = base
        self._apply_snapshot(base)
        self._sounds_armed = True
        self.app.notify(
            "Simulating a live match — 5 events over ~12s",
            title="Sim",
            severity="information",
            timeout=4,
        )

        # Build the scripted timeline; each step chains from the previous one.
        events: list[tuple[MatchSnapshot, float]] = []
        step1 = replace(
            previous,
            score_a=1, minute="18'",
            goals_a=[Goal(scorer="Lozano", minute="18'")],
        )
        events.append((step1, 2.5))

        step2 = replace(
            step1,
            score_b=1, minute="37'",
            goals_b=[Goal(scorer="Mokoena", minute="37'")],
        )
        events.append((step2, 2.5))

        step3 = replace(step2, minute="HT", period="Half Time", is_live=False)
        events.append((step3, 2.5))

        step4 = replace(
            step3,
            score_a=2, minute="58'", period="2nd Half", is_live=True,
            goals_a=step3.goals_a + [Goal(scorer="Vega", minute="58'")],
        )
        events.append((step4, 2.5))

        step5 = replace(step4, minute="FT", period="Full Time", is_live=False)
        events.append((step5, 0))

        for new_snap, delay_before_next in events:
            await asyncio.sleep(2.0)
            old = self._snap
            self._snap = new_snap
            self._apply_snapshot(new_snap)
            self._announce_changes(old, new_snap)
            if delay_before_next:
                await asyncio.sleep(delay_before_next - 2.0)

    # ── widget updates ──────────────────────────────────────────────

    def _apply_snapshot(self, snap: MatchSnapshot) -> None:
        self.query_one("#score-a", Static).update(render_big_number(snap.score_a))
        self.query_one("#score-b", Static).update(render_big_number(snap.score_b))
        self.query_one("#match-minute", Static).update(snap.minute)
        self.query_one("#match-period", Static).update(snap.period)
        self.query_one("#live-badge", Static).update("● LIVE" if snap.is_live else "○ NOT LIVE")

        self.query_one("#goals-a", Static).update(_format_goals(snap.goals_a))
        self.query_one("#goals-b", Static).update(_format_goals(snap.goals_b))

        self.query_one("#cards-a", Static).update(_format_cards(snap.cards_a))
        self.query_one("#cards-b", Static).update(_format_cards(snap.cards_b))

        for _, attr in _STAT_ROWS:
            self.query_one(f"#stat-{attr}-a", Static).update(_format_stat(snap.stats_a, attr))
            self.query_one(f"#stat-{attr}-b", Static).update(_format_stat(snap.stats_b, attr))

        now = datetime.now().astimezone().strftime("%H:%M:%S %Z")
        self._set_status_line(
            f"Last refreshed: {now}   ·   auto-refresh every "
            f"{int(REFRESH_INTERVAL_SECONDS)} seconds"
        )

    def _set_status_line(self, message: str) -> None:
        self.query_one("#match-refreshed-at", Static).update(message)
