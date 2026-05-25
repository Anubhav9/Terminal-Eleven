"""Browse every group-stage fixture, grouped by local match date.

Ordering today is purely chronological in the user's local timezone. Future
iterations may add filtering (by group / team / venue) and a click-through
to ``MatchDetailScreen`` — both are noted as follow-ups in the task list.
"""

from __future__ import annotations

from collections import OrderedDict
from datetime import date

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from static_data.fixtures.loader import Fixture, load_group_stage_fixtures


class FixturesScreen(Screen[None]):
    """All group-stage fixtures, ordered chronologically by local date."""

    CSS_PATH = "fixtures.tcss"
    BINDINGS = [
        ("b", "app.pop_screen", "Back"),
        ("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._fixtures: list[Fixture] = []

    # ── compose ─────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="fixtures-shell"):
            yield Static("GROUP STAGE FIXTURES", id="fixtures-title")
            yield Static("", id="fixtures-subtitle")
            # Per-day date headers + DataTables are mounted in on_mount
            # so we can populate their rows after they're attached.
            yield Static("Press b / Esc to go back", id="fixtures-back-hint")

    # ── lifecycle ───────────────────────────────────────────────────

    def on_mount(self) -> None:
        self._fixtures = load_group_stage_fixtures()

        self.query_one("#fixtures-subtitle", Static).update(
            f"{len(self._fixtures)} matches across "
            f"{len(set(_local_date(f) for f in self._fixtures))} days  "
            f"·  ordered by date  ·  times shown in your local timezone"
        )

        shell = self.query_one("#fixtures-shell", VerticalScroll)
        back_hint = self.query_one("#fixtures-back-hint", Static)

        # Insert one (header + table) pair per date, ABOVE the back-hint.
        for match_date, day_fixtures in _group_by_date(self._fixtures).items():
            header = Static(
                f"── {match_date.strftime('%A, %d %B %Y')}  "
                f"({len(day_fixtures)} match"
                f"{'es' if len(day_fixtures) != 1 else ''}) ──",
                classes="date-header",
            )
            table = DataTable(
                classes="day-table",
                show_cursor=False,
                zebra_stripes=True,
            )
            shell.mount(header, before=back_hint)
            shell.mount(table, before=back_hint)

            table.add_column("Kickoff", key="kickoff", width=11)
            table.add_column("Group", key="group", width=7)
            table.add_column("Team A", key="team_a", width=22)
            table.add_column("Team B", key="team_b", width=22)
            table.add_column("Venue", key="venue", width=38)

            for f in day_fixtures:
                local = f.utc_datetime.astimezone()
                table.add_row(
                    local.strftime("%I:%M %p"),
                    f.group,
                    f.team_a,
                    f.team_b,
                    f.venue,
                )


# ─── helpers ────────────────────────────────────────────────────────


def _local_date(fixture: Fixture) -> date:
    return fixture.utc_datetime.astimezone().date()


def _group_by_date(fixtures: list[Fixture]) -> OrderedDict[date, list[Fixture]]:
    """Bucket fixtures by local date, preserving chronological order.

    Assumes ``fixtures`` is already sorted by UTC time — which
    :func:`load_group_stage_fixtures` guarantees. Within each day we also
    keep them in kickoff order for the same reason.
    """
    out: OrderedDict[date, list[Fixture]] = OrderedDict()
    for f in fixtures:
        out.setdefault(_local_date(f), []).append(f)
    return out
